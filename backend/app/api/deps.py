from collections.abc import Callable

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session, selectinload

from app.core.security import decode_access_token
from app.database.session import get_db
from app.models import Role, User

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if credentials is None:
        raise unauthorized
    try:
        payload = decode_access_token(credentials.credentials)
        user_id = int(payload["sub"])
        token_version = int(payload["ver"])
    except (ValueError, KeyError, TypeError):
        raise unauthorized

    user = (
        db.query(User)
        .options(selectinload(User.roles).selectinload(Role.permissions))
        .filter(User.id == user_id)
        .first()
    )
    if user is None or not user.is_active or user.token_version != token_version:
        raise unauthorized
    return user


def require_role(*allowed_roles: str) -> Callable:
    def role_dependency(current_user: User = Depends(get_current_user)) -> User:
        if not set(allowed_roles).intersection(current_user.role_names):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient role")
        return current_user

    return role_dependency


def require_permission(permission_code: str) -> Callable:
    def permission_dependency(current_user: User = Depends(get_current_user)) -> User:
        if permission_code not in current_user.permission_codes:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permission")
        return current_user

    return permission_dependency
