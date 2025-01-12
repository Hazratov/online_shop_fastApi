from fastapi import Depends, HTTPException, status
from app.api.repositories.order import OrderRepository
from app.api.repositories.product import ProductRepository
from app.api.models.order import Order, OrderStatus
from app.api.models.ordering_detail import OrderDetail
from app.api.schemas.order import OrderCreateSchema, OrderOutSchema


class OrderController:
    def __init__(
        self,
        order_repo: OrderRepository = Depends(),
        product_repo: ProductRepository = Depends(),
    ):
        self.order_repo = order_repo
        self.product_repo = product_repo

    async def list_orders(self) -> list[Order]:
        return await self.order_repo.list_orders()

    async def get_order_details(self, order_id: int):
        order = await self.order_repo.get_order_by_id(order_id)
        if not order:
            raise HTTPException(404, "Order not found")
        _ = order.order_detail
        order_dict: dict[str, list | object] = {
            "id": order.id,
            "user_id": order.customer_id,
            "status": order.status,
            "total_amount": order.total_amount,
            "created_at": order.order_date,
            "order_details": [],
        }
        for d in order.order_detail:
            order_dict["order_details"].append(
                {
                    "product_id": d.product_id,
                    "quantity": d.quantity,
                    "unit_price": d.unit_price,
                }
            )

        return order_dict

    async def create_order(self, user_id: int, data: OrderCreateSchema):
        try:
            total = 0.0
            details = []
            print(f"Order data received: {data}")

            for item in data.items:
                print(f"Processing item: {item}")
                product = await self.product_repo.get_product_by_id(item.product_id)
                if not product:
                    raise HTTPException(status_code=404, detail="Product not found")
                line_total = product.price * item.quantity
                total += line_total
                detail = OrderDetail(
                    order_id=item.order_id,
                    product_id=item.product_id,
                    quantity=item.quantity,
                    unit_price=product.price,
                    subtotal=line_total,
                )
                details.append(detail)

            print(f"Order details prepared: {details}")
            order = Order(
                customer_id=user_id,
                order_date=data.order_date,
                status=OrderStatus.PENDING.value,
                total_amount=total,
            )
            created_order = await self.order_repo.create_order(order, details)
            fresh_order = await self.order_repo.get_order_by_id(created_order.id)
            print(f"Order created successfully: {fresh_order}")
            return fresh_order
        except Exception as e:
            # Log the error for debugging
            print(f"Error in OrderController.create_order: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    async def get_order_by_id(self, order_id: int) -> Order:
        order = await self.order_repo.get_order_by_id(order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return order

    async def list_orders_by_user(self, user_id: int) -> list[Order]:
        return await self.order_repo.list_orders_by_user(user_id)

    async def get_order_status(self, order_id: int) -> str:
        order = await self.get_order_by_id(order_id)
        return order.status