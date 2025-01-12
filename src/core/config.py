from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional, Dict, Any, List, Tuple
import secrets
from pathlib import Path


class Settings(BaseSettings):
    # API Settings
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "Heddy Backend"
    DEBUG: bool = False
    VERSION: str = "1.0.0"
    # CORS Settings
    BACKEND_CORS_ORIGINS: str = "http://localhost:3000,\
                                 http://localhost:8000,\
                                 http://localhost:5173"

    # MongoDB
    MONGO_HOST: str = "localhost"
    MONGO_PORT: str = "27017"
    MONGO_DB: str = "heddy"
    MONGO_USER: Optional[str] = None
    MONGO_PASSWORD: Optional[str] = None
    DATABASE_URL: Optional[str] = None

    # JWT Token Settings
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ALGORITHM: str = "HS256"

    # Email Settings (if needed)
    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = 587
    # SMTP_PORT: Optional[int] = 465
    SMTP_HOST: Optional[str] = "smtp.gmail.com"
    SMTP_USER: Optional[str] = "kzsc5464@gmail.com"
    SMTP_PASSWORD: Optional[str] = "jayjvoqotaocyowp"
    EMAILS_FROM_EMAIL: Optional[str] = "kzsc5464@gmail.com"
    EMAILS_FROM_NAME: Optional[str] = "Heddy"

    # Cache Settings
    REDIS_HOST: Optional[str] = "localhost"
    REDIS_PORT: Optional[int] = 6379
    REDIS_PASSWORD: Optional[str] = None

    # File Storage
    UPLOAD_DIR: Path = Path("uploads")
    MAX_UPLOAD_SIZE: int = 5_242_880  # 5MB in bytes
    ALLOWED_FILE_TYPES: Tuple[str, ...] = ("image/jpeg", "image/png", "application/pdf")

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"

    class Config:
        env_file = ".env"
        case_sensitive = True

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        # Construct Database URL if not provided
        if not self.DATABASE_URL:
            # MongoDB 인증이 필요한 경우
            if self.MONGO_USER and self.MONGO_PASSWORD:
                self.DATABASE_URL = (
                    f"mongodb://{self.MONGO_USER}:{self.MONGO_PASSWORD}"
                    f"@{self.MONGO_HOST}:{self.MONGO_PORT}/{self.MONGO_DB}"
                )
            else:
                # 인증이 필요없는 로컬 개발 환경
                self.DATABASE_URL = (
                    f"mongodb://{self.MONGO_HOST}:{self.MONGO_PORT}/{self.MONGO_DB}"
                )

    @property
    def cors_origins(self) -> List[str]:
        """CORS origins as list"""
        return [origin.strip() for origin in self.BACKEND_CORS_ORIGINS.split(",")]

    @property
    def fastapi_kwargs(self) -> Dict[str, Any]:
        """
        FastAPI configuration settings
        """
        return {
            "title": self.PROJECT_NAME,
            "version": self.VERSION,
            "debug": self.DEBUG,
            "openapi_url": f"{self.API_V1_PREFIX}/openapi.json",
            "docs_url": "/docs",
            "redoc_url": "/redoc",
        }


@lru_cache()
def get_settings() -> Settings:
    """
    Create cached instance of settings
    """
    return Settings()


# Create a settings instance
settings = get_settings()
