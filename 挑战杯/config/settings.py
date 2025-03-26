from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    # 日志配置
    LOG_DIR: Path = Path("logs")
    
    # 应用基础配置
    APP_NAME: str = "AI Tutor"
    DEBUG: bool = True
    
    # 数据库配置
    DATABASE_URL: str = "sqlite+aiosqlite:///./tutor.db"
    
    # GPU配置
    CUDA_VERSION: str = "12.1"
    MAX_GPU_MEMORY: float = 0.8
    
    # 模型配置
    deepseek_api_key: str = "sk-3abb79fe54944d53aa06653b81733048"
    MODEL_NAME: str = "deepseek-ai/deepseek-math-7b-base"
    MODEL_PRECISION: str = "float16"#gpt改
    
    # 安全配置
    JWT_SECRET: str = "your-secret-key"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE: int = 30
    
    # 输入验证
    MAX_QUESTION_LENGTH: int = 500
    
    # 新增内存优化参数
    MODEL_OFFLOAD_FOLDER: str = "model_offload"
    USE_SAFETENSORS: bool = True
    LOW_CPU_MEM_USAGE: bool = True
    
    
    
    class Config:
        env_file = ".env"

settings = Settings()