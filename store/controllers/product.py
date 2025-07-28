from decimal import Decimal
from typing import List
from uuid import UUID

from fastapi import APIRouter, Body, Depends, Path, Query, status

from store.schemas.product import ProductIn, ProductOut, ProductUpdate
from store.usecases.product import ProductUsecase

router = APIRouter(tags=["products"])


@router.post(path="/", status_code=status.HTTP_201_CREATED)
async def post(
    body: ProductIn = Body(...), usecase: ProductUsecase = Depends(ProductUsecase)
) -> ProductOut:
    return await usecase.create(body=body)


@router.get(path="/{id}", status_code=status.HTTP_200_OK)
async def get(
    id: UUID = Path(alias="id"), usecase: ProductUsecase = Depends(ProductUsecase)
) -> ProductOut:
    return await usecase.get(id=id)



@router.get(path="/", status_code=status.HTTP_200_OK)
async def query(
    price_min: Decimal = Query(None, alias="min_price"),
    price_max: Decimal = Query(None, alias="max_price"),
    usecase: ProductUsecase = Depends(ProductUsecase),
) -> List[ProductOut]:
    return await usecase.query(price_min=price_min, price_max=price_max)


@router.patch(path="/{id}", status_code=status.HTTP_200_OK)
async def patch(
    id: UUID = Path(alias="id"),
    body: ProductUpdate = Body(...),
    usecase: ProductUsecase = Depends(ProductUsecase),
) -> ProductOut:
    return await usecase.update(id=id, body=body)