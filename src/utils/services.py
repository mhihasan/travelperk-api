import asyncio
from typing import Optional, Any, cast

import httpx

from src.core.config import settings
from src.utils.logging import logger
from src.utils.types import TProduct, TUser


async def invoke_user_api(user_id: str, retry: int = 0) -> Optional[TUser]:
    if retry > 1:
        return None

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{settings.USER_SERVICE_DOMAIN}/users/{user_id}")

    if response.status_code == 500:
        return await invoke_user_api(user_id, retry=retry + 1)
    return cast(TUser, response.json())


async def invoke_product_api(product_code: str, **params: Any) -> Optional[TProduct]:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{settings.PRODUCT_SERVICE_DOMAIN}/products/{product_code}", **params
        )

    if response.status_code == 500:
        logger.error(f"Product Api returns 500: {product_code}")
        return None
    return cast(TProduct, response.json())


if __name__ == "__main__":
    asyncio.run(invoke_product_api("product-code-1"))
