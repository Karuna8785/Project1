from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ProductBase(BaseModel):
    product_code: str = Field(..., min_length=2, max_length=50, description="Unique product code (e.g. PRD-001)")
    sku: str = Field(..., min_length=2, max_length=50, description="Unique Stock Keeping Unit (e.g. SKU-ELEC-01)")
    barcode: str | None = Field(None, max_length=100)
    product_name: str = Field(..., min_length=2, max_length=150)
    description: str | None = None
    category_id: int
    unit: str = Field(default="pcs", max_length=30)
    cost_price: Decimal = Field(default=Decimal("0.00"), ge=0, description="Cost price cannot be negative")
    selling_price: Decimal = Field(default=Decimal("0.00"), ge=0, description="Selling price cannot be negative")
    tax_percentage: Decimal = Field(default=Decimal("0.00"), ge=0, le=100, description="Tax percentage between 0 and 100")
    reorder_level: int = Field(default=10, ge=0, description="Reorder threshold >= 0")
    minimum_stock_level: int = Field(default=5, ge=0)
    maximum_stock_level: int = Field(default=1000, ge=0)
    is_active: bool = True

    @field_validator("product_code", "sku")
    @classmethod
    def validate_code_or_sku(cls, v: str) -> str:
        v = v.strip().upper()
        if not v:
            raise ValueError("Code/SKU cannot be blank")
        return v

    @field_validator("product_name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Product name cannot be blank")
        return v

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    product_code: str | None = Field(None, min_length=2, max_length=50)
    sku: str | None = Field(None, min_length=2, max_length=50)
    barcode: str | None = Field(None, max_length=100)
    product_name: str | None = Field(None, min_length=2, max_length=150)
    description: str | None = None
    category_id: int | None = None
    unit: str | None = Field(None, max_length=30)
    cost_price: Decimal | None = Field(None, ge=0)
    selling_price: Decimal | None = Field(None, ge=0)
    tax_percentage: Decimal | None = Field(None, ge=0, le=100)
    reorder_level: int | None = Field(None, ge=0)
    minimum_stock_level: int | None = Field(None, ge=0)
    maximum_stock_level: int | None = Field(None, ge=0)
    is_active: bool | None = None

    @field_validator("product_code", "sku")
    @classmethod
    def validate_code_or_sku(cls, v: str | None) -> str | None:
        if v is not None:
            v = v.strip().upper()
            if not v:
                raise ValueError("Code/SKU cannot be blank")
        return v

    @field_validator("product_name")
    @classmethod
    def validate_name(cls, v: str | None) -> str | None:
        if v is not None:
            v = v.strip()
            if not v:
                raise ValueError("Product name cannot be blank")
        return v

class WarehouseStockSummary(BaseModel):
    warehouse_id: int
    warehouse_name: str
    warehouse_code: str
    quantity_on_hand: int
    reserved_quantity: int
    available_quantity: int

class ProductResponse(ProductBase):
    id: int
    category_name: str | None = None
    total_stock: int = 0
    stock_status: str = "OUT OF STOCK"
    created_by: int | None = None
    created_at: datetime
    updated_at: datetime
    warehouses_stock: list[WarehouseStockSummary] = []

    model_config = ConfigDict(from_attributes=True)

class ProductListResponse(BaseModel):
    total: int
    items: list[ProductResponse]
