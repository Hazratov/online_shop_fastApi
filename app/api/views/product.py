from fastapi import APIRouter, Depends, Path, Body, status
from typing import List
from fastapi.security import OAuth2PasswordBearer

from app.api.controllers.product import ProductController
from app.api.schemas.product import ProductCreate, ProductUpdate, ProductResponse

# OAuth2PasswordBearer token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

product_router = APIRouter(prefix="/products" , tags=["Product"])


@product_router.get("/", response_model=List[ProductResponse])
async def get_all_products(
    controller: ProductController = Depends()
):
    return await controller.get_all_products()


@product_router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: ProductCreate = Body(...),
    token: str = Depends(oauth2_scheme),
    controller: ProductController = Depends(),
):
    return await controller.create_product(product_data)


@product_router.get("/{product_id}", response_model=ProductResponse)
async def get_product_by_id(
    product_id: int = Path(...),
    controller: ProductController = Depends(),
):
    return await controller.get_product_by_id(product_id)


@product_router.patch("/{product_id}", response_model=ProductResponse)
async def patch_product(
    product_id: int = Path(...),
    update_data: ProductUpdate = Body(...),
    token: str = Depends(oauth2_scheme),
    controller: ProductController = Depends(),
):
    return await controller.update_product(product_id, update_data, partial=True)


@product_router.put("/{product_id}", response_model=ProductResponse)
async def put_product(
    product_id: int = Path(...),
    update_data: ProductUpdate = Body(...),
    token: str = Depends(oauth2_scheme),
    controller: ProductController = Depends(),
):
    return await controller.update_product(product_id, update_data, partial=False)


@product_router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int = Path(...),
    token: str = Depends(oauth2_scheme),
    controller: ProductController = Depends(),
):
    await controller.delete_product(product_id)
