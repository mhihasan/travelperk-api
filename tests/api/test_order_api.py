import httpx
import pytest
from aioresponses import aioresponses

from src.core.config import settings


class TestPostOrderAPI:
    @pytest.mark.asyncio
    async def test_creates_order_successfully(
        self, client: httpx.AsyncClient, mock_aiohttp: aioresponses
    ) -> None:
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

        response = await client.post(
            "/orders",
            json={"user_id": "test_user_id", "product_code": "test_product_id"},
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
        client: httpx.AsyncClient,
        invalid_payload,
        expected_status,
    ) -> None:
        response = await client.post(
            "/orders",
            json=invalid_payload,
        )

        assert response.status_code == expected_status


class TestGetOrderAPI:
    @pytest.mark.asyncio
    async def test_raises_404_exception_if_no_order_found(
        self, client: httpx.AsyncClient
    ) -> None:
        response = await client.get("/orders/a-random-order")

        assert response.status_code == 404

        data = response.json()
        assert data["detail"] == "Order not found"
