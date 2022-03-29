from typing import Any, Optional, cast

import httpx

from src.core.config import settings
from src.utils.logging import logger
from src.utils.types import TProduct


async def invoke_product_api(product_code: str, **params: Any) -> Optional[TProduct]:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{settings.PRODUCT_SERVICE_DOMAIN}/products/{product_code}", **params
        )

    if response.status_code == 500:
        logger.error(f"Product Api returns 500: {product_code}")
        return None
    return cast(TProduct, response.json())
