import pytest

from src.crud import order_crud
from src.models.order import OrderStatus


class TestPostOrder:
    @pytest.mark.asyncio
    async def test_post_order(self):
        order_info = {"user_id": "test_user_id", "product_code": "test_product_code"}
        created_order = await order_crud.post_order(order_info)

        created_order.pop("created_at")
        assert order_info == {
            "user_id": created_order["user_id"],
            "product_code": created_order["product_code"],
        }

    @pytest.mark.parametrize(
        "invalid_info",
        [
            ({"user_id": None, "product_code": None}),
            ({"user_id": "test_user_id", "product_code": None}),
            ({"user_id": None, "product_code": "test_product_code"}),
        ],
    )
    @pytest.mark.asyncio
    async def test_fails_on_creating_order_using_invalid_input(self, invalid_info):
        with pytest.raises(Exception):
            await order_crud.post_order(invalid_info)


class TestGetOrder:
    @pytest.mark.asyncio
    async def test_gets_order(self):
        order_info = {"user_id": "test_user_id", "product_code": "test_product_code"}
        created_order = await order_crud.post_order(order_info)

        order = await order_crud.get_order(created_order["id"])
        order.pop("created_at")
        order.pop("id")
        assert order == {
            "customer_fullname": None,
            "product_code": "test_product_code",
            "product_name": None,
            "status": None,
            "total_amount": None,
            "user_id": "test_user_id",
        }

    @pytest.mark.asyncio
    async def test_returns_None_on_non_existing_order(self):
        order = await order_crud.get_order("dummy")
        assert order is None


class TestListOrder:
    @pytest.mark.asyncio
    async def test_returns_order_list(self):
        for i in range(11):
            order_info = {
                "user_id": f"test_user_id_{i}",
                "product_code": "test_product_code",
            }
            await order_crud.post_order(order_info)

        orders = await order_crud.list_orders()
        assert len(orders) == 10

        orders = await order_crud.list_orders(page_no=2)
        assert len(orders) == 1

        orders = await order_crud.list_orders(page_no=3)
        assert len(orders) == 0

        orders = await order_crud.list_orders(per_page=11)
        assert len(orders) == 11


class TestPutOrder:
    @pytest.mark.asyncio
    async def test_put_order(self):
        order_info = {"user_id": "test_user_id", "product_code": "test_product_code"}
        created_order = await order_crud.post_order(order_info)

        await order_crud.put_order(
            created_order["id"], {"status": OrderStatus.finished.value}
        )

        created_order.pop("created_at")
        updated_order = await order_crud.get_order(created_order["id"])
        assert updated_order["status"] == OrderStatus.finished.value

    @pytest.mark.asyncio
    async def test_updates_no_order_for_non_existing_order(self):
        await order_crud.put_order("dummy", {"status": OrderStatus.finished.value})
        updated_order = await order_crud.get_order("dummy")
        assert updated_order is None
