import uuid
from typing import Any, cast

from sqlalchemy import select, update, delete, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.exceptions import DoesNotExist
from src.models.order import Order
from src.schemas import order_schema


async def create_order(session: AsyncSession, payload: dict[str, Any]) -> None:
    query = insert(Order).values(id=str(uuid.uuid4()), **payload)
    await session.execute(query)


async def get_order(session: AsyncSession, order_id: str) -> order_schema.Order:
    query = select(Order).where(Order.id == order_id)
    order = (await session.execute(query)).scalar()

    if order is None:
        raise DoesNotExist("Item not found")

    return cast(order_schema.Order, order_schema.Order.from_orm(order))


async def list_orders(
    session: AsyncSession, page_no: int = 1, per_page: int = 10
) -> list[order_schema.Order]:
    query = select(Order).offset(per_page * (page_no - 1)).limit(per_page)
    orders = (await session.execute(query)).scalars().all()

    return [order_schema.Order.from_orm(order) for order in orders]


async def update_order(
    session: AsyncSession, order_id: str, payload: dict[str, Any]
) -> None:
    query = update(Order).where(Order.id == order_id).values(**payload)
    await session.execute(query)


async def delete_order(session: AsyncSession, order_id: str) -> None:
    query = delete(Order).where(Order.id == order_id)
    await session.execute(query)
