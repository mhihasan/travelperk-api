from unittest.mock import Mock

import httpx
import pytest

from src.core.config import settings
from src.schemas import product_schema
from src.services.product_service import fetch_product


class TestFetchProduct:
    @pytest.mark.asyncio
    async def test_should_return_product_details(self, respx_mock: Mock) -> None:
        product = {"id": "test_code", "name": "test_name", "price": 10.0}
        respx_mock.get(
            f'{settings.product_service_domain}/products/{product["id"]}'
        ).mock(return_value=httpx.Response(200, json=product))

        response = await fetch_product("test_code")

        assert response == product_schema.Product(**product)

    @pytest.mark.asyncio
    async def test_throws_error_if_product_not_found(self, respx_mock: Mock) -> None:
        product = {"id": "test_code"}
        respx_mock.get(
            f'{settings.product_service_domain}/products/{product["id"]}'
        ).mock(return_value=httpx.Response(500))

        with pytest.raises(Exception):
            await fetch_product(product["id"])
