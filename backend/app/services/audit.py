from fastapi import Request
from sqlalchemy.orm import Session

from app.models import AuditLog


def record_audit(
    db: Session,
    request: Request,
    action: str,
    description: str,
    user_id: int | None = None,
) -> None:
    client_ip = request.client.host if request.client else None
    db.add(
        AuditLog(
            user_id=user_id,
            action=action,
            description=description,
            ip_address=client_ip,
        )
    )
