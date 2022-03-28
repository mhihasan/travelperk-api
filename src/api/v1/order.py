from typing import TypeVar, Any, Optional

from fastapi import APIRouter, HTTPException

from src.crud import order_crud
from src.models.order import OrderStatus
from src.schemas.order import OrderInDbSchema, OrderInSchema, OrderInResponseSchema

router = APIRouter()

T = TypeVar("T", str, float)


@router.post("/orders", response_model=OrderInResponseSchema)
async def create_order(payload: OrderInSchema) -> dict[str, Any]:
    order_info = {
        "user_id": payload.user_id,
        "product_code": payload.product_code,
        "status": OrderStatus.initiated.value,
    }
    created_order = await order_crud.post_order(order_info)
    return created_order


@router.get("/orders/{id}", response_model=OrderInDbSchema)
async def get_order(id: str) -> dict[str, Any]:
    order: Optional[dict[str, Any]] = await order_crud.get_order(id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.get("/orders", response_model=list[OrderInDbSchema])
async def list_orders(page: int = 1) -> list[dict[str, Any]]:
    orders = await order_crud.list_orders(page)
    return orders
