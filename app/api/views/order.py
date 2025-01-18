from fastapi import APIRouter, Depends, Path, Body, status
from typing import List
from fastapi.security import OAuth2PasswordBearer

from app.api.controllers.order import OrderController
from app.api.schemas.order import OrderDetailCreate, OrderResponse

# OAuth2PasswordBearer token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

order_router = APIRouter(prefix="/orders", tags=["Order"])


@order_router.get("/", response_model=List[OrderResponse])
async def get_all_orders(
    token: str = Depends(oauth2_scheme),
    controller: OrderController = Depends()
):
    return await controller.get_all_orders()


@order_router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
    order_data: OrderDetailCreate = Body(...),
    token: str = Depends(oauth2_scheme),
    controller: OrderController = Depends(),
):
    return await controller.create_order(order_data)


@order_router.get("/{order_id}", response_model=OrderResponse)
async def get_order_by_id(
    order_id: int = Path(...),
    token: str = Depends(oauth2_scheme),
    controller: OrderController = Depends(),
):
    return await controller.get_order_by_id(order_id)


@order_router.get("/customer/{customer_id}", response_model=List[OrderResponse])
async def get_orders_by_customer_id(
    customer_id: int = Path(...),
    token: str = Depends(oauth2_scheme),
    controller: OrderController = Depends(),
):
    return await controller.get_orders_by_customer_id(customer_id)


@order_router.get("/{order_id}/status", response_model=str)
async def get_order_status(
    order_id: int = Path(...),
    token: str = Depends(oauth2_scheme),
    controller: OrderController = Depends(),
):
    return await controller.get_order_status(order_id)
