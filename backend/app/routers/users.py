from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User, Role
from app.schemas.user import UserResponse
from app.dependencies import get_current_user, require_permission

router = APIRouter(prefix="/users", tags=["User Management"])

@router.get("", response_model=List[UserResponse])
def get_all_users(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("USER_READ"))
):
    users = db.query(User).offset(skip).limit(limit).all()
    return [
        UserResponse(
            id=u.id,
            email=u.email,
            username=u.username,
            full_name=u.full_name,
            is_active=u.is_active,
            is_superuser=u.is_superuser,
            created_at=u.created_at,
            roles=[r for r in u.roles],
            permissions=list(u.permissions)
        )
        for u in users
    ]

@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("USER_READ"))
):
    u = db.query(User).filter(User.id == user_id).first()
    if not u:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse(
        id=u.id,
        email=u.email,
        username=u.username,
        full_name=u.full_name,
        is_active=u.is_active,
        is_superuser=u.is_superuser,
        created_at=u.created_at,
        roles=[r for r in u.roles],
        permissions=list(u.permissions)
    )
