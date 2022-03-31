import aiohttp

from src.core.config import settings
from src.schemas import user_schema
from src.utils import requests


async def fetch_user(session: aiohttp.ClientSession, user_id: str) -> user_schema.User:
    response = await requests.fetch(
        session, f"{settings.user_service_domain}/users/{user_id}"
    )

    return user_schema.User(**response)
