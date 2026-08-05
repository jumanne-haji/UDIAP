"""
UDIAP Core Configuration
Centralized settings for the Universal Decision Intelligence Assessment Platform.
Supports both PostgreSQL (production) and SQLite (Termux / mobile).
"""

from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List, Optional
import os


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "UDIAP"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    API_PREFIX: str = "/api"

    # Security
    SECRET_KEY: str = "udiap-super-secret-key-change-in-production-2026"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Database – default to SQLite for easy Termux / mobile use
    # For PostgreSQL set: DATABASE_URL=postgresql+asyncpg://user:pass@host/db
    DATABASE_URL: str = "sqlite+aiosqlite:///./udiap.db"

    def model_post_init(self, __context) -> None:
        # Hosts like Render/Railway/Neon inject DATABASE_URL as
        # "postgres://..." or "postgresql://..." (sync form). The async
        # engine needs the +asyncpg driver, so normalize it here.
        url = self.DATABASE_URL
        if url.startswith("postgres://"):
            self.DATABASE_URL = url.replace("postgres://", "postgresql+asyncpg://", 1)
        elif url.startswith("postgresql://"):
            self.DATABASE_URL = url.replace("postgresql://", "postgresql+asyncpg://", 1)

    # CORS – allow Termux localhost and common mobile origins
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "*",
    ]

    # Scoring Weights (HDPM + COE)
    CONTENT_SCORE_WEIGHT: float = 0.60
    PROCESS_SCORE_WEIGHT: float = 0.40

    # Cognitive thresholds
    TYPING_SPEED_NORMAL_MIN: float = 30.0
    TYPING_SPEED_NORMAL_MAX: float = 80.0
    PAUSE_THRESHOLD_MS: int = 2000
    REVISION_QUALITY_THRESHOLD: int = 3

    # AI / LLM (placeholder)
    OPENAI_API_KEY: Optional[str] = None
    LLM_MODEL: str = "gpt-4o-mini"

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
