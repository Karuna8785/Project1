from typing import Optional
from sqlalchemy.orm import Session
from app.models.user import AuditLog


def log_audit_event(
    db: Session,
    action: str,
    user_id: Optional[int] = None,
    details: Optional[str] = None,
    ip_address: Optional[str] = None,
) -> AuditLog:
    """Record an audit trail event for security and compliance."""
    log = AuditLog(
        user_id=user_id,
        action=action,
        details=details,
        ip_address=ip_address,
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log
