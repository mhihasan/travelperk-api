import asyncio
import uuid
from typing import cast, Any

import aiohttp
from sqlalchemy import insert, update, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.order_model import Order
from src.schemas import order_schema
from src.services import product_service, user_service
from src.utils.exceptions import DoesNotExist


def _user_fullname(first: str, last: str) -> str:
    return f'{first or ""} {last or ""}'.strip()


async def create_order(db_session: AsyncSession, order: order_schema.OrderBase):
    async with aiohttp.ClientSession() as http_session:
        product, user = await asyncio.gather(
            product_service.fetch_product(http_session, order.product_code),
            user_service.fetch_user(http_session, order.user_id),
        )

    query = insert(Order).values(
        id=str(uuid.uuid4()),
        **order_schema.OrderCreate(
            user_id=user.id,
            customer_fullname=_user_fullname(user.first_name, user.last_name),
            product_code=product.id,
            product_name=product.name,
            total_amount=product.price,
        ).dict(),
    )
    await db_session.execute(query)


async def get_order(db_session: AsyncSession, order_id: str) -> order_schema.Order:
    query = select(Order).where(Order.id == order_id)
    order = (await db_session.execute(query)).scalar()

    if order is None:
        raise DoesNotExist("Item not found")

    return cast(order_schema.Order, order_schema.Order.from_orm(order))


async def list_orders(
    db_session: AsyncSession, page_no: int = 1, per_page: int = 10
) -> list[order_schema.Order]:
    query = select(Order).offset(per_page * (page_no - 1)).limit(per_page)
    orders = (await db_session.execute(query)).scalars().all()

    return [order_schema.Order.from_orm(order) for order in orders]


async def update_order(
    db_session: AsyncSession, order_id: str, payload: dict[str, Any]
) -> None:
    query = update(Order).where(Order.id == order_id).values(**payload)
    await db_session.execute(query)


async def delete_order(db_session: AsyncSession, order_id: str) -> None:
    query = delete(Order).where(Order.id == order_id)
    await db_session.execute(query)
