from collections.abc import AsyncGenerator

import pytest
import sqlalchemy
from httpx import AsyncClient

from src.core.config import settings
from src.crud.order_crud import post_order
from src.db.init_db import metadata
from src.main import app


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    c = AsyncClient(app=app, base_url="http://test")
    yield c
    await c.aclose()


@pytest.fixture(autouse=True)
async def create_test_db() -> AsyncGenerator[None, None]:
    engine = sqlalchemy.create_engine(settings.TEST_DB_URL)
    metadata.create_all(engine)

    yield

    engine = sqlalchemy.create_engine(settings.TEST_DB_URL)
    metadata.drop_all(engine)


@pytest.fixture
async def order():
    return await post_order(
        {"product_code": "test_product_code", "user_id": "test_user_id"}
    )
