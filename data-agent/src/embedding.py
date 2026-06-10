"""
Embedding Service
支持OpenAI、本地模型等多种嵌入方式
"""
import asyncio
from typing import List, Optional
import numpy as np
from .config import EmbeddingConfig


class EmbeddingService:
    """嵌入服务"""
    
    def __init__(self, config: EmbeddingConfig):
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
            print("警告: openai包未安装，将使用模拟嵌入")
            self.client = None
    
    def embed_text(self, text: str) -> List[float]:
        """嵌入单个文本"""
        if self.client is None:
            # 模拟嵌入（仅用于测试）
            return self._mock_embed(text)
        
        try:
            response = self.client.embeddings.create(
                model=self.config.model,
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"嵌入失败: {e}")
            return self._mock_embed(text)
    
    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """批量嵌入文本"""
        if not texts:
            return []
        
        if self.client is None:
            return [self._mock_embed(text) for text in texts]
        
        try:
            response = self.client.embeddings.create(
                model=self.config.model,
                input=texts
            )
            return [item.embedding for item in response.data]
        except Exception as e:
            print(f"批量嵌入失败: {e}")
            return [self._mock_embed(text) for text in texts]
    
    def _mock_embed(self, text: str) -> List[float]:
        """模拟嵌入（用于测试）"""
        # 基于文本hash生成伪向量
        hash_val = hash(text) % (2**32)
        np.random.seed(hash_val)
        vector = np.random.randn(self.config.dimension).astype(np.float32)
        # 归一化
        vector = vector / np.linalg.norm(vector)
        return vector.tolist()
    
    async def async_embed_text(self, text: str) -> List[float]:
        """异步嵌入单个文本"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.embed_text, text)
    
    async def async_embed_texts(self, texts: List[str]) -> List[List[float]]:
        """异步批量嵌入"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.embed_texts, texts)


def cosine_similarity(a: List[float], b: List[float]) -> float:
    """计算余弦相似度"""
    a_arr = np.array(a)
    b_arr = np.array(b)
    return float(np.dot(a_arr, b_arr) / (np.linalg.norm(a_arr) * np.linalg.norm(b_arr)))


def batch_cosine_similarity(query_vec: List[float], doc_vecs: List[List[float]]) -> List[float]:
    """批量计算余弦相似度"""
    query_arr = np.array(query_vec)
    docs_arr = np.array(doc_vecs)
    
    # 归一化
    query_norm = query_arr / np.linalg.norm(query_arr)
    docs_norm = docs_arr / np.linalg.norm(docs_arr, axis=1, keepdims=True)
    
    # 计算相似度
    similarities = np.dot(docs_norm, query_norm)
    return similarities.tolist()
