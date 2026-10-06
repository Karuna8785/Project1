"""
SmartERP Backend - Application Configuration
Unified Enterprise Platform Configuration
"""
from typing import List
from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    PROJECT_NAME: str = "SmartERP"
    APP_NAME: str = "SmartERP"
    VERSION: str = "1.0.0"
    APP_VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = True

    # Security / JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "smarterp-super-secret-key-change-in-production-2026-secure-jwt")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours

    # Database: SQLite default for local zero-config, PostgreSQL in production
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./smarterp.db")

    # CORS
    ALLOWED_ORIGINS: str = "http://localhost:5173,http://localhost:3000,http://127.0.0.1:5173,http://127.0.0.1:3000"
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

    # Module Flags
    HR_MODULE_ENABLED: bool = True
    SALES_MODULE_ENABLED: bool = True
    INVENTORY_MODULE_ENABLED: bool = True

    @property
    def allowed_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]

    model_config = {
        "case_sensitive": True,
        "env_file": ".env",
        "extra": "ignore",
    }


settings = Settings()
