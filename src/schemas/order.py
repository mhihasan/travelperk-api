from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class OrderInSchema(BaseModel):
    user_id: str = Field(..., min_length=3)
    product_code: str = Field(..., min_length=3)


class OrderInResponseSchema(OrderInSchema):
    id: str
    status: str
    created_at: datetime


class OrderSchema(OrderInSchema):
    created_at: datetime
    customer_fullname: Optional[str]
    product_name: Optional[str]
    total_amount: Optional[float]
    status: str


class OrderInDbSchema(OrderSchema):
    id: str
