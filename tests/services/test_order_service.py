from typing import Any

import pytest
from aioresponses import aioresponses
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import settings
from src.models.order_model import OrderStatus, Order
from src.schemas import order_schema
from src.services import order_service
from src.utils.exceptions import DoesNotExist
from tests.conftest import TEST_ORDER_ID


class TestPostOrder:
    @pytest.mark.asyncio
    async def test_post_order(
        self, db_session: AsyncSession, mock_aiohttp: aioresponses
    ):
        product = {"id": "test_product_id", "name": "test_name", "price": 10.99}
        mock_aiohttp.get(
            f'{settings.product_service_domain}/products/{product["id"]}',
            status=200,
            payload=product,
        )

        user = {"first_name": "John", "id": "test_user_id", "last_name": "Doe"}
        mock_aiohttp.get(
            f'{settings.user_service_domain}/users/{user["id"]}',
            status=200,
            payload=user,
        )

        order_info = {"user_id": "test_user_id", "product_code": "test_product_id"}
        await order_service.create_order(
            db_session, order_schema.OrderCreate(**order_info)
        )

        order = (await order_service.list_orders(db_session))[0]
        assert order == order_schema.Order(
            **{
                "id": order.id,
                "customer_fullname": "John Doe",
                "product_code": "test_product_id",
                "product_name": "test_name",
                "status": OrderStatus.initiated.value,
                "total_amount": 10.99,
                "user_id": "test_user_id",
                "created_at": order.created_at,
            }
        )

    @pytest.mark.parametrize(
        "invalid_info",
        [
            ({"user_id": None, "product_code": None}),
            ({"user_id": "test_user_id", "product_code": None}),
            ({"user_id": None, "product_code": "test_product_code"}),
        ],
    )
    @pytest.mark.asyncio
    async def test_fails_on_creating_order_using_invalid_input(
        self, invalid_info: dict[str, Any], db_session: AsyncSession
    ):
        with pytest.raises(Exception):
            await order_service.create_order(
                db_session, order_schema.OrderCreate(**invalid_info)
            )


class TestGetOrder:
    @pytest.mark.usefixtures("created_order")
    @pytest.mark.asyncio
    async def test_gets_order(self, db_session: AsyncSession):
        order = await order_service.get_order(db_session, TEST_ORDER_ID)

        assert order == order_schema.Order(
            **{
                "id": TEST_ORDER_ID,
                "customer_fullname": "John Doe",
                "product_code": "test-product-id",
                "product_name": "nice product",
                "status": OrderStatus.initiated.value,
                "total_amount": 10.99,
                "user_id": "test-user-id",
                "created_at": order.created_at,
            }
        )

    @pytest.mark.asyncio
    async def test_returns_Exception_on_non_existing_order(
        self, db_session: AsyncSession
    ):
        with pytest.raises(DoesNotExist):
            await order_service.get_order(db_session, "dummy")


class TestListOrders:
    @pytest.mark.asyncio
    async def test_returns_order_list(self, db_session: AsyncSession):
        for i in range(11):
            query = insert(Order).values(
                id=f"{TEST_ORDER_ID}_{i}",
                **order_schema.OrderCreate(
                    user_id="test-user-id",
                    customer_fullname="John Doe",
                    product_code="test-product-id",
                    product_name="nice product",
                    total_amount=10.99,
                ).dict(),
            )
            await db_session.execute(query)

        orders = await order_service.list_orders(db_session)
        assert len(orders) == 10

        orders = await order_service.list_orders(db_session, page_no=2)
        assert len(orders) == 1

        orders = await order_service.list_orders(db_session, page_no=3)
        assert len(orders) == 0

        orders = await order_service.list_orders(db_session, per_page=11)
        assert len(orders) == 11


class TestUpdateOrder:
    @pytest.mark.usefixtures("created_order")
    @pytest.mark.asyncio
    async def test_updates_order(self, db_session: AsyncSession):
        await order_service.update_order(
            db_session, TEST_ORDER_ID, {"status": OrderStatus.finished.value}
        )

        updated_order = await order_service.get_order(db_session, TEST_ORDER_ID)
        assert updated_order.status == OrderStatus.finished.value

    @pytest.mark.asyncio
    async def test_updates_no_order_for_non_existing_order(
        self, db_session: AsyncSession
    ):
        await order_service.update_order(
            db_session, "dummy", {"status": OrderStatus.finished.value}
        )

        with pytest.raises(DoesNotExist):
            await order_service.get_order(db_session, "dummy")
