from unittest.mock import Mock

import httpx
import pytest

from src.core.config import settings
from src.utils.services import (
    invoke_user_api,
    invoke_product_api,
)
from src.utils.types import TProduct


class TestInvokeUserApi:
    @pytest.mark.asyncio
    async def test_gets_user_details(self, respx_mock: Mock) -> None:
        user = {"firstName": "John", "id": "test_user_id", "lastName": "Doe"}
        respx_mock.get(f'{settings.USER_SERVICE_DOMAIN}/users/{user["id"]}').mock(
            return_value=httpx.Response(200, json=user)
        )
        response = await invoke_user_api(user["id"])
        assert response == user

    @pytest.mark.asyncio
    async def test_reties_if_user_api_returns_500(self, respx_mock: Mock) -> None:
        user = {"firstName": "John", "id": "test_user_id", "lastName": "Doe"}
        respx_mock.get(f'{settings.USER_SERVICE_DOMAIN}/users/{user["id"]}').mock(
            side_effect=[httpx.Response(500), httpx.Response(200, json=user)]
        )
        response = await invoke_user_api(user["id"])
        assert response == user


class TestInvokeProductApi:
    @pytest.mark.asyncio
    async def test_product_details(self, respx_mock: Mock) -> None:
        product: TProduct = {"code": "test_code", "name": "test_name", "price": 10.0}
        respx_mock.get(
            f'{settings.PRODUCT_SERVICE_DOMAIN}/products/{product["code"]}'
        ).mock(return_value=httpx.Response(200, json=product))
        response = await invoke_product_api(product["code"])
        assert response == product

    @pytest.mark.asyncio
    async def test_returns_None_if_product_api_returns_500(
        self, respx_mock: Mock
    ) -> None:
        product = {"code": "test_code"}
        respx_mock.get(
            f'{settings.PRODUCT_SERVICE_DOMAIN}/products/{product["code"]}'
        ).mock(return_value=httpx.Response(500))
        response = await invoke_product_api(product["code"])
        assert response is None
