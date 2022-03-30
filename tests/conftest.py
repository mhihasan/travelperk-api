from collections.abc import AsyncGenerator

import pytest
from httpx import AsyncClient
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.order_model import Order
from src.schemas import order_schema

from src.core.db.base import Base
from src.core.db.session import async_engine, async_session
from src.main import app


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    c = AsyncClient(app=app, base_url="http://test")
    yield c
    await c.aclose()


@pytest.fixture
async def order(db_session: AsyncSession):
    query = insert(Order).values(
        id="test-order-id",
        **order_schema.OrderCreate(
            user_id="user-id-1",
            customer_fullname="John Doe",
            product_code="product-id-1",
            product_name="nice product",
            total_amount=10.99,
        ).dict(),
    )
    await db_session.execute(query)


@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)

        async with async_session(bind=connection) as session:
            yield session

            await session.flush()
            await session.rollback()
