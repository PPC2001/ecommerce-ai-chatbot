"""
E-Commerce AI Chatbot Backend
Application configuration with strict environment variable validation.
Secrets are NEVER hardcoded — the app errors out if required config is missing.
"""

import logging
from functools import lru_cache
from pathlib import Path

from pydantic import field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent.parent / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Google Cloud — REQUIRED, no fallback
    google_cloud_project: str
    google_cloud_location: str = "us-central1"

    # LLM settings
    gemini_model: str = "gemini-2.5-pro"

    # Application settings
    app_env: str = "development"
    app_name: str = "E-Commerce AI Chatbot"
    app_version: str = "1.0.0"
    debug: bool = False

    # CORS — strict allow-list, no wildcards
    allowed_origins: str = "http://localhost:5173,http://127.0.0.1:5173"

    # Rate limiting
    rate_limit_per_minute: int = 60

    # Chat settings
    max_message_length: int = 2000
    max_history_length: int = 20

    @field_validator("google_cloud_project")
    @classmethod
    def validate_project(cls, v: str) -> str:
        if not v or v.strip() == "":
            raise ValueError(
                "GOOGLE_CLOUD_PROJECT is required and must not be empty. "
                "Set it in the .env file or environment."
            )
        return v.strip()

    @field_validator("google_cloud_location")
    @classmethod
    def validate_location(cls, v: str) -> str:
        valid_locations = {
            "us-central1", "us-east1", "us-west1", "us-west4",
            "europe-west1", "europe-west4", "asia-east1", "asia-northeast1",
        }
        if v not in valid_locations:
            logger.warning(
                "Location '%s' may not support Vertex AI. "
                "Recommended: us-central1",
                v,
            )
        return v.strip()

    @model_validator(mode="after")
    def validate_settings(self) -> "Settings":
        logger.info(
            "Configuration loaded: project=%s, location=%s, model=%s, env=%s",
            self.google_cloud_project,
            self.google_cloud_location,
            self.gemini_model,
            self.app_env,
        )
        return self

    @property
    def allowed_origins_list(self) -> list[str]:
        """Parse comma-separated origins into a list."""
        return [o.strip() for o in self.allowed_origins.split(",") if o.strip()]


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """
    Returns cached application settings.
    Raises ValueError if required environment variables are missing.
    """
    return Settings()
