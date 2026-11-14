from pathlib import Path

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


PROJECT_ROOT = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    app_name: str = "AI Product Studio API"
    app_version: str = "1.0.0"
    debug: bool = False
    hf_space_id: str = "alebcdev/ai-product-studio-space"
    hf_token: SecretStr | None = None
    hf_concurrency_limit: int = Field(default=2, gt=0, le=10)
    hf_timeout_seconds: float = Field(default=120.0, gt=0, le=600)
    rate_limit_requests: int = Field(default=5, gt=0)
    rate_limit_window_seconds: float = Field(default=600.0, gt=0)

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
