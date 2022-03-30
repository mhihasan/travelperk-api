import enum

import sqlalchemy as sa

from src.core.db.base import Base


class OrderStatus(enum.Enum):
    initiated = "initiated"
    processing = "processing"
    finished = "finished"
    failed = "failed"


class Order(Base):
    __tablename__ = "order"

    id = sa.Column(sa.String, primary_key=True)
    user_id = sa.Column(sa.String, nullable=False)
    customer_fullname = sa.Column(sa.String, nullable=True)
    product_code = sa.Column(sa.String, nullable=False)
    product_name = sa.Column(sa.String, nullable=True)
    total_amount = sa.Column(sa.Float, default=0.0)
    status = sa.Column(sa.String, default=OrderStatus.initiated.value)
    created_at = sa.Column(sa.DateTime, default=sa.func.now())
