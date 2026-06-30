"""Configuration management"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database
    database_url: str = "sqlite:///./selection_agent.db"
    
    # LLM API (OpenAI-compatible)
    llm_api_base: str = "https://api.openai.com/v1"
    llm_api_key: str = ""
    llm_model: str = "gpt-4o-mini"
    
    # App settings
    app_name: str = "跨境电商选品Agent"
    app_version: str = "0.1.0"
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Market configurations
    default_markets: list[str] = ["泰国", "越南", "菲律宾", "马来西亚", "印尼", "俄罗斯"]
    default_platforms: list[str] = ["TikTok Shop", "Shopee", "Lazada", "速卖通"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
