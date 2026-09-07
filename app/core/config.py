"""Application configuration loaded from environment variables."""

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration for the Smart Data Cleaning API."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "Smart Data Cleaning & Analysis API"
    app_version: str = "1.0.0"
    environment: str = "development"
    log_level: str = "INFO"

    database_url: str = "sqlite:///./smart_data.db"
    max_file_size: int = 52_428_800  # 50 MB
    storage_path: str = "./storage"
    allowed_extensions: str = "csv,xlsx,xls"

    @property
    def allowed_extension_set(self) -> set[str]:
        return {ext.strip().lower().lstrip(".") for ext in self.allowed_extensions.split(",") if ext.strip()}

    @property
    def raw_storage_path(self) -> Path:
        return Path(self.storage_path) / "raw"

    @property
    def cleaned_storage_path(self) -> Path:
        return Path(self.storage_path) / "cleaned"

    def ensure_storage_dirs(self) -> None:
        self.raw_storage_path.mkdir(parents=True, exist_ok=True)
        self.cleaned_storage_path.mkdir(parents=True, exist_ok=True)


@lru_cache
def get_settings() -> Settings:
    return Settings()
