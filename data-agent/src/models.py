"""
Data Models for Data Agent
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime


class QueryType(str, Enum):
    """查询类型"""
    SELECT = "select"
    ANALYSIS = "analysis"
    AGGREGATION = "aggregation"
    COMPARISON = "comparison"
    UNKNOWN = "unknown"


class ColumnInfo(BaseModel):
    """列信息"""
    name: str
    data_type: str
    is_nullable: bool = True
    is_primary_key: bool = False
    is_foreign_key: bool = False
    comment: Optional[str] = None
    sample_values: List[Any] = Field(default_factory=list)


class TableInfo(BaseModel):
    """表信息"""
    name: str
    schema: Optional[str] = None
    columns: List[ColumnInfo] = Field(default_factory=list)
    comment: Optional[str] = None
    row_count: Optional[int] = None
    primary_key: Optional[List[str]] = None
    foreign_keys: List[Dict[str, str]] = Field(default_factory=list)
    
    def to_ddl(self) -> str:
        """转换为DDL语句"""
        cols = []
        for col in self.columns:
            col_def = f"  {col.name} {col.data_type}"
            if not col.is_nullable:
                col_def += " NOT NULL"
            if col.is_primary_key:
                col_def += " PRIMARY KEY"
            if col.comment:
                col_def += f"  -- {col.comment}"
            cols.append(col_def)
        
        ddl = f"CREATE TABLE {self.name} (\n"
        ddl += ",\n".join(cols)
        ddl += "\n);"
        
        if self.comment:
            ddl += f"\n-- {self.comment}"
        
        return ddl


class SchemaInfo(BaseModel):
    """Schema信息"""
    tables: List[TableInfo] = Field(default_factory=list)
    relationships: List[Dict[str, str]] = Field(default_factory=list)
    
    def get_table(self, name: str) -> Optional[TableInfo]:
        """获取指定表"""
        for table in self.tables:
            if table.name.lower() == name.lower():
                return table
        return None
    
    def to_ddl(self) -> str:
        """转换为完整DDL"""
        ddls = [table.to_ddl() for table in self.tables]
        return "\n\n".join(ddls)


class SQLResult(BaseModel):
    """SQL执行结果"""
    sql: str
    success: bool
    data: Optional[List[Dict[str, Any]]] = None
    columns: Optional[List[str]] = None
    row_count: int = 0
    error: Optional[str] = None
    execution_time_ms: Optional[float] = None
    
    def to_markdown(self) -> str:
        """转换为Markdown表格"""
        if not self.success:
            return f"❌ 执行失败: {self.error}"
        
        if not self.data:
            return "✅ 查询成功，但无结果数据"
        
        # 生成Markdown表格
        md = "| " + " | ".join(self.columns) + " |\n"
        md += "| " + " | ".join(["---"] * len(self.columns)) + " |\n"
        
        for row in self.data[:20]:  # 限制显示行数
            values = [str(row.get(col, "")) for col in self.columns]
            md += "| " + " | ".join(values) + " |\n"
        
        if self.row_count > 20:
            md += f"\n... 共 {self.row_count} 行（仅显示前20行）"
        
        return md


class ChatMessage(BaseModel):
    """聊天消息"""
    role: str  # user, assistant, system
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)
    sql: Optional[str] = None
    query_result: Optional[SQLResult] = None


class ConversationContext(BaseModel):
    """对话上下文"""
    session_id: str
    messages: List[ChatMessage] = Field(default_factory=list)
    last_sql: Optional[str] = None
    last_schema: Optional[List[str]] = None  # 涉及的表名
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    def add_message(self, role: str, content: str, sql: Optional[str] = None, 
                    query_result: Optional[SQLResult] = None):
        """添加消息"""
        msg = ChatMessage(role=role, content=content, sql=sql, query_result=query_result)
        self.messages.append(msg)
        self.updated_at = datetime.now()
        
        if sql:
            self.last_sql = sql


class RetrievalResult(BaseModel):
    """检索结果"""
    content: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    score: float
    source: str  # schema, example, documentation
