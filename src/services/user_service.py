import httpx

from src.core.config import settings
from src.schemas import user_schema


async def fetch_user(user_id: str, retry: int = 3) -> user_schema.User:
    if retry < 0:
        raise Exception("Max retries are exceeded")

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{settings.user_service_domain}/users/{user_id}")

    if response.status_code != 200:
        return await fetch_user(user_id, retry=retry + 1)

    return user_schema.User(**response.json())
