from sqlalchemy import Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.models.base import Base


class OrderDetail(Base):
    __tablename__ = "order_details"

    order_id: Mapped[int] = mapped_column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_price: Mapped[int] = mapped_column(Float, nullable=False)
    subtotal: Mapped[int] = mapped_column(Float, nullable=False)
    order = relationship("Order", back_populates="order_details")

    # Correct relationship
    order: Mapped["Order"] = relationship(
        "Order",
        back_populates="order_details"
    )