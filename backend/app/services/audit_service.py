from typing import Optional
from sqlalchemy.orm import Session
from app.models.audit_log import AuditLog

class AuditService:
    @staticmethod
    def log(
        db: Session,
        action: str,
        description: str,
        user_id: Optional[int] = None,
        ip_address: Optional[str] = None
    ) -> AuditLog:
        try:
            log_entry = AuditLog(
                user_id=user_id,
                action=action,
                description=description,
                ip_address=ip_address
            )
            db.add(log_entry)
            db.commit()
            db.refresh(log_entry)
            return log_entry
        except Exception:
            db.rollback()
            return None
