import os
import secrets
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator

class Settings(BaseSettings):
    PROJECT_NAME: str = "Learning Management System (LMS)"
    VERSION: str = "1.1.0"
    API_V1_STR: str = "/api"

    DATABASE_URL: str = "mysql+pymysql://root:root@localhost:3306/lms_db?charset=utf8mb4"
    TEST_DATABASE_URL: str = "sqlite:///./test_lms.db"

    # JWT Authentication - MUST be provided via environment variable. No hardcoded default permitted.
    JWT_SECRET: str = ""
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 Hours

    UPLOAD_DIR: str = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "uploads")
    MAX_UPLOAD_SIZE_MB: int = 50

    # Object Storage: "local" | "s3"
    STORAGE_BACKEND: str = "local"
    S3_BUCKET: str = ""
    S3_REGION: str = "us-east-1"
    S3_ENDPOINT_URL: str = ""
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    S3_PUBLIC_BASE_URL: str = ""

    # SMTP Email Configuration
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    FROM_EMAIL: str = "noreply@lms-institute.edu"
    FRONTEND_URL: str = "https://lms-fullstack-vibe.netlify.app"

    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "https://lms-fullstack-vibe.netlify.app",
    ]

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"),
        extra="allow",
        case_sensitive=True
    )

    @field_validator("JWT_SECRET", mode="before")
    @classmethod
    def validate_jwt_secret(cls, v):
        secret = v or os.getenv("JWT_SECRET") or os.getenv("SECRET_KEY")
        # Explicitly check for absence or legacy exposed default in git history
        if not secret or secret == "REDACTED_LEGACY_JWT_SECRET":
            raise RuntimeError(
                "CRITICAL SECURITY CONFIGURATION ERROR: JWT_SECRET environment variable is missing or using an insecure legacy default. "
                "Application startup aborted. Please provide a cryptographically secure 256-bit secret key in your environment or .env file."
            )
        return secret

settings = Settings()
