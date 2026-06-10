"""
SQL Executor
安全的SQL执行器
"""
import re
import time
from typing import List, Dict, Any, Optional
from .models import SQLResult
from .config import DatabaseConfig


# 危险SQL关键词（默认禁止）
DANGEROUS_KEYWORDS = [
    "DROP", "TRUNCATE", "DELETE", "ALTER", "CREATE", "INSERT", "UPDATE",
    "GRANT", "REVOKE", "EXEC", "EXECUTE", "SHUTDOWN"
]


class SQLExecutor:
    """SQL执行器"""
    
    def __init__(self, config: Optional[DatabaseConfig] = None, 
                 allow_write: bool = False):
        self.config = config or DatabaseConfig()
        self.allow_write = allow_write
        self.engine = None
        self._init_engine()
    
    def _init_engine(self):
        """初始化数据库引擎"""
        try:
            from sqlalchemy import create_engine
            self.engine = create_engine(self.config.connection_string)
        except ImportError:
            print("警告: sqlalchemy未安装")
    
    def validate_sql(self, sql: str) -> tuple[bool, Optional[str]]:
        """验证SQL安全性"""
        
        if not sql or not sql.strip():
            return False, "SQL为空"
        
        # 检查危险关键词
        if not self.allow_write:
            sql_upper = sql.upper()
            for keyword in DANGEROUS_KEYWORDS:
                # 使用词边界匹配，避免误判
                pattern = rf'\b{keyword}\b'
                if re.search(pattern, sql_upper):
                    return False, f"包含禁止的操作: {keyword}"
        
        # 检查多语句（防注入）
        statements = [s.strip() for s in sql.split(";") if s.strip()]
        if len(statements) > 1:
            return False, "不允许多语句执行"
        
        # 检查注释注入
        if "--" in sql or "/*" in sql:
            # 简单的注释检查（允许尾部注释）
            lines = sql.split("\n")
            for line in lines[:-1]:  # 允许最后一行有注释
                if "--" in line and not line.strip().startswith("--"):
                    pass  # 允许行内注释
        
        return True, None
    
    def execute(self, sql: str, params: Optional[Dict] = None) -> SQLResult:
        """执行SQL"""
        
        # 验证
        is_safe, error = self.validate_sql(sql)
        if not is_safe:
            return SQLResult(
                sql=sql,
                success=False,
                error=error
            )
        
        if self.engine is None:
            return SQLResult(
                sql=sql,
                success=False,
                error="数据库引擎未初始化"
            )
        
        start_time = time.time()
        
        try:
            from sqlalchemy import text
            
            with self.engine.connect() as conn:
                result = conn.execute(text(sql), params or {})
                
                # 检查是否有结果集
                if result.returns_rows:
                    columns = list(result.keys())
                    rows = [dict(zip(columns, row)) for row in result.fetchall()]
                    
                    execution_time = (time.time() - start_time) * 1000
                    
                    return SQLResult(
                        sql=sql,
                        success=True,
                        data=rows,
                        columns=columns,
                        row_count=len(rows),
                        execution_time_ms=round(execution_time, 2)
                    )
                else:
                    # 没有结果集（如INSERT/UPDATE等）
                    conn.commit()
                    execution_time = (time.time() - start_time) * 1000
                    
                    return SQLResult(
                        sql=sql,
                        success=True,
                        data=None,
                        columns=None,
                        row_count=result.rowcount,
                        execution_time_ms=round(execution_time, 2)
                    )
        
        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            return SQLResult(
                sql=sql,
                success=False,
                error=str(e),
                execution_time_ms=round(execution_time, 2)
            )
    
    def execute_batch(self, sqls: List[str]) -> List[SQLResult]:
        """批量执行SQL"""
        results = []
        for sql in sqls:
            result = self.execute(sql)
            results.append(result)
            if not result.success:
                break  # 遇到错误停止
        return results
    
    def get_table_info(self, table_name: str) -> Optional[Dict[str, Any]]:
        """获取表信息"""
        if self.engine is None:
            return None
        
        try:
            from sqlalchemy import inspect, text
            
            inspector = inspect(self.engine)
            
            # 检查表是否存在
            if table_name not in inspector.get_table_names():
                return None
            
            columns = inspector.get_columns(table_name)
            pk = inspector.get_pk_constraint(table_name)
            fks = inspector.get_foreign_keys(table_name)
            
            # 获取行数
            with self.engine.connect() as conn:
                count = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}")).scalar()
            
            return {
                "name": table_name,
                "columns": [{
                    "name": col["name"],
                    "type": str(col["type"]),
                    "nullable": col.get("nullable", True)
                } for col in columns],
                "primary_key": pk.get("constrained_columns", []),
                "foreign_keys": fks,
                "row_count": count
            }
        except Exception as e:
            print(f"获取表信息失败: {e}")
            return None
    
    def close(self):
        """关闭连接"""
        if self.engine:
            self.engine.dispose()
