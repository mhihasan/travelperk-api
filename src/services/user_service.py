from typing import Optional, cast

import httpx

from src.core.config import settings
from src.utils.types import TUser


async def invoke_user_api(user_id: str, retry: int = 0) -> Optional[TUser]:
    if retry > 1:
        return None

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{settings.USER_SERVICE_DOMAIN}/users/{user_id}")

    if response.status_code == 500:
        return await invoke_user_api(user_id, retry=retry + 1)
    return cast(TUser, response.json())
