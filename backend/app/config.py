import os
from typing import List, Union
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator

class Settings(BaseSettings):
    PROJECT_NAME: str = "Learning Management System (LMS)"
    VERSION: str = "1.1.0"
    API_V1_STR: str = "/api"

    DATABASE_URL: str = "mysql+pymysql://root:root@localhost:3306/lms_db?charset=utf8mb4"
    TEST_DATABASE_URL: str = "mysql+pymysql://root:root@localhost:3306/lms_test_db?charset=utf8mb4"

    JWT_SECRET: str = "REDACTED_LEGACY_JWT_SECRET"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 Hours

    UPLOAD_DIR: str = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "uploads")
    MAX_UPLOAD_SIZE_MB: int = 50

    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
    ]

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"),
        extra="allow",
        case_sensitive=True
    )

settings = Settings()
