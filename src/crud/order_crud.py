import uuid
from typing import Optional, Any

from sqlalchemy import select, insert, update

from src.db.init_db import database
from src.models.order import order_table


async def post_order(order: dict[str, Any]) -> dict[str, Any]:
    order_id = str(uuid.uuid4())

    query = insert(order_table).values(id=order_id, **order)
    await database.execute(query=query)

    created_order: Optional[dict[str, Any]] = await get_order(order_id)
    if created_order is None:
        raise Exception("Error on creating order")

    return created_order


async def get_order(order_id: str) -> Optional[dict[str, Any]]:
    query = select(order_table).where(order_table.c.id == order_id)

    order = await database.fetch_one(query=query)
    if order is None:
        return None

    return {
        "id": order["id"],
        "user_id": order["user_id"],
        "customer_fullname": order["customer_fullname"],
        "product_code": order["product_code"],
        "product_name": order["product_name"],
        "total_amount": order["total_amount"],
        "created_at": order["created_at"],
        "status": order["status"],
    }


async def list_orders(page_no: int = 1, per_page: int = 10) -> list[dict[str, Any]]:
    query = select(order_table).offset(per_page * (page_no - 1)).limit(per_page)
    orders = await database.fetch_all(query=query)
    return [
        {
            "id": order["id"],
            "user_id": order["user_id"],
            "customer_fullname": order["customer_fullname"],
            "product_code": order["product_code"],
            "product_name": order["product_name"],
            "total_amount": order["total_amount"],
            "created_at": order["created_at"],
            "status": order["status"],
        }
        for order in orders
    ]


async def put_order(order_id: str, payload: dict[str, Any]) -> None:
    query = update(order_table).where(order_table.c.id == order_id).values(**payload)
    await database.execute(query=query)
