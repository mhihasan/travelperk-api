import os
from typing import TYPE_CHECKING

from pydantic import BaseSettings

DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_NAME = os.environ["DB_NAME"]

USER_SERVICE_HOST = os.environ["USER_SERVICE_HOST"]
USER_SERVICE_PORT = os.environ["USER_SERVICE_PORT"]
PRODUCT_SERVICE_HOST = os.environ["PRODUCT_SERVICE_HOST"]
PRODUCT_SERVICE_PORT = os.environ["PRODUCT_SERVICE_PORT"]

if TYPE_CHECKING:
    PostgresDsn = str
else:
    from pydantic import PostgresDsn


class Settings(BaseSettings):
    POSTGRESQL_URL: PostgresDsn = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    TEST_DB_URL: str = "sqlite:///./sql_app.db"
    STAGE: str = os.getenv("STAGE", "test")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    PRODUCT_SERVICE_DOMAIN: str = (
        f"http://{PRODUCT_SERVICE_HOST}:{PRODUCT_SERVICE_PORT}"
    )
    USER_SERVICE_DOMAIN: str = f"http://{USER_SERVICE_HOST}:{USER_SERVICE_PORT}"

    class Config:
        case_sensitive = True


settings = Settings()
