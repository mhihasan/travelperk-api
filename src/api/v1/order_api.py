from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db.session_creator import get_session
from src.utils.exceptions import DoesNotExist
from src.schemas import order_schema
from src.services import order_service

router = APIRouter()


@router.post("/orders", status_code=201, response_model=order_schema.Order)
async def post_order(
    payload: order_schema.OrderBase, session: AsyncSession = Depends(get_session)
):
    await order_service.create_order(session, payload)


@router.get("/orders/{order_id}", response_model=order_schema.Order)
async def get_order(order_id: str, session: AsyncSession = Depends(get_session)):
    try:
        order = await order_service.get_order(session, order_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Order not found")

    return order


@router.get("/orders", response_model=list[order_schema.Order])
async def list_orders(
    page_no: int = 1, per_page: int = 10, session: AsyncSession = Depends(get_session)
):
    return await order_service.list_orders(session, page_no=page_no, per_page=per_page)


@router.delete("/orders/{order_id}", response_model=order_schema.Order)
async def delete_order(order_id: str, session: AsyncSession = Depends(get_session)):
    await order_service.delete_order(session, order_id)
