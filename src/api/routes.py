from fastapi import APIRouter

from src.api.v1.order import router as order_router

api_router = APIRouter()
api_router.include_router(order_router, tags=["orders"])
