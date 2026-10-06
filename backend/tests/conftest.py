import os

os.environ["DATABASE_URL"] = "sqlite:///./test_auth.db"
os.environ["SECRET_KEY"] = "test-secret-key-that-is-long-enough-for-testing"
os.environ["ADMIN_PASSWORD"] = "StrongAdminPassword1!"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database.base import Base
from app.database.session import get_db
from app.main import app
from app.models import Permission, Role

engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


@pytest.fixture()
def client():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    for name in ("ADMIN", "MANAGER", "EMPLOYEE"):
        db.add(Role(name=name, description=name.title()))
    for code in (
        "AUTH_LOGIN", "AUTH_REGISTER", "USER_CREATE", "USER_READ", "USER_UPDATE",
        "USER_DELETE", "ROLE_CREATE", "ROLE_READ", "ROLE_UPDATE", "ROLE_DELETE", "AUDIT_READ",
    ):
        db.add(Permission(code=code, description=code))
    db.commit()
    for role_name in ("ADMIN", "MANAGER", "EMPLOYEE"):
        role = db.query(Role).filter_by(name=role_name).one()
        if role_name == "ADMIN":
            role.permissions = db.query(Permission).all()
        else:
            role.permissions = [db.query(Permission).filter_by(code=c).one() for c in ("AUTH_LOGIN", "AUTH_REGISTER", "USER_READ")]
    db.commit()
    db.close()

    def override_get_db():
        session = TestingSessionLocal()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        test_client.db_factory = TestingSessionLocal
        yield test_client
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)
