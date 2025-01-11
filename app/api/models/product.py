from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Float, DateTime, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.models.base import Base

class Product(Base):
    __tablename__ = 'product'

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(500))
    price: Mapped[float] = mapped_column(Float, nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    stock_quantity: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # Relationships
    order_details: Mapped[List["OrderDetail"]] = relationship(back_populates="product")