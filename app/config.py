from __future__ import annotations

import json
from functools import lru_cache
from typing import Any

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings and environment configuration loader.

    Reads configuration values from environment variables or a local `.env` file.
    Supports CORS configuration, Gemini model adjustments, and rate limiter tuning.
    """
    gemini_api_key: str | None = None
    gemini_model: str = "gemini-2.5-flash"
    gemini_max_output_tokens: int = 256
    allowed_origins: list[str] = ["http://localhost:8000", "http://127.0.0.1:8000"]
    rate_limit_capacity: int = 30
    rate_limit_refill_per_sec: float = 0.5

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @field_validator("allowed_origins", mode="before")
    @classmethod
    def parse_allowed_origins(cls, v: Any) -> list[str]:
        """Convert environment string configurations for CORS allowed origins into a list.

        Supports JSON lists e.g. '["http://localhost:3000"]' or comma-separated lists.

        Args:
            v: Input raw value.

        Returns:
            list[str]: Parsed list of origins.
        """
        if isinstance(v, str):
            try:
                parsed = json.loads(v)
                if isinstance(parsed, list):
                    return [str(item) for item in parsed]
            except ValueError:
                return [item.strip() for item in v.split(",") if item.strip()]
        if isinstance(v, list):
            return [str(item) for item in v]
        return ["*"]

    @property
    def gemini_enabled(self) -> bool:
        """True if the Gemini API Key is configured and the model is active.

        Returns:
            bool: Activation status.
        """
        return bool(self.gemini_api_key)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Retrieve and cache the global application settings instance.

    Returns:
        Settings: Configured settings object.
    """
    return Settings()
