from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.core.config import settings


async_engine = create_async_engine(settings.async_db_url, echo=True)

async_session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)
