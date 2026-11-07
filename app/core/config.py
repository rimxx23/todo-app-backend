import functools

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    DATABASE_URL: str
    CORS_ALLOWED_ORIGIN: list[str]


@functools.lru_cache
def get_settings() -> Settings:
    return Settings()
