from fastapi import Depends
from typing import List, Optional, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.api.models.order import Order
from app.api.models.ordering_detail import OrderDetail
from app.core.database.postgres.config import get_general_session


class OrderRepository:
    def __init__(self, session: AsyncSession = Depends(get_general_session)):
        self.session = session

    async def list_orders(self) -> Sequence[Order]:
        stmt = select(Order).options(selectinload(Order.order_details))
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create_order(self, order: Order, details: List[OrderDetail]) -> Order:
        self.session.add(order)
        await self.session.flush()

        for detail in details:
            detail.order_id = order.id  # fix: set the FK
            self.session.add(detail)

        await self.session.commit()
        await self.session.refresh(order)
        return order

    async def get_order_by_id(self, order_id: int) -> Optional[Order]:
        stmt = (
            select(Order)
            .where(Order.id == order_id)
            .options(selectinload(Order.order_details))  # or joinedload
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def list_orders_by_user(self, user_id: int) -> List[Order]:
        stmt = (
            select(Order)
            .where(Order.user_id == user_id)
            .options(selectinload(Order.order_details))
        )
        result = await self.session.execute(stmt)
        order = result.scalar_one_or_none()
        order = await self.session.get(Order, id)
        if order:
            await self.session.refresh(order, ["order_details"])
        return order

    async def update_order(self, order: Order) -> Order:
        self.session.add(order)
        await self.session.commit()
        await self.session.refresh(order)
        return order