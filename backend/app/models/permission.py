from sqlalchemy import Column, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database.base import Base
from app.models.role import role_permissions


class Permission(Base):
    __tablename__ = "permissions"
    __table_args__ = (UniqueConstraint("code", name="uq_permissions_code"),)

    id = Column(Integer, primary_key=True)
    code = Column(String(80), nullable=False, unique=True, index=True)
    description = Column(String(255), nullable=False)
    roles = relationship("Role", secondary=role_permissions, back_populates="permissions")
