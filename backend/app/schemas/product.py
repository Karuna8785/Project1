from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ProductBase(BaseModel):
    sku: str
    name: str
    description: Optional[str] = None
    category: Optional[str] = "General"
    unit: Optional[str] = "Units"
    unit_price: float = 0.0
    cost_price: float = 0.0
    tax_rate: float = 18.0
    stock_quantity: int = 100
    is_active: bool = True


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    sku: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    unit: Optional[str] = None
    unit_price: Optional[float] = None
    cost_price: Optional[float] = None
    tax_rate: Optional[float] = None
    stock_quantity: Optional[int] = None
    is_active: Optional[bool] = None


class ProductOut(ProductBase):
    id: int
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
