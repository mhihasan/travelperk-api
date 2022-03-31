from collections.abc import AsyncGenerator, Generator

import aiohttp
import httpx
import pytest
from aioresponses import aioresponses
from sqlalchemy import insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db.base import Base
from src.core.db.session import async_engine, async_session
from src.main import app
from src.models.order_model import Order
from src.schemas import order_schema

TEST_ORDER_ID = "test-order-id"


@pytest.fixture
async def client() -> AsyncGenerator[httpx.AsyncClient, None]:
    async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def mock_aiohttp() -> Generator[aioresponses, None, None]:
    with aioresponses() as m:
        yield m


@pytest.fixture
async def aiohttp_session() -> AsyncGenerator[aiohttp.ClientSession, None]:
    async with aiohttp.ClientSession() as session:
        yield session


@pytest.fixture
async def created_order(db_session: AsyncSession) -> AsyncGenerator:
    query = insert(Order).values(
        id=TEST_ORDER_ID,
        **order_schema.OrderCreate(
            user_id="test-user-id",
            customer_fullname="John Doe",
            product_code="test-product-id",
            product_name="nice product",
            total_amount=10.99,
        ).dict(),
    )
    await db_session.execute(query)

    yield

    await db_session.execute(delete(Order).where(Order.id == TEST_ORDER_ID))


@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


@pytest.fixture(autouse=True)
async def test_db() -> AsyncGenerator[None, None]:
    async with async_engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
        yield
        await connection.run_sync(Base.metadata.drop_all)
