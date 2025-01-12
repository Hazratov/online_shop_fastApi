from fastapi import HTTPException, status, Depends
from typing import Sequence, Optional

from app.api.repositories.product import ProductRepository
from app.api.schemas.product import ProductCreate, ProductUpdate, ProductResponse


class ProductController:
    def __init__(self, product_repo: ProductRepository = Depends()):
        self.product_repo = product_repo

    async def create_product(self, product_data: ProductCreate) -> ProductResponse:
        product = await self.product_repo.create_product(**product_data.dict())
        return product

    async def get_all_products(self) -> Sequence[ProductResponse]:
        return await self.product_repo.get_all_products()

    async def get_product_by_id(self, product_id: int) -> ProductResponse:
        product = await self.product_repo.get_product_by_id(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found",
            )
        return product

    async def update_product(self, product_id: int, update_data: ProductUpdate, partial: bool = True) -> ProductResponse:
        product = await self.product_repo.get_product_by_id(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found",
            )

        # Apply partial or full updates
        for key, value in update_data.dict(exclude_unset=True).items():
            setattr(product, key, value)

        return await self.product_repo.update_product(product)

    async def delete_product(self, product_id: int):
        product = await self.product_repo.get_product_by_id(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found",
            )
        await self.product_repo.delete_product(product)
