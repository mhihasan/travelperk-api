from typing import Any

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud import order_crud
from src.crud.exceptions import DoesNotExist
from src.models.order_model import OrderStatus
from src.schemas import order_schema


class TestPostOrder:
    @pytest.mark.asyncio
    async def test_post_order(self, db_session: AsyncSession):
        order_info = {"user_id": "test_user_id", "product_code": "test_product_code"}
        await order_crud.create_order(
            db_session, order_schema.OrderCreate(**order_info)
        )

        order = (await order_crud.list_orders(db_session))[0]
        assert order == order_schema.Order(
            **{
                "id": order.id,
                "customer_fullname": None,
                "product_code": "test_product_code",
                "product_name": None,
                "status": OrderStatus.initiated.value,
                "total_amount": 0.0,
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
            await order_crud.create_order(
                db_session, order_schema.OrderCreate(**invalid_info)
            )


class TestGetOrder:
    @pytest.mark.asyncio
    async def test_gets_order(self, db_session: AsyncSession):
        order_info = {"user_id": "test_user_id", "product_code": "test_product_code"}
        await order_crud.create_order(
            db_session, order_schema.OrderCreate(**order_info)
        )
        created_order = (await order_crud.list_orders(db_session))[0]

        order = await order_crud.get_order(db_session, created_order.id)

        assert order == order_schema.Order(
            **{
                "id": order.id,
                "customer_fullname": None,
                "product_code": "test_product_code",
                "product_name": None,
                "status": OrderStatus.initiated.value,
                "total_amount": 0.0,
                "user_id": "test_user_id",
                "created_at": order.created_at,
            }
        )

    @pytest.mark.asyncio
    async def test_returns_Exception_on_non_existing_order(
        self, db_session: AsyncSession
    ):
        with pytest.raises(DoesNotExist):
            await order_crud.get_order(db_session, "dummy")


class TestListOrders:
    @pytest.mark.asyncio
    async def test_returns_order_list(self, db_session: AsyncSession):
        for i in range(11):
            order_info = {
                "user_id": f"test_user_id_{i}",
                "product_code": "test_product_code",
            }
            await order_crud.create_order(
                db_session, order_schema.OrderCreate(**order_info)
            )

        orders = await order_crud.list_orders(db_session)
        assert len(orders) == 10

        orders = await order_crud.list_orders(db_session, page_no=2)
        assert len(orders) == 1

        orders = await order_crud.list_orders(db_session, page_no=3)
        assert len(orders) == 0

        orders = await order_crud.list_orders(db_session, per_page=11)
        assert len(orders) == 11


class TestUpdateOrder:
    @pytest.mark.asyncio
    async def test_updates_order(self, db_session: AsyncSession):
        order_info = {"user_id": "test_user_id", "product_code": "test_product_code"}
        await order_crud.create_order(
            db_session, order_schema.OrderCreate(**order_info)
        )

        created_order = (await order_crud.list_orders(db_session))[0]

        await order_crud.update_order(
            db_session, created_order.id, {"status": OrderStatus.finished.value}
        )

        updated_order = await order_crud.get_order(db_session, created_order.id)
        assert updated_order.status == OrderStatus.finished.value

    @pytest.mark.asyncio
    async def test_updates_no_order_for_non_existing_order(
        self, db_session: AsyncSession
    ):
        await order_crud.update_order(
            db_session, "dummy", {"status": OrderStatus.finished.value}
        )

        with pytest.raises(DoesNotExist):
            await order_crud.get_order(db_session, "dummy")
