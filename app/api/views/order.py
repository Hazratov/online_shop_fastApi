from fastapi import APIRouter, Depends, Path, Body, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from typing import List

from app.api.controllers.order import OrderController
from app.api.schemas.order import OrderCreate, OrderResponse
from app.api.controllers.user  import UserController
from app.api.schemas.auth import UserAlertSchema
from app.core.auth.dependencies import get_current_user

# OAuth2PasswordBearer token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

order_router = APIRouter(prefix="/orders", tags=["Order"])


@order_router.get("/", response_model=List[OrderResponse])
async def get_all_orders(
    current_user: UserAlertSchema = Depends(get_current_user),
    controller: OrderController = Depends(),
):
    return await controller.get_orders_by_customer_id(current_user.id)


@order_router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
    order_data: OrderCreate = Body(...),
    current_user: UserAlertSchema = Depends(get_current_user),
    controller: OrderController = Depends(),
):
    return await controller.create_order(order_data, current_user.id)


@order_router.get("/{order_id}", response_model=OrderResponse)
async def get_order_by_id(
    order_id: int = Path(...),
    current_user: UserAlertSchema = Depends(get_current_user),
    controller: OrderController = Depends(),
):
    order = await controller.get_order_by_id(order_id)
    if order.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied.")
    return order



@order_router.get("/customer/{customer_id}", response_model=List[OrderResponse])
async def get_orders_by_customer_id(
    customer_id: int = Path(...),
    current_user: UserAlertSchema = Depends(get_current_user),
    controller: OrderController = Depends(),
):
    return await controller.get_orders_by_customer_id(customer_id)


@order_router.get("/{order_id}/status", response_model=str)
async def get_order_status(
    order_id: int = Path(...),
    current_user: UserAlertSchema = Depends(get_current_user),
    controller: OrderController = Depends(),
):
    order = await controller.get_order_by_id(order_id)
    if order.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied.")
    return await controller.get_order_status(order_id)
