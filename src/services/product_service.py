import httpx

from src.core.config import settings
from src.schemas import product_schema


async def fetch_product(product_id: str) -> product_schema.Product:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{settings.product_service_domain}/products/{product_id}"
        )

    if response.status_code != 200:
        raise Exception(f"Error on fetching product with: {str(response)}")

    return product_schema.Product(**response.json())
