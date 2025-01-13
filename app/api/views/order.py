from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.api.controllers.order import OrderController
from app.api.controllers.user import UserController
from app.api.schemas.order import OrderCreateSchema, OrderOutSchema
from app.api.utils.security import get_current_user

order_router = APIRouter(prefix="/orders", tags=["Order"])


@order_router.get("", response_model=List[OrderOutSchema])
async def list_orders(
    current_user=Depends(get_current_user),
    controller: OrderController = Depends(),
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    return await controller.list_orders()


@order_router.get("/{order_id}")
async def get_order(
    order_id: int,
    controller: OrderController = Depends(),
):
    return await controller.get_order_details(order_id)


@order_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_order(
        user_id: int,
        data: OrderCreateSchema,
        controller: OrderController = Depends(),
):
    # Check if the user role is admin based on the input data (optional check)
    if hasattr(data, "role") and data.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    # Process the order creation
    return await controller.create_order(user_id=user_id, data=data)

@order_router.get("/customer/{customer_id}", response_model=List[OrderOutSchema])
async def get_customer_orders(
    customer_id: int,
    current_user=Depends(get_current_user),
    controller: OrderController = Depends(),
):
    if current_user.role == "customer" and current_user.id != customer_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return await controller.list_orders_by_user(customer_id)


@order_router.get("/{order_id}/status")
async def get_order_status(
    order_id: int,
    current_user=Depends(get_current_user),
    controller: OrderController = Depends(),
):
    order = await controller.get_order_by_id(order_id)
    if current_user.role == "customer" and order.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return {"order_id": order.id, "status": order.status}