from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "SmartERP API"
    api_v1_prefix: str = "/api/v1"
    database_url: str = "sqlite:///./smarterp_dev.db"
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    backend_cors_origins: list[str] = ["http://localhost:5173"]
    admin_email: str = "admin@example.com"
    admin_username: str = "admin"
    admin_full_name: str = "ERP Administrator"
    admin_password: str = ""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @field_validator("backend_cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: object) -> object:
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value

    @field_validator("secret_key")
    @classmethod
    def validate_secret_key(cls, value: str) -> str:
        lowered = value.lower()
        if len(value) < 32 or "replace-with-" in lowered or "change-this" in lowered:
            raise ValueError("SECRET_KEY must be at least 32 characters and must not be a placeholder")
        return value

    @field_validator("database_url")
    @classmethod
    def validate_database_url(cls, value: str) -> str:
        if not value.startswith("sqlite:"):
            raise ValueError("This project is configured to use SQLite; set DATABASE_URL to a sqlite:/// URL")
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
