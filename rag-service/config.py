import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration settings"""
    
    # Server configuration
    python_port: int = 8000
    python_env: str = "development"
    
    # Pinecone configuration
    pinecone_api_key: str
    pinecone_cloud: str = "aws"
    pinecone_region: str = "us-east-1"
    pinecone_index_name: str = "financial-docs"
    
    # OpenAI configuration
    openai_api_key: str
    openai_model: str = "gpt-3.5-turbo"
    openai_embedding_model: str = "text-embedding-3-small"
    
    # RAG configuration
    top_k: int = 5
    max_tokens: int = 500
    temperature: float = 0.7
    chunk_size: int = 1000
    chunk_overlap: int = 200
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
