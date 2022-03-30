import os
from functools import cache
from typing import TYPE_CHECKING

from pydantic import BaseSettings
from dotenv import load_dotenv

if TYPE_CHECKING:
    PostgresDsn = str
else:
    from pydantic import PostgresDsn

load_dotenv(".env")


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_DRIVER: str = "asyncpg"

    USER_SERVICE_HOST: str
    USER_SERVICE_PORT: str
    PRODUCT_SERVICE_HOST: str
    PRODUCT_SERVICE_PORT: str

    STAGE: str = os.getenv("STAGE", "test")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    class Config:
        case_sensitive = True
        env_file = ".env"

    @property
    def db_url(self) -> PostgresDsn:
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def async_db_url(self) -> str:
        """Use this while creating async engine, POSTGRESQL_URL is for alembic
        migration"""
        return (
            "sqlite+aiosqlite:///./sql_app.db"
            if self.STAGE == "test"
            else self.db_url.replace("postgresql://", f"postgresql+{self.DB_DRIVER}://")
        )

    @property
    def product_service_domain(self) -> str:
        return f"http://{self.PRODUCT_SERVICE_HOST}:{self.PRODUCT_SERVICE_PORT}"

    @property
    def user_service_domain(self) -> str:
        return f"http://{self.USER_SERVICE_HOST}:{self.USER_SERVICE_PORT}"


@cache
def get_settings():
    return Settings()


settings = get_settings()
