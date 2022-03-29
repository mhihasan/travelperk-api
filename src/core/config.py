import os
from functools import cache
from typing import TYPE_CHECKING

from pydantic import BaseSettings

if TYPE_CHECKING:
    PostgresDsn = str
else:
    from pydantic import PostgresDsn


class Settings(BaseSettings):
    DB_HOST = os.environ["DB_HOST"]
    DB_PORT = os.environ["DB_PORT"]
    DB_USER = os.environ["DB_USER"]
    DB_PASSWORD = os.environ["DB_PASSWORD"]
    DB_NAME = os.environ["DB_NAME"]
    DB_DRIVER = "asyncpg"

    USER_SERVICE_HOST = os.environ["USER_SERVICE_HOST"]
    USER_SERVICE_PORT = os.environ["USER_SERVICE_PORT"]
    PRODUCT_SERVICE_HOST = os.environ["PRODUCT_SERVICE_HOST"]
    PRODUCT_SERVICE_PORT = os.environ["PRODUCT_SERVICE_PORT"]
    POSTGRESQL_URL: PostgresDsn = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    TEST_DB_URL: str = "sqlite+aiosqlite:///./sql_app.db"
    STAGE: str = os.getenv("STAGE", "test")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    PRODUCT_SERVICE_DOMAIN: str = (
        f"http://{PRODUCT_SERVICE_HOST}:{PRODUCT_SERVICE_PORT}"
    )
    USER_SERVICE_DOMAIN: str = f"http://{USER_SERVICE_HOST}:{USER_SERVICE_PORT}"

    class Config:
        case_sensitive = True
        env_file = ".env"

    @property
    def async_db_url(self) -> str:
        """Use this while creating async engine, POSTGRESQL_URL is for alembic
        migration"""

        return (
            self.TEST_DB_URL
            if self.STAGE == "test"
            else self.POSTGRESQL_URL.replace(
                "postgresql://", f"postgresql+{self.DB_DRIVER}://"
            )
        )


@cache
def get_settings():
    return Settings()


settings = get_settings()
