from app.core.security import hash_password, verify_password
from app.models import AuditLog, Role, User

REGISTER = {
    "full_name": "Taylor Employee",
    "email": "taylor@example.com",
    "username": "taylor",
    "password": "StrongPassword1!",
    "confirm_password": "StrongPassword1!",
}


def register(client, **updates):
    return client.post("/api/v1/auth/register", json={**REGISTER, **updates})


def login(client, identifier="taylor@example.com", password="StrongPassword1!"):
    return client.post("/api/v1/auth/login", json={"identifier": identifier, "password": password})


def test_register_hashes_password_and_assigns_employee_role(client):
    response = register(client)
    assert response.status_code == 201
    assert response.json()["roles"] == ["EMPLOYEE"]

    with client.db_factory() as db:
        user = db.query(User).filter_by(email="taylor@example.com").one()
        assert user.hashed_password != REGISTER["password"]
        assert verify_password(REGISTER["password"], user.hashed_password)
    assert "hashed_password" not in response.json()


def test_duplicate_email_and_username_are_rejected(client):
    assert register(client).status_code == 201
    assert register(client, username="another").status_code == 409
    assert register(client, email="another@example.com").status_code == 409


def test_invalid_password_and_confirmation_are_rejected(client):
    assert register(client, password="weak", confirm_password="weak").status_code == 422
    assert register(client, confirm_password="DifferentPassword1!").status_code == 422


def test_login_me_and_protected_routes(client):
    register(client)
    response = login(client, identifier="taylor")
    assert response.status_code == 200
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    assert client.get("/api/v1/auth/me", headers=headers).json()["username"] == "taylor"
    assert client.get("/api/v1/auth/protected", headers=headers).status_code == 200
    assert client.get("/api/v1/auth/admin-only", headers=headers).status_code == 403
    assert client.get("/api/v1/auth/permission-only", headers=headers).status_code == 403


def test_admin_manager_and_permission_authorization(client):
    register(client)
    with client.db_factory() as db:
        for username, role_name in (("admin-user", "ADMIN"), ("manager-user", "MANAGER")):
            role = db.query(Role).filter_by(name=role_name).one()
            db.add(
                User(
                    full_name=username,
                    email=f"{username}@example.com",
                    username=username,
                    hashed_password=hash_password("StrongPassword1!"),
                    roles=[role],
                )
            )
        db.commit()
    admin_token = login(client, "admin-user").json()["access_token"]
    manager_token = login(client, "manager-user").json()["access_token"]
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    manager_headers = {"Authorization": f"Bearer {manager_token}"}
    assert client.get("/api/v1/auth/admin-only", headers=admin_headers).status_code == 200
    assert client.get("/api/v1/auth/permission-only", headers=admin_headers).status_code == 200
    assert client.get("/api/v1/auth/admin-only", headers=manager_headers).status_code == 403
    assert client.get("/api/v1/auth/permission-only", headers=manager_headers).status_code == 403


def test_failed_login_is_audited(client):
    response = login(client, password="WrongPassword1!")
    assert response.status_code == 401
    with client.db_factory() as db:
        assert db.query(AuditLog).filter_by(action="LOGIN_FAILED").count() == 1


def test_logout_revokes_access_token(client):
    register(client)
    token = login(client).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    assert client.post("/api/v1/auth/logout", headers=headers).status_code == 200
    assert client.get("/api/v1/auth/me", headers=headers).status_code == 401


def test_invalid_token_is_rejected(client):
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": "Bearer not-a-valid-token"},
    )
    assert response.status_code == 401


def test_unauthorized_access_and_audit_logs(client):
    assert client.get("/api/v1/auth/protected").status_code == 401
    register(client)
    employee_token = login(client).json()["access_token"]
    assert client.get(
        "/api/v1/auth/audit-logs",
        headers={"Authorization": f"Bearer {employee_token}"},
    ).status_code == 403
    with client.db_factory() as db:
        admin_role = db.query(Role).filter_by(name="ADMIN").one()
        db.add(
            User(
                full_name="Audit Administrator",
                email="audit-admin@example.com",
                username="audit-admin",
                hashed_password=hash_password("StrongPassword1!"),
                roles=[admin_role],
            )
        )
        db.commit()
    admin_token = login(client, "audit-admin").json()["access_token"]
    response = client.get(
        "/api/v1/auth/audit-logs",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    assert any(row["action"] == "REGISTER" for row in response.json())
