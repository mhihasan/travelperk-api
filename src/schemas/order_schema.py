from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from src.models.order_model import OrderStatus


class OrderBase(BaseModel):
    user_id: str = Field(..., min_length=3)
    product_code: str = Field(..., min_length=3)
    status: str = OrderStatus.initiated.value


class OrderCreate(OrderBase):
    customer_fullname: Optional[str]
    product_name: Optional[str]
    total_amount: Optional[float]


class Order(OrderBase):
    id: str
    created_at: datetime
    customer_fullname: Optional[str]
    product_name: Optional[str]
    total_amount: Optional[float]

    class Config:
        orm_mode = True
