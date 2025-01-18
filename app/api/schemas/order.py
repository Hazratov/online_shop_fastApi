from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class OrderDetailCreate(BaseModel):
    product_id: int
    quantity: int
    unit_price: float
    subtotal: float

class OrderCreate(BaseModel):
    user_id: int
    status: str
    total_amount: float
    details: List[OrderDetailCreate]


class OrderResponse(OrderDetailCreate):
    id: int = Field(..., description="Order ID")
    created_at: datetime = Field(..., description="Order creation time")

    class Config:
        orm_mode = True
