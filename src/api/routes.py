from fastapi import APIRouter

from src.api.v1 import order_api

api_router = APIRouter()
api_router.include_router(order_api.router, tags=["orders"])
