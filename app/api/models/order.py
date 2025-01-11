from datetime import datetime
from typing import List
from sqlalchemy import String, Float, DateTime, ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum
from app.core.models.base import Base


class OrderStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"

class Order(Base):
    __tablename__ = "order"

    customer_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    order_date: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    status: Mapped[OrderStatus] = mapped_column(default=OrderStatus.PENDING)
    total_amount: Mapped[float] = mapped_column(Float, nullable=False)
    shipping_address: Mapped[str] = mapped_column(String(200), nullable=False)

    # Relationships
    customer: Mapped["User"] = relationship(back_populates="orders")
    order_details: Mapped[List["OrderDetail"]] = relationship(back_populates="order")
