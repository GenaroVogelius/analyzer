import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

from app.infrastructure.utils.decorators.singleton import singleton

load_dotenv()


@singleton
class Settings(BaseSettings):
    APP_NAME: str = "Analizer API Backend Service"
    DESCRIPTION: str = "Backend service that analyze portfolio maded with fastAPI"
    DEBUG: bool = bool(os.getenv("DEBUG", "True"))
    VERSION: str = "1.0.0"

    POSTGRESQL_URL: str = os.getenv(
        "POSTGRESQL_URL",
        "postgres://admin:password123@postgres:5432/postgresql-backend",
    )
    ALLOW_ORIGINS: str = os.getenv("ALLOW_ORIGINS", "*")

    # API settings
    API_PREFIX: str = os.getenv("API_PREFIX", "/api/v1")

    # Authentication settings
    SECRET_KEY: str = os.getenv(
        "SECRET_KEY", "your-secret-key-change-this-in-production"
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

