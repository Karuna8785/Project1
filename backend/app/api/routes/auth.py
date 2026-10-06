from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import func, or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload

from app.api.deps import get_current_user, require_permission, require_role
from app.core.security import create_access_token, hash_password, verify_password
from app.database.session import get_db
from app.models import AuditLog, Role, User
from app.schemas.auth import (
    LoginRequest,
    MessageResponse,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)
from app.services.audit import record_audit

router = APIRouter(prefix="/auth", tags=["Authentication & Security"])


def serialize_user(user: User) -> UserResponse:
    return UserResponse(
        id=user.id,
        full_name=user.full_name,
        email=user.email,
        username=user.username,
        roles=sorted(user.role_names),
        permissions=sorted(user.permission_codes),
    )


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, request: Request, db: Session = Depends(get_db)):
    normalized_email = str(payload.email).lower()
    normalized_username = payload.username.lower()
    duplicate = (
        db.query(User)
        .filter(or_(func.lower(User.email) == normalized_email, func.lower(User.username) == normalized_username))
        .first()
    )
    if duplicate:
        if duplicate.email.lower() == normalized_email:
            detail = "An account with this email already exists"
        else:
            detail = "This username is already taken"
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=detail)

    employee_role = db.query(Role).filter(Role.name == "EMPLOYEE").first()
    if employee_role is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentication roles are not initialized",
        )
    user = User(
        full_name=payload.full_name.strip(),
        email=normalized_email,
        username=payload.username.strip(),
        hashed_password=hash_password(payload.password),
        roles=[employee_role],
    )
    db.add(user)
    try:
        db.flush()
        record_audit(db, request, "REGISTER", "New user registered", user.id)
        db.commit()
        db.refresh(user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email or username is already in use")
    return serialize_user(user)


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, request: Request, db: Session = Depends(get_db)):
    identifier = payload.identifier.strip().lower()
    user = (
        db.query(User)
        .options(selectinload(User.roles).selectinload(Role.permissions))
        .filter(or_(func.lower(User.email) == identifier, func.lower(User.username) == identifier))
        .first()
    )
    if user is None or not verify_password(payload.password, user.hashed_password) or not user.is_active:
        record_audit(db, request, "LOGIN_FAILED", "Invalid login attempt")
        db.commit()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username/email or password")
    record_audit(db, request, "LOGIN", "User logged in", user.id)
    db.commit()
    return TokenResponse(
        access_token=create_access_token(user.id, user.token_version),
        user=serialize_user(user),
    )


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return serialize_user(current_user)


@router.post("/logout", response_model=MessageResponse)
def logout(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    current_user.token_version += 1
    record_audit(db, request, "LOGOUT", "User logged out; outstanding access tokens invalidated", current_user.id)
    db.commit()
    return MessageResponse(message="Successfully logged out")


@router.get("/protected", response_model=MessageResponse)
def protected_route(current_user: User = Depends(get_current_user)):
    return MessageResponse(message=f"Authenticated as {current_user.username}")


@router.get("/admin-only", response_model=MessageResponse)
def admin_only(current_user: User = Depends(require_role("ADMIN"))):
    return MessageResponse(message="Administrator access granted")


@router.get("/permission-only", response_model=MessageResponse)
def permission_only(current_user: User = Depends(require_permission("USER_DELETE"))):
    return MessageResponse(message="USER_DELETE permission granted")


@router.get("/audit-logs", response_model=list[dict[str, Any]])
def audit_logs(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("AUDIT_READ")),
):
    rows = db.query(AuditLog).order_by(AuditLog.created_at.desc()).limit(100).all()
    return [
        {
            "id": row.id,
            "user_id": row.user_id,
            "action": row.action,
            "description": row.description,
            "ip_address": row.ip_address,
            "created_at": row.created_at,
        }
        for row in rows
    ]
