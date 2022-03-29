import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud import order_crud
from src.schemas import order_schema


class TestPostOrderAPI:
    @pytest.mark.asyncio
    async def test_creates_order_successfully(
        self,
        client: AsyncClient,
    ) -> None:
        payload = {"user_id": "test_user_id", "product_code": "test_product_code"}
        response = await client.post(
            "/orders",
            json=payload,
        )

        assert response.status_code == 201

    @pytest.mark.parametrize(
        "invalid_payload, expected_status",
        [
            ({"user_id": None, "product_code": "test_product_code"}, 422),
            ({"user_id": "test_user_id", "product_code": None}, 422),
            ({"user_id": None, "product_code": None}, 422),
            ({"user_id": "", "product_code": ""}, 422),
        ],
    )
    @pytest.mark.asyncio
    async def test_raises_exception_for_invalid_input_payload(
        self,
        invalid_payload,
        expected_status,
        client: AsyncClient,
    ) -> None:
        response = await client.post(
            "/orders",
            json=invalid_payload,
        )

        assert response.status_code == expected_status


class TestGetOrderAPI:
    @pytest.mark.asyncio
    async def test_gets_order(
        self, client: AsyncClient, db_session: AsyncSession
    ) -> None:
        order_info = {
            "customer_fullname": "John Doe",
            "product_code": "test_product_code",
            "product_name": "test_product_name",
            "status": "initiated",
            "total_amount": 10.0,
            "user_id": "test_user_id",
        }
        await order_crud.create_order(
            db_session, order_schema.OrderCreate(**order_info)
        )
        order = (await order_crud.list_orders(db_session))[0]

        response = await client.get(f"/orders/{order.id}")

        assert response.status_code == 200
        data = response.json()
        assert data == {}

    @pytest.mark.asyncio
    async def test_raises_404_exception_if_no_order_found(
        self,
        client: AsyncClient,
    ) -> None:
        response = await client.get("/orders/a-random-string")

        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "Order not found"
