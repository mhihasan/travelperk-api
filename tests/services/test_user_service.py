import aiohttp
import pytest
from aioresponses import aioresponses

from src.core.config import settings
from src.services.user_service import fetch_user


class TestFetchUser:
    @pytest.mark.asyncio
    async def test_should_returns_user_details(
        self, mock_aiohttp: aioresponses, aiohttp_session: aiohttp.ClientSession
    ) -> None:
        user = {"first_name": "John", "id": "test_user_id", "last_name": "Doe"}
        mock_aiohttp.get(
            f'{settings.user_service_domain}/users/{user["id"]}',
            status=200,
            payload=user,
        )

        response = await fetch_user(aiohttp_session, user["id"])
        assert response == user

    @pytest.mark.asyncio
    async def test_reties_if_user_api_returns_500(
        self, mock_aiohttp: aioresponses, aiohttp_session: aiohttp.ClientSession
    ) -> None:
        user = {"first_name": "John", "id": "test_user_id", "last_name": "Doe"}
        mock_aiohttp.get(
            f'{settings.user_service_domain}/users/{user["id"]}', status=500
        )

        with pytest.raises(Exception):
            await fetch_user(aiohttp_session, user["id"])
