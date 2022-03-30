import asyncio
import uuid
from typing import cast, Any

from sqlalchemy import insert, update, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.order_model import Order
from src.schemas import order_schema
from src.services import product_service, user_service
from src.utils.exceptions import DoesNotExist


def user_fullname(first: str, last: str) -> str:
    return f'{first or ""} {last or ""}'.strip()


async def create_order(session: AsyncSession, order: order_schema.OrderBase):
    product, user = await asyncio.gather(
        product_service.fetch_product(order.product_code),
        user_service.fetch_user(order.user_id),
    )

    query = insert(Order).values(
        id=str(uuid.uuid4()),
        **order_schema.OrderCreate(
            user_id=user.id,
            customer_fullname=user_fullname(user.first_name, user.last_name),
            product_code=product.id,
            product_name=product.name,
            total_amount=product.price,
        ).dict(),
    )
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
