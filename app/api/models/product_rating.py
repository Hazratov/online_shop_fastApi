from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship

from app.core.models.base import Base


class ProductRating(Base):
    __tablename__ = "product_ratings"

    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(String(500))
    rating_date = Column(DateTime, default=datetime.utcnow)

    # Relationships
    product = relationship("Product", back_populates="product_ratings")
    user = relationship("User", back_populates="product_ratings")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.rating < 1 or self.rating > 5:
            raise ValueError("Rating must be between 1 and 5")