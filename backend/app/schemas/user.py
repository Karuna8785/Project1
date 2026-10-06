from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, ConfigDict

class PermissionResponse(BaseModel):
    id: int
    name: str
    code: str
    module: str

    model_config = ConfigDict(from_attributes=True)

class RoleResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    permissions: List[PermissionResponse] = []

    model_config = ConfigDict(from_attributes=True)

class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: str
    is_active: bool = True

class UserCreate(UserBase):
    password: str
    roles: Optional[List[str]] = []

class UserResponse(UserBase):
    id: int
    is_superuser: bool
    created_at: datetime
    roles: List[RoleResponse] = []
    permissions: List[str] = []

    model_config = ConfigDict(from_attributes=True)

class LoginRequest(BaseModel):
    username_or_email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
