import aiohttp

from src.core.config import settings
from src.schemas import product_schema
from src.utils import requests


async def fetch_product(
    session: aiohttp.ClientSession, product_id: str
) -> product_schema.Product:
    response = await requests.fetch(
        session, f"{settings.product_service_domain}/products/{product_id}"
    )

    return product_schema.Product(**response)
