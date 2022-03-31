import aiohttp
import pytest
from aioresponses import aioresponses

from src.core.config import settings
from src.schemas import product_schema
from src.services.product_service import fetch_product


class TestFetchProduct:
    @pytest.mark.asyncio
    async def test_should_return_product_details(
        self, mock_aiohttp: aioresponses, aiohttp_session: aiohttp.ClientSession
    ) -> None:
        product = {"id": "test_code", "name": "test_name", "price": 10.0}
        mock_aiohttp.get(
            f'{settings.product_service_domain}/products/{product["id"]}',
            status=200,
            payload=product,
        )

        response = await fetch_product(aiohttp_session, "test_code")

        assert response == product_schema.Product(**product)

    @pytest.mark.asyncio
    async def test_throws_error_if_product_not_found(
        self, mock_aiohttp: aioresponses, aiohttp_session: aiohttp.ClientSession
    ) -> None:
        product = {"id": "test_code"}
        mock_aiohttp.get(
            f'{settings.product_service_domain}/products/{product["id"]}', status=500
        )

        with pytest.raises(Exception):
            await fetch_product(aiohttp_session, product["id"])
