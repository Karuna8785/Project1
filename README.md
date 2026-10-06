# SmartERP — Authentication & Security

SmartERP is an extensible ERP application. This phase implements **Module 1 only**: registration, login, JWT authentication, roles, permissions, audit logging, protected routes, user profile, and logout. HR, CRM, inventory, sales, procurement, finance, and reports are not implemented.

## Stack

- Frontend: React, Vite, React Router, Axios, Tailwind CSS, Lucide
- Backend: FastAPI, SQLAlchemy, Pydantic, Alembic, SQLite
- Security: bcrypt password hashing, signed JWT access tokens, role/permission dependencies

## Project layout

```text
backend/
  app/api/             API dependencies and authentication routes
  app/core/            Settings and security primitives
  app/database/        SQLAlchemy base and sessions
  app/models/          Users, roles, permissions, audit logs
  app/schemas/         Request and response validation
  app/services/        Audit logging
  migrations/          Alembic migration
  tests/               Authentication and authorization tests
frontend/
  src/components/      Auth layout and signed-in application shell
  src/context/         Authentication state and actions
  src/pages/auth/      Login, registration, profile
  src/pages/dashboard/ Protected placeholder dashboard
  src/routes/          Protected route handling
```

## Prerequisites

- Python 3.10+
- Node.js 20+

No Docker or external API keys are required.

## Database

This project uses SQLite, so no database server or database account is needed. The local database file, `backend/smarterp_dev.db`, is created automatically and ignored by Git.

## Backend setup (Windows PowerShell)

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `backend/.env` and set a unique `SECRET_KEY` (at least 32 random characters) and a strong `ADMIN_PASSWORD`. `.env` is ignored by Git.

Apply the schema and seed the three roles, permissions, and development administrator:

```powershell
alembic upgrade head
python -m app.seed
```

The development administrator is configured through `ADMIN_EMAIL`, `ADMIN_USERNAME`, and `ADMIN_PASSWORD`; credentials are not embedded in source files. Change the development password before use outside a local environment.

Run the API:

```powershell
uvicorn app.main:app --reload
```

API: http://localhost:8000  
Swagger: http://localhost:8000/docs  
ReDoc: http://localhost:8000/redoc

## Frontend setup

In another PowerShell:

```powershell
cd frontend
npm install
Copy-Item .env.example .env
npm run dev
```

Frontend: http://localhost:5173. `VITE_API_URL` can be changed in `frontend/.env` when the backend runs elsewhere.

From the project root, `start.bat` opens separate PowerShell windows for the API and Vite development server. The API window migrates and seeds SQLite automatically. Configure `backend/.env` and install frontend dependencies first.

## Authentication API

All endpoints are under `/api/v1`:

| Method | Path | Access | Purpose |
| --- | --- | --- | --- |
| POST | `/auth/register` | Public | Register an EMPLOYEE account |
| POST | `/auth/login` | Public | Exchange email/username and password for an access token |
| GET | `/auth/me` | Authenticated | Return current user, roles, and permissions |
| POST | `/auth/logout` | Authenticated | Invalidate all current access tokens for this user |
| GET | `/auth/protected` | Authenticated | Demonstrate protected access |
| GET | `/auth/admin-only` | ADMIN | Demonstrate role-based access |
| GET | `/auth/permission-only` | `USER_DELETE` | Demonstrate permission-based access |
| GET | `/auth/audit-logs` | `AUDIT_READ` (ADMIN only) | Read the most recent 100 security events |

Registration requires a full name, valid email, username, and a password of at least 10 characters containing uppercase, lowercase, numeric, and symbol characters. Password confirmation is checked and never persisted. Public registration always assigns the EMPLOYEE role; administrative privileges must only be assigned by trusted setup.

Login accepts:

```json
{ "identifier": "user@example.com", "password": "YourStrongPassword1!" }
```

Send the returned token on protected requests as `Authorization: Bearer <access_token>`. Access tokens expire after `ACCESS_TOKEN_EXPIRE_MINUTES` (60 by default). Logout increments the user's token version, invalidating previously issued tokens for that account.

## Roles and permissions

The seed script provisions `ADMIN`, `MANAGER`, and `EMPLOYEE`, plus the `AUTH_LOGIN`, `AUTH_REGISTER`, `USER_*`, `ROLE_*`, and `AUDIT_READ` permissions. ADMIN receives all seeded permissions. MANAGER and EMPLOYEE receive basic authentication and user-read permissions in this phase; audit-log access is restricted to ADMIN. Reusable `require_role(...)` and `require_permission(...)` FastAPI dependencies are in `backend/app/api/deps.py`.

## Audit logging

Registration, successful and failed login attempts, and logout are recorded with the user (when known), action, timestamp, description, and client IP where available. Passwords, hashes, and tokens are not written to audit logs.

## Tests

Run backend tests from `backend/` after installing requirements:

```powershell
pytest
```

Tests use an in-memory SQLite database and require no database service. Run `npm run build` from `frontend/` to check the production frontend build.

## Future module allocation

Planned team responsibility: Member 1 — Authentication & Security; Member 2 — HR; Member 3 — CRM; Member 4 — Inventory; Member 5 — Sales; Member 6 — Procurement & Finance; Member 7 — Dashboard, integration, reports, and analytics. Only Member 1's module is functional at this time.
