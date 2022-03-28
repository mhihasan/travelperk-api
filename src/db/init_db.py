import databases
import sqlalchemy
from sqlalchemy import create_engine

from src.core.config import settings

DATABASE_URL = (
    settings.TEST_DB_URL if settings.STAGE == "test" else settings.POSTGRESQL_URL
)

engine = create_engine(DATABASE_URL)

metadata = sqlalchemy.MetaData()

database = databases.Database(DATABASE_URL)
