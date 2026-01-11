"""Application configuration using Pydantic Settings V2."""

from typing import Annotated

from pydantic import BeforeValidator, Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


def parse_cors(url: str | list[str]) -> list[str] | str:
    """Parse CORS origins from string or list."""
    if isinstance(url, str) and not url.startswith("["):
        return [i.strip() for i in url.split(",")]
    elif isinstance(url, list | str):
        return url
    raise ValueError(url)


class Settings(BaseSettings):
    """Application settings with validation."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )

    # Application
    APP_NAME: str = "BookGram"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "production"

    # API
    API_V1_PREFIX: str = "/api/v1"
    ALLOWED_HOSTS: Annotated[list[str] | str, BeforeValidator(parse_cors)] = ["*"]

    # Database
    DATABASE_URL: PostgresDsn = Field(
        default="postgresql+asyncpg://bookgram:bookgram@localhost:5432/bookgram"
    )
    TEST_DATABASE_URL: PostgresDsn | None = None

    # Security
    SECRET_KEY: str = Field(min_length=32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    @property
    def database_url_str(self) -> str:
        """Get database URL as string."""
        return str(self.DATABASE_URL)

    @property
    def test_database_url_str(self) -> str | None:
        """Get test database URL as string."""
        return str(self.TEST_DATABASE_URL) if self.TEST_DATABASE_URL else None


# Global settings instance
settings = Settings()
