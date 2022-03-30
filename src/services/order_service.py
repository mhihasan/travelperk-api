import asyncio

from sqlalchemy.ext.asyncio import AsyncSession

from src.crud import order_crud
from src.schemas import order_schema
from src.services import product_service, user_service


def user_fullname(first: str, last: str) -> str:
    return f'{first or ""} {last or ""}'.strip()


async def create_order(session: AsyncSession, order: order_schema.OrderBase):
    product, user = await asyncio.gather(
        product_service.fetch_product(order.product_code),
        user_service.fetch_user(order.user_id),
    )

    await order_crud.create_order(
        session,
        order_schema.OrderCreate(
            user_id=user.id,
            customer_fullname=user_fullname(user.first_name, user.last_name),
            product_code=product.id,
            product_name=product.name,
            total_amount=product.price,
        ),
    )
