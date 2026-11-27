from functools import lru_cache
from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import make_url
from sqlalchemy.exc import ArgumentError


BACKEND_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BACKEND_DIR / ".env", env_file_encoding="utf-8",
        extra="ignore", hide_input_in_errors=True,
    )

    database_url: str
    test_database_url: str | None = None
    frontend_origin: str = "http://localhost:5173"
    session_ttl_hours: int = Field(default=24, gt=0)
    session_cookie_secure: bool = False
    app_tz: str = "Europe/Moscow"
    features: str = ""
    ai_enabled: bool = False

    @field_validator("database_url", "test_database_url")
    @classmethod
    def postgres_url(cls, value: str | None) -> str | None:
        if value is None:
            return None
        try:
            url = make_url(value)
        except ArgumentError:
            raise ValueError("Некорректная строка подключения к PostgreSQL") from None
        if url.drivername not in {"postgresql", "postgresql+psycopg"} or not url.database:
            raise ValueError("Укажите адрес PostgreSQL с именем базы данных")
        return url.set(drivername="postgresql+psycopg").render_as_string(hide_password=False)


@lru_cache
def get_settings() -> Settings:
    return Settings()
