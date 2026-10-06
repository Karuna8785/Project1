"""
SmartERP - Security / Auth Stub
Member 2: HR Management Module

NOTE TO MEMBER 1 (Auth Module):
  Replace this stub with your real JWT implementation.
  The `get_current_user` dependency is used throughout the HR module.
  Expected return type: schemas.user.UserOut (or similar).

  Required interface:
    - current_user.id: int
    - current_user.email: str
    - current_user.username: str
    - current_user.role: str  (e.g. "ADMIN", "MANAGER", "EMPLOYEE")
    - current_user.full_name: str
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.config import settings

# ─── Token scheme ────────────────────────────────────────────────────────────
security_scheme = HTTPBearer(auto_error=False)


# ─── Mock user for development (Replace with Member 1's JWT verification) ────
class MockUser:
    """
    Development-only mock user.
    REMOVE or REPLACE when Member 1's auth module is integrated.
    """
    def __init__(self):
        self.id = 1
        self.email = "admin@smarterp.com"
        self.username = "admin"
        self.full_name = "Admin User"
        self.role = "ADMIN"
        self.is_active = True


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
):
    """
    Auth dependency injected into HR routes.

    ── Development Mode ──────────────────────────────────────────────────────
    Returns a MockUser so you can develop the HR module without the auth
    service running.  When Member 1's auth module is ready, replace this
    function body with real JWT verification.

    ── Integration (Member 1 replaces this block) ────────────────────────────
    from app.core.security import verify_token
    from app.services.user_service import get_user_by_id
    ...
    """
    # DEV: Accept any bearer token (or no token) and return mock admin user
    # PROD: Uncomment the block below and delete the mock return
    return MockUser()

    # ── Member 1 integration block (uncomment when ready) ──────────────────
    # if not credentials:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Not authenticated",
    #         headers={"WWW-Authenticate": "Bearer"},
    #     )
    # try:
    #     payload = verify_token(credentials.credentials, settings.SECRET_KEY)
    #     user_id: int = payload.get("sub")
    #     if user_id is None:
    #         raise HTTPException(status_code=401, detail="Invalid token")
    # except Exception:
    #     raise HTTPException(status_code=401, detail="Invalid or expired token")
    # user = await get_user_by_id(user_id)
    # if not user or not user.is_active:
    #     raise HTTPException(status_code=401, detail="User not found or inactive")
    # return user


async def get_current_active_user(
    current_user=Depends(get_current_user),
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def require_roles(*roles: str):
    """Role-based access control dependency factory."""
    async def role_checker(current_user=Depends(get_current_user)):
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {list(roles)}",
            )
        return current_user
    return role_checker


# Convenience role dependencies
require_admin = require_roles("ADMIN")
require_manager_or_admin = require_roles("ADMIN", "MANAGER")
require_any_role = require_roles("ADMIN", "MANAGER", "EMPLOYEE")
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from app.config import settings


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except (ValueError, TypeError):
        return False

def get_password_hash(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None
