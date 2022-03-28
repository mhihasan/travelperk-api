from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.core.config import settings

DATABASE_URL = (
    settings.TEST_DB_URL if settings.STAGE == "test" else settings.POSTGRESQL_URL
)

async_engine = create_async_engine(DATABASE_URL, echo=True)

async_session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)
