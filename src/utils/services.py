import asyncio

from src.services.product_service import invoke_product_api

if __name__ == "__main__":
    asyncio.run(invoke_product_api("product-code-1"))
