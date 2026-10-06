
from app.models.audit_log import AuditLog
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session


class AuditService:
    @staticmethod
    def log(
        db: Session,
        action: str,
        description: str,
        user_id: int | None = None,
        ip_address: str | None = None
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
        except SQLAlchemyError:
            db.rollback()
            return None
