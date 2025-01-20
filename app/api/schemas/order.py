from pydantic import BaseModel, Field
from typing import List
from datetime import datetime


class OrderDetailCreate(BaseModel):
    product_id: int
    quantity: int
    unit_price: float
    subtotal: float


class OrderCreate(BaseModel):
    status: str
    total_amount: float
    details: List[OrderDetailCreate]


class OrderResponse(BaseModel):
    id: int = Field(..., description="Order ID")
    status: str
    total_amount: float
    created_at: datetime
    details: List[OrderDetailCreate]

    class Config:
        orm_mode = True