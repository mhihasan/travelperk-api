from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class OrderBase(BaseModel):
    user_id: str = Field(..., min_length=3)
    product_code: str = Field(..., min_length=3)


class OrderCreate(OrderBase):
    pass


class Order(OrderBase):
    id: str
    created_at: datetime
    customer_fullname: Optional[str]
    product_name: Optional[str]
    total_amount: Optional[float]
    status: str

    class Config:
        orm_mode = True
