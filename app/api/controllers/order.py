from fastapi import HTTPException, status, Depends
from typing import Sequence, Optional

from app.api.repositories.order import OrderRepository
from app.api.schemas.order import OrderCreate, OrderResponse


class OrderController:
    def __init__(self, order_repo: OrderRepository = Depends()):
        self.order_repo = order_repo

    async def create_order(self, order_data: OrderCreate) -> OrderResponse:
        order = await self.order_repo.create_order(**order_data.dict())
        return order

    async def get_all_orders(self) -> Sequence[OrderResponse]:
        return await self.order_repo.get_all_orders()

    async def get_order_by_id(self, order_id: int) -> OrderResponse:
        order = await self.order_repo.get_order_by_id(order_id)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found",
            )
        return order

    async def get_orders_by_customer_id(self, customer_id: int) -> Sequence[OrderResponse]:
        orders = await self.order_repo.get_orders_by_customer_id(customer_id)
        if not orders:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No orders found for the customer",
            )
        return orders

    async def get_order_status(self, order_id: int) -> str:
        status_value = await self.order_repo.get_order_status(order_id)
        if not status_value:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found or status unavailable",
            )
        return status_value
