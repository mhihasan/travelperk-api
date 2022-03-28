from collections.abc import AsyncGenerator

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.order_crud import create_order

from src.db.base import Base
from src.db.session import async_engine, async_session
from src.main import app


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    c = AsyncClient(app=app, base_url="http://test")
    yield c
    await c.aclose()


@pytest.fixture
async def order(db_session: AsyncSession):
    return await create_order(
        db_session, {"product_code": "test_product_code", "user_id": "test_user_id"}
    )


@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)

        async with async_session(bind=connection) as session:
            yield session

            await session.flush()
            await session.rollback()
