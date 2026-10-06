from sqlalchemy import func

from app.core.config import settings
from app.core.security import hash_password
from app.database.session import SessionLocal
from app.models import Permission, Role, User

PERMISSIONS = {
    "AUTH_LOGIN": "Authenticate to SmartERP",
    "AUTH_REGISTER": "Register a user account",
    "USER_CREATE": "Create users",
    "USER_READ": "Read user and audit information",
    "USER_UPDATE": "Update users",
    "USER_DELETE": "Delete or disable users",
    "ROLE_CREATE": "Create roles",
    "ROLE_READ": "Read roles",
    "ROLE_UPDATE": "Update roles",
    "ROLE_DELETE": "Delete roles",
    "AUDIT_READ": "Read security audit events",
}


def seed() -> None:
    if not settings.admin_password:
        raise RuntimeError("Set ADMIN_PASSWORD in backend/.env before running the seed script.")
    db = SessionLocal()
    try:
        roles: dict[str, Role] = {}
        for role_name, description in (
            ("ADMIN", "Full access to authentication and security"),
            ("MANAGER", "Operational access; security administration is restricted"),
            ("EMPLOYEE", "Basic authenticated user access"),
        ):
            role = db.query(Role).filter(Role.name == role_name).first()
            if role is None:
                role = Role(name=role_name, description=description)
                db.add(role)
            roles[role_name] = role

        permissions: dict[str, Permission] = {}
        for code, description in PERMISSIONS.items():
            permission = db.query(Permission).filter(Permission.code == code).first()
            if permission is None:
                permission = Permission(code=code, description=description)
                db.add(permission)
            permissions[code] = permission
        db.flush()

        roles["ADMIN"].permissions = list(permissions.values())
        roles["MANAGER"].permissions = [
            permissions[code] for code in ("AUTH_LOGIN", "AUTH_REGISTER", "USER_READ")
        ]
        roles["EMPLOYEE"].permissions = [
            permissions[code] for code in ("AUTH_LOGIN", "AUTH_REGISTER", "USER_READ")
        ]

        admin = db.query(User).filter(func.lower(User.email) == settings.admin_email.lower()).first()
        if admin is None:
            admin = User(
                full_name=settings.admin_full_name,
                email=settings.admin_email.lower(),
                username=settings.admin_username,
                hashed_password=hash_password(settings.admin_password),
                roles=[roles["ADMIN"]],
            )
            db.add(admin)
        elif roles["ADMIN"] not in admin.roles:
            admin.roles.append(roles["ADMIN"])
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
