"""
Data Agent - 数据领域智能Agent
整合RAG、Embedding、VectorDB、Text2SQL的完整Agent
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid

from .config import AgentConfig
from .models import (
    SchemaInfo, SQLResult, ConversationContext, 
    ChatMessage, RetrievalResult
)
from .embedding import EmbeddingService
from .vector_store import VectorStore
from .llm import LLMService
from .schema_loader import SchemaLoader
from .sql_generator import SQLGenerator
from .sql_executor import SQLExecutor
from .prompts import RESULT_INTERPRETATION_PROMPT, SYSTEM_PROMPT
from .utils import extract_table_names, sql_to_natural_language


class DataAgent:
    """数据领域Agent
    
    功能：
    - 自然语言转SQL (Text2SQL)
    - 数据分析与查询
    - RAG增强的schema理解
    - 多轮对话支持
    - SQL安全执行
    - 结果解读
    """
    
    def __init__(self, config: Optional[AgentConfig] = None):
        self.config = config or AgentConfig()
        
        # 初始化服务
        self.embedding_service = EmbeddingService(self.config.embedding)
        self.vector_store = VectorStore(self.config.vector_store, self.embedding_service)
        self.llm_service = LLMService(self.config.llm)
        self.schema_loader = SchemaLoader(self.config.database)
        self.sql_generator = SQLGenerator(self.llm_service, self.vector_store)
        self.sql_executor = SQLExecutor(self.config.database)
        
        # 当前schema
        self.current_schema: Optional[SchemaInfo] = None
        
        # 对话上下文管理
        self.conversations: Dict[str, ConversationContext] = {}
    
    # ==================== Schema管理 ====================
    
    def load_schema_from_ddl(self, ddl_text: str):
        """从DDL加载schema"""
        self.current_schema = self.schema_loader.load_from_ddl(ddl_text)
        self._index_schema()
        return self.current_schema
    
    def load_schema_from_file(self, file_path: str):
        """从DDL文件加载schema"""
        self.current_schema = self.schema_loader.load_from_ddl_file(file_path)
        self._index_schema()
        return self.current_schema
    
    def load_schema_from_database(self, schemas: Optional[List[str]] = None):
        """从数据库加载schema"""
        self.current_schema = self.schema_loader.load_from_database(schemas)
        self._index_schema()
        return self.current_schema
    
    def load_schema_from_dict(self, schema_dict: Dict[str, Any]):
        """从字典加载schema（测试用）"""
        self.current_schema = self.schema_loader.load_from_dict(schema_dict)
        self._index_schema()
        return self.current_schema
    
    def _index_schema(self):
        """将schema索引到向量库"""
        if not self.current_schema:
            return
        
        for table in self.current_schema.tables:
            ddl = table.to_ddl()
            metadata = {
                "comment": table.comment,
                "row_count": table.row_count,
                "columns": [c.name for c in table.columns]
            }
            self.vector_store.add_schema(table.name, ddl, metadata)
    
    # ==================== 示例管理 ====================
    
    def add_example(self, question: str, sql: str, explanation: str = ""):
        """添加问答示例（用于few-shot）"""
        self.vector_store.add_example(question, sql, explanation)
    
    def add_examples_batch(self, examples: List[Dict[str, str]]):
        """批量添加示例"""
        for ex in examples:
            self.add_example(
                ex["question"],
                ex["sql"],
                ex.get("explanation", "")
            )
    
    # ==================== 文档管理 ====================
    
    def add_documentation(self, title: str, content: str):
        """添加业务文档"""
        self.vector_store.add_documentation(title, content)
    
    # ==================== 查询处理 ====================
    
    def ask(self, question: str, session_id: Optional[str] = None) -> Dict[str, Any]:
        """
        处理用户问题
        
        流程:
        1. 分析问题类型
        2. 检索相关schema和示例 (RAG)
        3. 生成SQL
        4. 验证SQL
        5. 执行SQL
        6. 解读结果
        """
        
        # 获取或创建对话上下文
        context = self._get_context(session_id)
        
        # 添加用户消息
        context.add_message("user", question)
        
        # 检查schema是否已加载
        if not self.current_schema:
            return {
                "success": False,
                "error": "尚未加载数据库schema，请先调用 load_schema_*",
                "type": "setup_required"
            }
        
        # Step 1: 分析问题类型
        query_type = self._classify_question(question)
        
        # Step 2: 生成SQL
        sql_response = self.sql_generator.generate_with_retry(
            question=question,
            schema=self.current_schema,
            context=context,
            max_retries=self.config.max_retries
        )
        
        # 检查是否需要澄清
        if sql_response.get("clarification"):
            result = {
                "success": True,
                "type": "clarification_needed",
                "question": question,
                "interpretation": sql_response.get("interpretation", ""),
                "clarification": sql_response["clarification"],
                "sql": sql_response.get("suggested_sql"),
                "ambiguities": sql_response.get("ambiguities", [])
            }
            context.add_message("assistant", sql_response["clarification"])
            return result
        
        # 检查SQL是否生成成功
        sql = sql_response.get("sql")
        if not sql:
            result = {
                "success": False,
                "type": "generation_failed",
                "question": question,
                "error": sql_response.get("error", "无法生成SQL"),
                "explanation": sql_response.get("explanation", "")
            }
            context.add_message("assistant", result["error"])
            return result
        
        # Step 3: 执行SQL
        sql_result = self.sql_executor.execute(sql)
        
        # Step 4: 如果执行失败，尝试修复
        if not sql_result.success and self.config.enable_sql_validation:
            repair_response = self.sql_generator.repair_sql(
                original_sql=sql,
                error_message=sql_result.error,
                question=question,
                schema=self.current_schema
            )
            
            repaired_sql = repair_response.get("sql")
            if repaired_sql and repaired_sql != sql:
                sql_result = self.sql_executor.execute(repaired_sql)
                if sql_result.success:
                    sql = repaired_sql
                    sql_response["fix_applied"] = repair_response.get("fix_explanation")
        
        # Step 5: 解读结果
        interpretation = self._interpret_result(question, sql, sql_result)
        
        # 构建返回结果
        result = {
            "success": sql_result.success,
            "type": query_type,
            "question": question,
            "sql": sql,
            "sql_result": sql_result,
            "explanation": sql_response.get("explanation", ""),
            "interpretation": interpretation,
            "tables_used": sql_response.get("tables_used", extract_table_names(sql)),
            "confidence": sql_response.get("confidence", "unknown"),
            "execution_time_ms": sql_result.execution_time_ms,
            "assumptions": sql_response.get("assumptions", [])
        }
        
        # 更新上下文
        context.add_message("assistant", interpretation or "", sql=sql, query_result=sql_result)
        
        return result
    
    def execute_sql(self, sql: str) -> SQLResult:
        """直接执行SQL"""
        return self.sql_executor.execute(sql)
    
    def get_schema_info(self) -> Optional[str]:
        """获取当前schema的DDL文本"""
        if self.current_schema:
            return self.current_schema.to_ddl()
        return None
    
    def search_knowledge(self, query: str, top_k: int = 5) -> List[RetrievalResult]:
        """搜索知识库"""
        return self.vector_store.search(query, top_k=top_k)
    
    # ==================== 对话管理 ====================
    
    def _get_context(self, session_id: Optional[str] = None) -> ConversationContext:
        """获取对话上下文"""
        if session_id and session_id in self.conversations:
            return self.conversations[session_id]
        
        sid = session_id or str(uuid.uuid4())
        context = ConversationContext(session_id=sid)
        self.conversations[sid] = context
        return context
    
    def get_conversation_history(self, session_id: str) -> List[ChatMessage]:
        """获取对话历史"""
        if session_id in self.conversations:
            return self.conversations[session_id].messages
        return []
    
    def clear_conversation(self, session_id: str):
        """清除对话历史"""
        if session_id in self.conversations:
            del self.conversations[session_id]
    
    # ==================== 内部方法 ====================
    
    def _classify_question(self, question: str) -> str:
        """简单分类问题类型"""
        q = question.lower()
        
        if any(kw in q for kw in ["多少", "几个", "总数", "数量", "count", "有多少"]):
            return "count"
        elif any(kw in q for kw in ["平均", "均值", "avg", "average"]):
            return "aggregation"
        elif any(kw in q for kw in ["最大", "最高", "最多", "top", "max"]):
            return "ranking"
        elif any(kw in q for kw in ["趋势", "变化", "对比", "比较", "同比", "环比"]):
            return "comparison"
        elif any(kw in q for kw in ["为什么", "原因", "分析", "为什么"]):
            return "analysis"
        elif any(kw in q for kw in ["查询", "列出", "显示", "查看", "哪些", "什么"]):
            return "query"
        else:
            return "general"
    
    def _interpret_result(self, question: str, sql: str, 
                          sql_result: SQLResult) -> str:
        """解读查询结果"""
        
        if not sql_result.success:
            return f"查询执行失败: {sql_result.error}"
        
        if not sql_result.data:
            return "查询成功但未返回数据。可能需要调整查询条件。"
        
        # 对于简单结果直接用自然语言描述
        if sql_result.row_count == 1 and len(sql_result.columns) == 1:
            value = sql_result.data[0][sql_result.columns[0]]
            return f"查询结果: {value}"
        
        # 对于少量结果，直接返回Markdown表格
        if sql_result.row_count <= 20:
            return sql_result.to_markdown()
        
        # 对于大量结果，用LLM总结
        try:
            prompt = RESULT_INTERPRETATION_PROMPT.format(
                question=question,
                sql=sql,
                result_data=str(sql_result.data[:10])
            )
            
            messages = [
                {"role": "system", "content": "你是数据分析专家，请用简洁的中文解读查询结果。"},
                {"role": "user", "content": prompt}
            ]
            
            return self.llm_service.chat(messages, max_tokens=500)
        except Exception:
            return sql_result.to_markdown()
    
    # ==================== 生命周期 ====================
    
    def close(self):
        """关闭Agent，释放资源"""
        self.sql_executor.close()
    
    def get_stats(self) -> Dict[str, Any]:
        """获取Agent统计信息"""
        return {
            "vector_store": self.vector_store.get_stats(),
            "schema_tables": len(self.current_schema.tables) if self.current_schema else 0,
            "active_conversations": len(self.conversations)
        }
