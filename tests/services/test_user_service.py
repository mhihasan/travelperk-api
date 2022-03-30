from unittest.mock import Mock

import httpx
import pytest

from src.core.config import settings
from src.services.user_service import fetch_user


class TestFetchUser:
    @pytest.mark.asyncio
    async def test_should_returns_user_details(self, respx_mock: Mock) -> None:
        user = {"first_name": "John", "id": "test_user_id", "last_name": "Doe"}
        respx_mock.get(f'{settings.user_service_domain}/users/{user["id"]}').mock(
            return_value=httpx.Response(200, json=user)
        )
        response = await fetch_user(user["id"])
        assert response == user

    @pytest.mark.asyncio
    async def test_reties_if_user_api_returns_500(self, respx_mock: Mock) -> None:
        user = {"first_name": "John", "id": "test_user_id", "last_name": "Doe"}
        respx_mock.get(f'{settings.user_service_domain}/users/{user["id"]}').mock(
            side_effect=[httpx.Response(500), httpx.Response(200, json=user)]
        )
        response = await fetch_user(user["id"])
        assert response == user
