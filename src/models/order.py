import enum

import sqlalchemy as sa

from src.db.init_db import metadata


class OrderStatus(enum.Enum):
    initiated = "initiated"
    processing = "processing"
    finished = "finished"
    failed = "failed"


order_table = sa.Table(
    "order",
    metadata,
    sa.Column("id", sa.String, primary_key=True),
    sa.Column("user_id", sa.String, nullable=False),
    sa.Column("product_code", sa.String, nullable=False),
    sa.Column("customer_fullname", sa.String, nullable=True),
    sa.Column("product_name", sa.String, nullable=True),
    sa.Column("total_amount", sa.Float, default=0),
    sa.Column("created_at", sa.DateTime, default=sa.func.now()),
    sa.Column("status", sa.String, default=OrderStatus.initiated.value),
)
