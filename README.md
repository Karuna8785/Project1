# SmartERP — HR Management Module (Member 2)

> **Module 2 of 7** in the SmartERP project.
> Covers: **Employees · Departments · Attendance · Leave Management**

---

## Team Module Allocation

| Member | Responsibility | Status |
|---|---|---|
| Member 1 | Authentication & Security | Pending Integration |
| **Member 2** | **HR Management** | ✅ **This Module** |
| Member 3 | CRM | Coming Soon |
| Member 4 | Inventory | Coming Soon |
| Member 5 | Sales | Coming Soon |
| Member 6 | Procurement & Finance | Coming Soon |
| Member 7 | Dashboard & Reports | Coming Soon |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React + Vite + Tailwind CSS |
| Backend | FastAPI + Python |
| ORM | SQLAlchemy |
| Validation | Pydantic v2 |
| Database | PostgreSQL |
| Auth (stub) | JWT stub → Member 1 replaces |
| Testing | Pytest |

---

## Prerequisites

- Python 3.10+
- Node.js 18+
- PostgreSQL 14+

---

## Quick Start (Windows)

Simply double-click **`start.bat`** from the project root.

Or run manually:

---

## Manual Setup

### 1. PostgreSQL — Create Database

```sql
CREATE DATABASE smarterp;
```

### 2. Backend Setup

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 3. Environment Variables

Copy and configure:

```powershell
copy .env.example .env
```

Edit `backend/.env`:

```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/smarterp
SECRET_KEY=your-random-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### 4. Start Backend

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload
```

Tables are created automatically on first run.

### 5. Seed Sample Data (optional)

```powershell
cd backend
python seed.py
```

### 6. Frontend Setup

```powershell
cd frontend
npm install
npm run dev
```

---

## Running URLs

| Service | URL |
|---|---|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:8000 |
| Swagger Docs | http://localhost:8000/docs |
| ReDoc | http://localhost:8000/redoc |

---

## API Endpoints — HR Module

### Departments

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/v1/departments` | List all departments |
| POST | `/api/v1/departments` | Create department |
| GET | `/api/v1/departments/{id}` | Get department |
| PUT | `/api/v1/departments/{id}` | Update department |
| DELETE | `/api/v1/departments/{id}` | Delete department |
| GET | `/api/v1/departments/{id}/employees` | List dept employees |

### Employees

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/v1/employees` | List (search/filter) |
| POST | `/api/v1/employees` | Create employee |
| GET | `/api/v1/employees/{id}` | Get employee |
| PUT | `/api/v1/employees/{id}` | Update employee |
| DELETE | `/api/v1/employees/{id}` | Deactivate (soft) |
| GET | `/api/v1/employees/{id}/attendance` | History |
| GET | `/api/v1/employees/{id}/leaves` | Leave history |
| GET | `/api/v1/employees/summary` | HR stats |

### Attendance

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/v1/attendance` | List (date/emp/status filter) |
| POST | `/api/v1/attendance` | Record attendance |
| GET | `/api/v1/attendance/{id}` | Get record |
| PUT | `/api/v1/attendance/{id}` | Update record |
| DELETE | `/api/v1/attendance/{id}` | Delete record |

### Leave Requests

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/v1/leaves` | List (filter by status/type/emp) |
| POST | `/api/v1/leaves` | Submit request |
| GET | `/api/v1/leaves/{id}` | Get request |
| PUT | `/api/v1/leaves/{id}` | Update pending request |
| POST | `/api/v1/leaves/{id}/review` | Approve / Reject |
| POST | `/api/v1/leaves/{id}/cancel` | Cancel own request |

---

## Database Tables (Member 2)

| Table | Description |
|---|---|
| `departments` | Department records |
| `employees` | Employee records |
| `attendance` | Daily attendance (unique per employee per day) |
| `leave_requests` | Leave applications with approval workflow |

**Does NOT touch Member 1's tables** (`users`, `roles`, `permissions`, `audit_logs`)

---

## Running Tests

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
pytest tests/test_hr.py -v
```

Tests cover:
- Department CRUD + duplicate detection
- Employee CRUD + search + soft-delete
- Attendance with duplicate-date protection
- Leave apply / approve / reject / overlap detection

---

## Auth Integration (for Member 1)

When integrating Member 1's auth:

1. **Backend** — Replace `backend/app/core/security.py` `get_current_user()` body with real JWT verification
2. **Frontend** — Replace `frontend/src/context/AuthContext.jsx` mock user with real JWT context
3. **Frontend** — The `frontend/src/services/api.js` interceptor already reads `localStorage.getItem('access_token')`

---

## Project Structure

```
SmartERP/
├── backend/
│   ├── app/
│   │   ├── api/routes/        # departments, employees, attendance, leaves
│   │   ├── core/              # config, security stub
│   │   ├── database/          # SQLAlchemy engine + session
│   │   ├── models/            # Department, Employee, Attendance, Leave
│   │   ├── schemas/           # Pydantic schemas
│   │   ├── services/          # Business logic
│   │   └── main.py
│   ├── tests/test_hr.py
│   ├── seed.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/        # Sidebar, Navbar, UI kit
│   │   ├── context/           # AuthContext (stub)
│   │   ├── hooks/             # useToast
│   │   ├── layouts/           # MainLayout
│   │   ├── pages/hr/          # HRDashboard, Employees, Departments, Attendance, Leaves
│   │   ├── services/          # api.js, hrService.js
│   │   └── utils/             # helpers, constants
│   ├── package.json
│   └── vite.config.js
├── .gitignore
├── start.bat
└── README.md
```
