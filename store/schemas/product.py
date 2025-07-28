from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field
from store.core.mixins import BaseSchemaMixin


class ProductBase(BaseModel):
    name: str = Field(..., description="Product name")
    quantity: int = Field(..., description="Product quantity")
    price: Decimal = Field(..., description="Product price")
    status: bool = Field(..., description="Product status")


class ProductIn(ProductBase):
    """Schema for creating a product (input)."""

    pass


class ProductOut(ProductIn, BaseSchemaMixin):
    """Schema for representing a product (output)."""

    pass


class ProductUpdate(BaseModel):
    """Schema for updating a product (all fields are optional)."""

    quantity: Optional[int] = Field(None, description="Product quantity")
    price: Optional[Decimal] = Field(None, description="Product price")
    status: Optional[bool] = Field(None, description="Product status")
    updated_at: Optional[datetime] = Field(None, description="Timestamp of the last update")