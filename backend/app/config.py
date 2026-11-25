import hashlib
import os
import secrets
from typing import List, Union
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator

class Settings(BaseSettings):
    PROJECT_NAME: str = "Learning Management System (LMS)"
    VERSION: str = "1.1.0"
    API_V1_STR: str = "/api"
    DEBUG: bool = False

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
    FRONTEND_URL: str = "https://lms-fullstack-platform.netlify.app"

    CORS_ORIGINS: Union[List[str], str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://lms-fullstack-platform.netlify.app",
    ]

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str):
            if v.startswith("[") and v.endswith("]"):
                import json
                try:
                    return json.loads(v)
                except Exception:
                    pass
            return [i.strip() for i in v.split(",") if i.strip()]
        elif isinstance(v, (list, tuple)):
            return list(v)
        return []

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"),
        extra="allow",
        case_sensitive=True
    )

    @field_validator("JWT_SECRET", mode="before")
    @classmethod
    def validate_jwt_secret(cls, v):
        secret = v or os.getenv("JWT_SECRET") or os.getenv("SECRET_KEY")
        # Explicitly check for absence or legacy exposed default via SHA-256 hash
        legacy_hash = "32d1545f1d494f5148c6fd7a27595589149eae8c79f33efbcc2dae2c1affe48b"
        if not secret or hashlib.sha256(secret.encode("utf-8")).hexdigest() == legacy_hash:
            raise RuntimeError(
                "CRITICAL SECURITY CONFIGURATION ERROR: JWT_SECRET environment variable is missing or using an insecure legacy default. "
                "Application startup aborted. Please provide a cryptographically secure 256-bit secret key in your environment or .env file."
            )
        return secret

settings = Settings()
