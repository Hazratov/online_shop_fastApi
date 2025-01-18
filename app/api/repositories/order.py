from typing import Sequence, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import Depends

from app.api.models.order import Order
from app.api.models.ordering_detail import OrderDetail
from app.api.schemas.order import OrderDetailCreate
from app.core.database.postgres.config import get_general_session


class OrderRepository:
    def __init__(self, session: AsyncSession = Depends(get_general_session)):
        self.session = session

    async def create_order(self,  user_id: int, status: str, total_amount: float, details: List[dict]):
        order = Order(user_id=user_id, status=status, total_amount=total_amount)
        self.session.add(order)
        await self.session.commit()
        await self.session.refresh(order)


        for detail_data in details:
            detail = OrderDetailCreate(**detail_data)
            order_detail = OrderDetail(
                order_id=order.id,
                product_id=detail.product_id,
                quantity=detail.quantity,
                unit_price=detail.unit_price,
                subtotal=detail.subtotal
            )
            self.session.add(order_detail)

        await self.session.commit()
        await self.session.refresh(order)

        return order


    async def get_all_orders(self) -> Sequence[Order]:
        result = await self.session.execute(select(Order))
        return result.scalars().all()

    async def get_order_by_id(self, order_id: int) -> Optional[Order]:
        return await self.session.get(Order, order_id)

    async def get_orders_by_customer_id(self, customer_id: int) -> Sequence[Order]:
        result = await self.session.execute(select(Order).where(Order.user_id == customer_id))
        return result.scalars().all()

    async def get_order_status(self, order_id: int) -> Optional[str]:
        result = await self.session.execute(select(Order.status).where(Order.id == order_id))
        return result.scalar()
