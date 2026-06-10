"""
Vector Store Service
基于ChromaDB的向量存储
"""
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings
from .config import VectorStoreConfig
from .models import RetrievalResult
from .embedding import EmbeddingService


class VectorStore:
    """向量数据库服务"""
    
    def __init__(self, config: VectorStoreConfig, embedding_service: EmbeddingService):
        self.config = config
        self.embedding_service = embedding_service
        
        # 初始化ChromaDB客户端
        self.client = chromadb.Client(Settings(
            persist_directory=config.persist_directory,
            anonymized_telemetry=False
        ))
        
        # 创建或获取集合
        self.collection = self.client.get_or_create_collection(
            name=config.collection_name,
            metadata={"hnsw:space": "cosine"}  # 使用余弦相似度
        )
    
    def add_schema(self, table_name: str, ddl: str, metadata: Optional[Dict] = None):
        """添加表schema到向量库"""
        doc_id = f"schema_{table_name}"
        
        # 生成嵌入
        embedding = self.embedding_service.embed_text(ddl)
        
        # 准备元数据
        meta = metadata or {}
        meta.update({
            "type": "schema",
            "table_name": table_name,
            "content_type": "ddl"
        })
        
        # 添加到集合
        self.collection.upsert(
            ids=[doc_id],
            embeddings=[embedding],
            documents=[ddl],
            metadatas=[meta]
        )
    
    def add_example(self, question: str, sql: str, explanation: str = "", 
                    metadata: Optional[Dict] = None):
        """添加示例问答对"""
        doc_id = f"example_{hash(question) % 1000000}"
        
        # 组合文档内容
        content = f"问题: {question}\nSQL: {sql}"
        if explanation:
            content += f"\n解释: {explanation}"
        
        # 生成嵌入（基于问题）
        embedding = self.embedding_service.embed_text(question)
        
        # 准备元数据
        meta = metadata or {}
        meta.update({
            "type": "example",
            "question": question,
            "sql": sql,
            "content_type": "qa_pair"
        })
        
        # 添加到集合
        self.collection.upsert(
            ids=[doc_id],
            embeddings=[embedding],
            documents=[content],
            metadatas=[meta]
        )
    
    def add_documentation(self, title: str, content: str, 
                         metadata: Optional[Dict] = None):
        """添加文档知识"""
        doc_id = f"doc_{hash(title) % 1000000}"
        
        # 生成嵌入
        embedding = self.embedding_service.embed_text(f"{title}\n{content}")
        
        # 准备元数据
        meta = metadata or {}
        meta.update({
            "type": "documentation",
            "title": title,
            "content_type": "doc"
        })
        
        # 添加到集合
        self.collection.upsert(
            ids=[doc_id],
            embeddings=[embedding],
            documents=content,
            metadatas=[meta]
        )
    
    def search(self, query: str, top_k: int = 5, 
               filter_type: Optional[str] = None,
               threshold: float = 0.0) -> List[RetrievalResult]:
        """搜索相关内容"""
        # 生成查询嵌入
        query_embedding = self.embedding_service.embed_text(query)
        
        # 准备过滤条件
        where_filter = None
        if filter_type:
            where_filter = {"type": filter_type}
        
        # 执行搜索
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where_filter,
            include=["documents", "metadatas", "distances"]
        )
        
        # 转换结果
        retrieval_results = []
        for i, (doc, meta, distance) in enumerate(zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0]
        )):
            # ChromaDB返回距离，转换为相似度（假设余弦距离）
            score = 1 - distance  # cosine distance to similarity
            
            if score >= threshold:
                retrieval_results.append(RetrievalResult(
                    content=doc,
                    metadata=meta,
                    score=score,
                    source=meta.get("type", "unknown")
                ))
        
        return retrieval_results
    
    def search_schemas(self, query: str, top_k: int = 5) -> List[RetrievalResult]:
        """搜索相关schema"""
        return self.search(query, top_k=top_k, filter_type="schema")
    
    def search_examples(self, query: str, top_k: int = 3) -> List[RetrievalResult]:
        """搜索相关示例"""
        return self.search(query, top_k=top_k, filter_type="example")
    
    def search_documentation(self, query: str, top_k: int = 3) -> List[RetrievalResult]:
        """搜索相关文档"""
        return self.search(query, top_k=top_k, filter_type="documentation")
    
    def delete_by_id(self, doc_id: str):
        """删除指定文档"""
        self.collection.delete(ids=[doc_id])
    
    def delete_by_type(self, doc_type: str):
        """删除指定类型的所有文档"""
        # ChromaDB不直接支持按metadata删除，需要查询后逐个删除
        results = self.collection.get(where={"type": doc_type})
        if results["ids"]:
            self.collection.delete(ids=results["ids"])
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            "total_documents": self.collection.count(),
            "collection_name": self.config.collection_name,
            "persist_directory": self.config.persist_directory
        }
    
    def clear_all(self):
        """清空所有数据"""
        self.client.delete_collection(self.config.collection_name)
        self.collection = self.client.get_or_create_collection(
            name=self.config.collection_name,
            metadata={"hnsw:space": "cosine"}
        )
