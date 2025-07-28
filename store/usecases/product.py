from datetime import datetime
from decimal import Decimal
from typing import List
from uuid import UUID

import pymongo
from motor.motor_asyncio import AsyncIOMotorClient

from store.core.exceptions import InsertionException, NotFoundException
from store.db.mongo import db_client
from store.models.product import ProductModel
from store.schemas.product import ProductIn, ProductOut, ProductUpdate


class ProductUsecase:
    def __init__(self) -> None:
        self.client: AsyncIOMotorClient = db_client.get()
        self.database = self.client.get_database()
        self.collection = self.database.get_collection("products")

    async def create(self, *, body: ProductIn) -> ProductOut:
        product_model = ProductModel(**body.model_dump())
        try:
            await self.collection.insert_one(product_model.model_dump())
        except pymongo.errors.DuplicateKeyError:
            raise InsertionException(
                message=f"Product with name '{product_model.name}' already exists."
            )
        except Exception as exc:
            raise InsertionException(message=str(exc))

        return ProductOut(**product_model.model_dump())

    async def get(self, *, id: UUID) -> ProductOut:
        result = await self.collection.find_one({"id": id})

        if not result:
            raise NotFoundException(message=f"Product not found with id: {id}")

        return ProductOut(**result)

    async def query(self, price_min: Decimal = None, price_max: Decimal = None) -> List[ProductOut]:
        filter_query = {}
        price_filter = {}

        if price_min:
            price_filter["$gt"] = float(price_min)
        if price_max:
            price_filter["$lt"] = float(price_max)

        if price_filter:
            filter_query["price"] = price_filter

        return [ProductOut(**item) async for item in self.collection.find(filter_query)]

    async def update(self, *, id: UUID, body: ProductUpdate) -> ProductOut:
        update_data = body.model_dump(exclude_none=True)

        if "updated_at" not in update_data:
            update_data["updated_at"] = datetime.utcnow()

        result = await self.collection.find_one_and_update(
            filter={"id": id},
            update={"$set": update_data},
            return_document=pymongo.ReturnDocument.AFTER,
        )

        if not result:
            raise NotFoundException(message=f"Product not found with id: {id}")

        return ProductOut(**result)


product_usecase = ProductUsecase()