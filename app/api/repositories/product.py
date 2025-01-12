from typing import Sequence, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import Depends

from app.api.models.product import Product
from app.core.database.postgres.config import get_general_session


class ProductRepository:
    def __init__(self, session: AsyncSession = Depends(get_general_session)):
        self.session = session

    async def create_product(self, **kwargs) -> Product:
        product = Product(**kwargs)
        self.session.add(product)
        await self.session.commit()
        await self.session.refresh(product)
        return product

    async def get_all_products(self) -> Sequence[Product]:
        result = await self.session.execute(select(Product))
        return result.scalars().all()

    async def get_product_by_id(self, product_id: int) -> Optional[Product]:
        return await self.session.get(Product, product_id)

    async def update_product(self, product: Product) -> Product:
        self.session.add(product)
        await self.session.commit()
        await self.session.refresh(product)
        return product

    async def delete_product(self, product: Product):
        await self.session.delete(product)
        await self.session.commit()
