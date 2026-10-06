import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "SmartERP"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "postgresql+psycopg2://postgres:postgres@localhost:5432/smarterp"
    )
    # Fallback to local SQLite if PostgreSQL is unreachable during offline dev/testing
    SQLITE_FALLBACK_URL: str = "sqlite:///./smarterp.db"
    
    # Security / JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "smarterp-super-secret-production-grade-jwt-key-2026")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours

    model_config = SettingsConfigDict(env_file=".env", extra="allow")

settings = Settings()
