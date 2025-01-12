from datetime import datetime
from typing import List

from pydantic import Field, BaseModel
from app.api.models.order import OrderStatus
from app.api.schemas.ordering_detail import OrderDetailResponse, OrderDetailCreate


class OrderBase(BaseModel):
    shipping_address: str = Field(..., max_length=200)

class OrderCreate(OrderBase):
    order_details: List[OrderDetailCreate]

class OrderResponse(OrderBase):
    id: int
    customer_id: int
    order_date: datetime
    status: OrderStatus
    total_amount: float
    order_details: List[OrderDetailResponse]

    class Config:
        from_attributes = True
