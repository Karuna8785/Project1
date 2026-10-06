from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator

class CategoryBase(BaseModel):
    category_code: str = Field(..., min_length=2, max_length=50, description="Unique category code (e.g. CAT-ELEC)")
    category_name: str = Field(..., min_length=2, max_length=100, description="Category name")
    description: Optional[str] = None
    parent_category_id: Optional[int] = None
    is_active: bool = True

    @field_validator("category_code")
    @classmethod
    def validate_code(cls, v: str) -> str:
        v = v.strip().upper()
        if not v:
            raise ValueError("Category code cannot be blank")
        return v

    @field_validator("category_name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Category name cannot be blank")
        return v

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    category_code: Optional[str] = Field(None, min_length=2, max_length=50)
    category_name: Optional[str] = Field(None, min_length=2, max_length=100)
    description: Optional[str] = None
    parent_category_id: Optional[int] = None
    is_active: Optional[bool] = None

    @field_validator("category_code")
    @classmethod
    def validate_code(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            v = v.strip().upper()
            if not v:
                raise ValueError("Category code cannot be blank")
        return v

    @field_validator("category_name")
    @classmethod
    def validate_name(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            v = v.strip()
            if not v:
                raise ValueError("Category name cannot be blank")
        return v

class CategoryResponse(CategoryBase):
    id: int
    product_count: int = 0
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class CategoryListResponse(BaseModel):
    total: int
    items: List[CategoryResponse]
