"""
Data Agent Configuration
API密钥占位符 - 请在实际使用前填入真实密钥
"""
from dataclasses import dataclass, field
from typing import Optional
import os

@dataclass
class LLMConfig:
    """LLM配置"""
    api_key: str = "YOUR_OPENAI_API_KEY_HERE"  # 替换为真实API密钥
    base_url: str = "https://api.openai.com/v1"  # 可替换为其他兼容API
    model: str = "gpt-4o-mini"  # 或 gpt-4, gpt-3.5-turbo
    temperature: float = 0.1
    max_tokens: int = 2000
    
    @classmethod
    def from_env(cls):
        """从环境变量加载配置"""
        instance = cls()
        return cls(
            api_key=os.getenv("OPENAI_API_KEY", instance.api_key),
            base_url=os.getenv("OPENAI_BASE_URL", instance.base_url),
            model=os.getenv("OPENAI_MODEL", instance.model)
        )

@dataclass
class EmbeddingConfig:
    """嵌入模型配置"""
    api_key: str = "YOUR_OPENAI_API_KEY_HERE"  # 替换为真实API密钥
    base_url: str = "https://api.openai.com/v1"
    model: str = "text-embedding-3-small"  # 或 text-embedding-3-large, bge-large-zh
    dimension: int = 1536  # embedding维度
    
    @classmethod
    def from_env(cls):
        instance = cls()
        return cls(
            api_key=os.getenv("OPENAI_API_KEY", instance.api_key),
            base_url=os.getenv("OPENAI_BASE_URL", instance.base_url),
            model=os.getenv("EMBEDDING_MODEL", instance.model)
        )

@dataclass
class DatabaseConfig:
    """数据库配置"""
    db_type: str = "sqlite"  # sqlite, postgresql, mysql
    connection_string: str = "sqlite:///./test.db"
    # PostgreSQL: postgresql://user:password@host:port/dbname
    # MySQL: mysql://user:password@host:port/dbname

@dataclass
class VectorStoreConfig:
    """向量数据库配置"""
    persist_directory: str = "./vector_store"
    collection_name: str = "data_agent"

@dataclass
class AgentConfig:
    """Agent主配置"""
    llm: LLMConfig = field(default_factory=LLMConfig)
    embedding: EmbeddingConfig = field(default_factory=EmbeddingConfig)
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    vector_store: VectorStoreConfig = field(default_factory=VectorStoreConfig)
    
    # Agent参数
    max_retries: int = 3
    enable_sql_validation: bool = True
    enable_multi_turn: bool = True
    top_k_retrieval: int = 5
    similarity_threshold: float = 0.7
    
    @classmethod
    def from_env(cls):
        """从环境变量加载所有配置"""
        return cls(
            llm=LLMConfig.from_env(),
            embedding=EmbeddingConfig.from_env(),
            database=DatabaseConfig(
                db_type=os.getenv("DB_TYPE", "sqlite"),
                connection_string=os.getenv("DATABASE_URL", "sqlite:///./test.db")
            )
        )

# 全局配置实例
config = AgentConfig.from_env()
