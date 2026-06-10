"""
Schema Loader
从数据库或DDL文件加载schema信息
"""
import re
from typing import List, Optional, Dict, Any
from pathlib import Path
from .models import TableInfo, ColumnInfo, SchemaInfo
from .config import DatabaseConfig


class SchemaLoader:
    """Schema加载器"""
    
    def __init__(self, config: Optional[DatabaseConfig] = None):
        self.config = config or DatabaseConfig()
        self.engine = None
        self._init_engine()
    
    def _init_engine(self):
        """初始化数据库引擎"""
        try:
            from sqlalchemy import create_engine
            self.engine = create_engine(self.config.connection_string)
        except ImportError:
            print("警告: sqlalchemy未安装，只能使用DDL文件加载")
    
    def load_from_database(self, schemas: Optional[List[str]] = None) -> SchemaInfo:
        """从数据库加载schema"""
        if self.engine is None:
            raise RuntimeError("数据库引擎未初始化")
        
        from sqlalchemy import inspect, text
        
        inspector = inspect(self.engine)
        schema_info = SchemaInfo()
        
        # 获取所有表
        table_names = inspector.get_table_names(schema=schemas[0] if schemas else None)
        
        for table_name in table_names:
            # 获取列信息
            columns = []
            for col in inspector.get_columns(table_name):
                col_info = ColumnInfo(
                    name=col["name"],
                    data_type=str(col["type"]),
                    is_nullable=col.get("nullable", True),
                    is_primary_key=False  # 稍后设置
                )
                columns.append(col_info)
            
            # 获取主键
            pk = inspector.get_pk_constraint(table_name)
            pk_cols = pk.get("constrained_columns", [])
            for col in columns:
                if col.name in pk_cols:
                    col.is_primary_key = True
            
            # 获取外键
            fks = inspector.get_foreign_keys(table_name)
            foreign_keys = []
            for fk in fks:
                for local_col, ref_col in zip(
                    fk.get("constrained_columns", []),
                    fk.get("referred_columns", [])
                ):
                    foreign_keys.append({
                        "column": local_col,
                        "ref_table": fk["referred_table"],
                        "ref_column": ref_col
                    })
                    # 标记外键列
                    for col in columns:
                        if col.name == local_col:
                            col.is_foreign_key = True
            
            # 获取表注释
            try:
                comment = inspector.get_table_comment(table_name).get("text")
            except Exception:
                comment = None
            
            # 获取行数（估算）
            try:
                with self.engine.connect() as conn:
                    result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
                    row_count = result.scalar()
            except Exception:
                row_count = None
            
            table_info = TableInfo(
                name=table_name,
                schema=schemas[0] if schemas else None,
                columns=columns,
                comment=comment,
                row_count=row_count,
                primary_key=pk_cols,
                foreign_keys=foreign_keys
            )
            schema_info.tables.append(table_info)
        
        return schema_info
    
    def load_from_ddl(self, ddl_text: str) -> SchemaInfo:
        """从DDL文本解析schema"""
        schema_info = SchemaInfo()
        
        # 简单的CREATE TABLE解析
        pattern = r'CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?(\w+)\s*\((.*?)\);'
        matches = re.findall(pattern, ddl_text, re.IGNORECASE | re.DOTALL)
        
        for table_name, columns_text in matches:
            columns = []
            primary_key = []
            foreign_keys = []
            
            # 解析列定义
            for line in columns_text.split("\n"):
                line = line.strip().rstrip(",")
                if not line:
                    continue
                
                # 跳过约束定义
                if line.upper().startswith(("PRIMARY KEY", "FOREIGN KEY", "UNIQUE", "INDEX", "KEY", "CONSTRAINT")):
                    if line.upper().startswith("PRIMARY KEY"):
                        pk_match = re.search(r'PRIMARY\s+KEY\s*\((.*?)\)', line, re.IGNORECASE)
                        if pk_match:
                            primary_key = [c.strip() for c in pk_match.group(1).split(",")]
                    continue
                
                # 解析列
                col_match = re.match(r'(\w+)\s+(\w+(?:\([^)]*\))?)(.*)', line)
                if col_match:
                    col_name = col_match.group(1)
                    col_type = col_match.group(2)
                    col_rest = col_match.group(3).upper()
                    
                    comment = None
                    comment_match = re.search(r'--\s*(.+)$', line)
                    if comment_match:
                        comment = comment_match.group(1).strip()
                    
                    is_pk = "PRIMARY KEY" in col_rest
                    is_nullable = "NOT NULL" not in col_rest
                    is_fk = "REFERENCES" in col_rest
                    
                    if is_pk:
                        primary_key.append(col_name)
                    
                    # 解析外键引用
                    if is_fk:
                        ref_match = re.search(r'REFERENCES\s+(\w+)\s*\(\s*(\w+)\s*\)', line, re.IGNORECASE)
                        if ref_match:
                            foreign_keys.append({
                                "column": col_name,
                                "ref_table": ref_match.group(1),
                                "ref_column": ref_match.group(2)
                            })
                    
                    columns.append(ColumnInfo(
                        name=col_name,
                        data_type=col_type,
                        is_nullable=is_nullable,
                        is_primary_key=is_pk,
                        is_foreign_key=is_fk,
                        comment=comment
                    ))
            
            table_info = TableInfo(
                name=table_name,
                columns=columns,
                primary_key=primary_key,
                foreign_keys=foreign_keys
            )
            schema_info.tables.append(table_info)
        
        return schema_info
    
    def load_from_ddl_file(self, file_path: str) -> SchemaInfo:
        """从DDL文件加载schema"""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"DDL文件不存在: {file_path}")
        
        ddl_text = path.read_text(encoding="utf-8")
        return self.load_from_ddl(ddl_text)
    
    def load_from_dict(self, schema_dict: Dict[str, Any]) -> SchemaInfo:
        """从字典加载schema（用于测试）"""
        schema_info = SchemaInfo()
        
        for table_name, table_data in schema_dict.items():
            columns = []
            for col in table_data.get("columns", []):
                columns.append(ColumnInfo(
                    name=col["name"],
                    data_type=col.get("type", "TEXT"),
                    is_nullable=col.get("nullable", True),
                    is_primary_key=col.get("primary_key", False),
                    is_foreign_key=col.get("foreign_key", False),
                    comment=col.get("comment")
                ))
            
            table_info = TableInfo(
                name=table_name,
                columns=columns,
                comment=table_data.get("comment"),
                primary_key=table_data.get("primary_key"),
                foreign_keys=table_data.get("foreign_keys", [])
            )
            schema_info.tables.append(table_info)
        
        return schema_info
    
    def get_sample_data(self, table_name: str, limit: int = 5) -> List[Dict[str, Any]]:
        """获取表的样本数据"""
        if self.engine is None:
            return []
        
        try:
            from sqlalchemy import text
            with self.engine.connect() as conn:
                result = conn.execute(text(f"SELECT * FROM {table_name} LIMIT {limit}"))
                columns = list(result.keys())
                return [dict(zip(columns, row)) for row in result.fetchall()]
        except Exception as e:
            print(f"获取样本数据失败: {e}")
            return []
