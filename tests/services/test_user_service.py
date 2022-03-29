from unittest.mock import Mock

import httpx
import pytest

from src.core.config import settings
from src.services.user_service import invoke_user_api


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
