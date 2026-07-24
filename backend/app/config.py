import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "IntelliWealth Financial Intelligence Agent"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "super-secret-key-intelliwealth-jwt-change-in-production-2026"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # Database
    DATABASE_URL: str = "sqlite:///./intelliwealth.db"

    # AI Keys (Optional - fallback engine used if absent)
    GEMINI_API_KEY: str = ""
    OPENAI_API_KEY: str = ""

    # Bank Integration Settings
    BANK_SYNC_INTERVAL_MINUTES: int = 15

    class Config:
        case_sensitive = True
        env_file = ".env"
        extra = "ignore"

settings = Settings()
