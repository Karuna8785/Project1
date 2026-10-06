from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr, field_validator, ConfigDict

class WarehouseBase(BaseModel):
    warehouse_code: str = Field(..., min_length=2, max_length=50, description="Unique warehouse code (e.g. WH-MAIN)")
    warehouse_name: str = Field(..., min_length=2, max_length=100, description="Warehouse name")
    description: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    is_active: bool = True

    @field_validator("warehouse_code")
    @classmethod
    def validate_code(cls, v: str) -> str:
        v = v.strip().upper()
        if not v:
            raise ValueError("Warehouse code cannot be blank")
        return v

    @field_validator("warehouse_name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Warehouse name cannot be blank")
        return v

class WarehouseCreate(WarehouseBase):
    pass

class WarehouseUpdate(BaseModel):
    warehouse_code: Optional[str] = Field(None, min_length=2, max_length=50)
    warehouse_name: Optional[str] = Field(None, min_length=2, max_length=100)
    description: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = None

    @field_validator("warehouse_code")
    @classmethod
    def validate_code(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            v = v.strip().upper()
            if not v:
                raise ValueError("Warehouse code cannot be blank")
        return v

    @field_validator("warehouse_name")
    @classmethod
    def validate_name(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            v = v.strip()
            if not v:
                raise ValueError("Warehouse name cannot be blank")
        return v

class WarehouseStockItem(BaseModel):
    product_id: int
    product_name: str
    product_code: str
    sku: str
    unit: str
    category_name: Optional[str] = None
    quantity_on_hand: int
    reserved_quantity: int
    available_quantity: int
    reorder_level: int
    stock_status: str

    model_config = ConfigDict(from_attributes=True)

class WarehouseResponse(WarehouseBase):
    id: int
    total_products_count: int = 0
    total_units_in_stock: int = 0
    low_stock_products_count: int = 0
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class WarehouseDetailResponse(WarehouseResponse):
    stock_items: List[WarehouseStockItem] = []

class WarehouseListResponse(BaseModel):
    total: int
    items: List[WarehouseResponse]
