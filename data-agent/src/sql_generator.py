"""
SQL Generator
Text2SQL核心生成逻辑
"""
from typing import List, Dict, Any, Optional
from .models import SchemaInfo, RetrievalResult, ConversationContext
from .vector_store import VectorStore
from .llm import LLMService
from .prompts import (
    SYSTEM_PROMPT, SQL_GENERATION_PROMPT, SQL_REPAIR_PROMPT,
    QUERY_CLARIFICATION_PROMPT, MULTI_TURN_CONTEXT_PROMPT
)
import json
import re


class SQLGenerator:
    """SQL生成器"""
    
    def __init__(self, llm_service: LLMService, vector_store: VectorStore):
        self.llm = llm_service
        self.vector_store = vector_store
    
    def generate_sql(self, question: str, schema: SchemaInfo,
                     context: Optional[ConversationContext] = None) -> Dict[str, Any]:
        """生成SQL"""
        
        # 1. 检索相关schema
        schema_results = self.vector_store.search_schemas(question, top_k=5)
        
        # 2. 检索相关示例
        example_results = self.vector_store.search_examples(question, top_k=3)
        
        # 3. 构建schema文本
        schema_text = self._build_schema_text(schema, schema_results)
        
        # 4. 构建示例文本
        examples_text = self._build_examples_text(example_results)
        
        # 5. 构建消息
        if context and len(context.messages) > 2:
            # 多轮对话
            prompt = MULTI_TURN_CONTEXT_PROMPT.format(
                history=self._format_history(context),
                question=question,
                schema=schema_text
            )
        else:
            # 单轮对话
            prompt = SQL_GENERATION_PROMPT.format(
                schema=schema_text,
                examples=examples_text,
                question=question
            )
        
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]
        
        # 6. 调用LLM
        response = self.llm.chat_json(messages)
        
        return response
    
    def repair_sql(self, original_sql: str, error_message: str,
                   question: str, schema: SchemaInfo) -> Dict[str, Any]:
        """修复SQL错误"""
        
        schema_text = schema.to_ddl()
        
        prompt = SQL_REPAIR_PROMPT.format(
            schema=schema_text,
            original_sql=original_sql,
            error_message=error_message,
            question=question
        )
        
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]
        
        return self.llm.chat_json(messages)
    
    def clarify_query(self, question: str, schema: SchemaInfo) -> Dict[str, Any]:
        """分析查询是否需要澄清"""
        
        schema_text = schema.to_ddl()
        
        prompt = QUERY_CLARIFICATION_PROMPT.format(
            schema=schema_text,
            question=question
        )
        
        messages = [
            {"role": "system", "content": "你是一个SQL查询分析专家。"},
            {"role": "user", "content": prompt}
        ]
        
        return self.llm.chat_json(messages)
    
    def generate_with_retry(self, question: str, schema: SchemaInfo,
                            context: Optional[ConversationContext] = None,
                            max_retries: int = 3) -> Dict[str, Any]:
        """带重试的SQL生成"""
        
        result = self.generate_sql(question, schema, context)
        
        # 检查是否需要重试
        retry_count = 0
        while result.get("error") and retry_count < max_retries:
            # 如果是需要澄清，直接返回
            if result.get("clarification"):
                return result
            
            # 尝试修复
            if result.get("sql"):
                result = self.repair_sql(
                    result["sql"],
                    result.get("error", "未知错误"),
                    question,
                    schema
                )
            else:
                result = self.generate_sql(question, schema, context)
            
            retry_count += 1
        
        return result
    
    def _build_schema_text(self, schema: SchemaInfo, 
                           schema_results: List[RetrievalResult]) -> str:
        """构建schema文本"""
        
        if schema_results:
            # 使用检索到的相关schema
            parts = []
            for result in schema_results:
                parts.append(result.content)
                if result.metadata.get("comment"):
                    parts.append(f"-- 说明: {result.metadata['comment']}")
            return "\n\n".join(parts)
        else:
            # 使用完整schema
            return schema.to_ddl()
    
    def _build_examples_text(self, example_results: List[RetrievalResult]) -> str:
        """构建示例文本"""
        
        if not example_results:
            return "（暂无相关示例）"
        
        parts = []
        for i, result in enumerate(example_results, 1):
            parts.append(f"### 示例{i}")
            parts.append(result.content)
            parts.append("")
        
        return "\n".join(parts)
    
    def _format_history(self, context: ConversationContext) -> str:
        """格式化对话历史"""
        
        parts = []
        # 只取最近5轮对话
        recent_messages = context.messages[-10:]
        
        for msg in recent_messages:
            role = "用户" if msg.role == "user" else "助手"
            parts.append(f"**{role}**: {msg.content}")
            if msg.sql:
                parts.append(f"```sql\n{msg.sql}\n```")
        
        return "\n\n".join(parts)
    
    def extract_sql_from_response(self, response: str) -> Optional[str]:
        """从响应文本中提取SQL"""
        
        # 尝试从JSON中提取
        try:
            data = json.loads(response)
            if "sql" in data:
                return data["sql"]
        except json.JSONDecodeError:
            pass
        
        # 尝试从markdown代码块中提取
        sql_pattern = r'```sql\s*\n(.*?)\n```'
        match = re.search(sql_pattern, response, re.DOTALL)
        if match:
            return match.group(1).strip()
        
        # 尝试直接提取SELECT语句
        select_pattern = r'(SELECT\s+.*?(?:;|$))'
        match = re.search(select_pattern, response, re.IGNORECASE | re.DOTALL)
        if match:
            return match.group(1).strip()
        
        return None
