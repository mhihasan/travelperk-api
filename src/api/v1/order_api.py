from typing import TypeVar

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.dependencies.db import get_session
from src.crud import order_crud
from src.crud.exceptions import DoesNotExist
from src.models.order import OrderStatus
from src.schemas import order_schema

router = APIRouter()

T = TypeVar("T", str, float)


@router.post("/orders", status_code=201, response_model=order_schema.Order)
async def post_order(
    payload: order_schema.OrderCreate, session: AsyncSession = Depends(get_session)
):
    order_info = {
        "user_id": payload.user_id,
        "product_code": payload.product_code,
        "status": OrderStatus.initiated.value,
    }
    await order_crud.create_order(session, order_info)


@router.get("/orders/{order_id}", response_model=order_schema.Order)
async def get_order(order_id: str, session: AsyncSession = Depends(get_session)):
    try:
        order = await order_crud.get_order(session, order_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Order not found")

    return order


@router.get("/orders", response_model=list[order_schema.Order])
async def list_orders(
    page_no: int = 1, per_page: int = 10, session: AsyncSession = Depends(get_session)
):
    return await order_crud.list_orders(session, page_no=page_no, per_page=per_page)