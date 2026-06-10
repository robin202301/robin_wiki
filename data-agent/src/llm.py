"""
LLM Service
支持OpenAI兼容API（可切换任意兼容服务）
"""
import json
from typing import List, Dict, Any, Optional
from .config import LLMConfig


class LLMService:
    """LLM服务"""
    
    def __init__(self, config: LLMConfig):
        self.config = config
        self.client = None
        self._init_client()
    
    def _init_client(self):
        """初始化客户端"""
        try:
            from openai import OpenAI
            self.client = OpenAI(
                api_key=self.config.api_key,
                base_url=self.config.base_url
            )
        except ImportError:
            print("警告: openai包未安装，将使用模拟响应")
            self.client = None
    
    def chat(self, messages: List[Dict[str, str]], 
             temperature: Optional[float] = None,
             max_tokens: Optional[int] = None,
             response_format: Optional[Dict] = None) -> str:
        """发送聊天请求"""
        if self.client is None:
            return self._mock_response(messages)
        
        try:
            kwargs = {
                "model": self.config.model,
                "messages": messages,
                "temperature": temperature or self.config.temperature,
                "max_tokens": max_tokens or self.config.max_tokens,
            }
            
            if response_format:
                kwargs["response_format"] = response_format
            
            response = self.client.chat.completions.create(**kwargs)
            return response.choices[0].message.content
        except Exception as e:
            print(f"LLM调用失败: {e}")
            return self._mock_response(messages)
    
    def chat_json(self, messages: List[Dict[str, str]], 
                  temperature: Optional[float] = None) -> Dict[str, Any]:
        """发送聊天请求并解析JSON响应"""
        response = self.chat(
            messages, 
            temperature=temperature,
            response_format={"type": "json_object"}
        )
        try:
            return json.loads(response)
        except json.JSONDecodeError as e:
            print(f"JSON解析失败: {e}")
            return {"error": f"JSON解析失败: {e}", "raw": response}
    
    def _mock_response(self, messages: List[Dict[str, str]]) -> str:
        """模拟响应（用于测试）"""
        # 解析最后一条用户消息，返回模拟SQL
        last_msg = messages[-1]["content"] if messages else ""
        
        # 简单的关键词匹配
        if "总数" in last_msg or "多少" in last_msg or "count" in last_msg.lower():
            return '{"sql": "SELECT COUNT(*) as total FROM table_name", "explanation": "统计总数"}'
        elif "平均" in last_msg or "average" in last_msg.lower():
            return '{"sql": "SELECT AVG(amount) as avg_value FROM orders", "explanation": "计算平均值"}'
        elif "最大" in last_msg or "最高" in last_msg.lower():
            return '{"sql": "SELECT MAX(amount) as max_value FROM orders", "explanation": "查找最大值"}'
        else:
            return '{"sql": "SELECT * FROM table_name LIMIT 10", "explanation": "查询数据"}'
