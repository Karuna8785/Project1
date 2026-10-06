# SmartERP — Enterprise Resource Planning Platform

A modern, production-style Enterprise Resource Planning (ERP) platform built with **FastAPI**, **PostgreSQL / SQLAlchemy**, **React (Vite)**, and **Tailwind CSS**.

---

## 1. Project Overview & Architecture

SmartERP is designed as a scalable, modular enterprise system. The project features clean separation of concerns:
- **Module 1**: Authentication & Security (JWT, RBAC, Passlib/Bcrypt, Security Audit Logging) — **Fully Functional**
- **Member 3 (CRM)**: Customers, Sales Leads Pipeline, and Customer Interaction History — **Fully Functional**
- **Upcoming Modules (Phase 2)**: HR Management, Inventory, Sales, Procurement, Finance, and BI Reports (Designed with clean blueprint endpoints and UI placeholders).

---

## 2. Team Module Allocation

| Team Member | Responsibility | Status | Scope / Features |
|---|---|---|---|
| **Member 1** | **Authentication & Security** | **Active & Functional** | Login, Register, JWT, Roles, Permissions, Security Audit Logs |
| **Member 2** | HR Management | Phase 2 Blueprint | Employees, Departments, Attendance, Leave |
| **Member 3** | **CRM Management** | **Active & Functional** | Customers, Leads Pipeline, Interaction History, Lead Conversion |
| **Member 4** | Inventory | Phase 2 Blueprint | Products, Categories, Warehouses, Stock Tracking |
| **Member 5** | Sales | Phase 2 Blueprint | Quotations, Orders, Invoices, Payments |
| **Member 6** | Procurement & Finance | Phase 2 Blueprint | Suppliers, Purchases, Expenses, General Ledger |
| **Member 7** | Dashboard & Integration | Integrated Baseline | System Overview, Integration Tests, Security Audit Hub |

---

## 3. Technology Stack

### Frontend
- **Framework**: React 18 + Vite
- **Routing**: React Router v6
- **Styling**: Tailwind CSS + Custom Design System
- **Icons**: Lucide React
- **HTTP Client**: Axios with Bearer token interceptor

### Backend
- **Framework**: FastAPI (Python 3.12+)
- **ORM & Database**: SQLAlchemy 2.0 + PostgreSQL / psycopg (with automatic local fallback)
- **Validation**: Pydantic v2
- **Security**: python-jose (JWT HS256), passlib (Bcrypt)
- **Testing**: Pytest + HTTPX TestClient

---

## 4. Default Seed Credentials

SmartERP seeds the database on first run with three pre-configured enterprise accounts:

| Role | Username | Email | Password | Access Rights |
|---|---|---|---|---|
| **ADMIN** | `admin` | `admin@smarterp.com` | `AdminPassword123!` | Full unrestricted access to all modules, users, and audit logs |
| **MANAGER** | `manager` | `manager@smarterp.com` | `ManagerPassword123!` | CRM management, pipeline oversight, user directory view |
| **EMPLOYEE** | `employee` | `employee@smarterp.com` | `EmployeePassword123!` | Customer directory, lead tracking, activity logging, profile |

---

## 5. Quick Start (Windows)

### Option A: One-Click Start
Double click or run:
```cmd
start.bat
```
This automatically launches both the FastAPI backend on port 8000 and the Vite frontend on port 5173 in separate terminal windows.

---

### Option B: Manual Setup & Execution

#### 1. Backend Setup
```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
- API Server: `http://localhost:8000`
- Interactive Swagger Docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

#### 2. Frontend Setup
```powershell
cd frontend
npm install
npm run dev
```
- Web Application: `http://localhost:5173`

---

## 6. Running Automated Tests

Run the complete test suite (24 automated tests covering Authentication, JWT, RBAC permissions, Security Audit logging, and Member 3 CRM functionality):

```powershell
.\backend\.venv\Scripts\pytest tests -v
```

Output:
```
====================== 24 passed in 21.48s =======================
```

---

## 7. Project Directory Structure

```
SmartERP/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── routes/
│   │   │   │   ├── auth.py          # Module 1: Auth endpoints
│   │   │   │   ├── users.py         # Module 1: User & RBAC endpoints
│   │   │   │   ├── audit.py         # Module 1: Audit logs
│   │   │   │   ├── crm.py           # Member 3: CRM endpoints
│   │   │   │   ├── hr.py            # Phase 2 placeholder
│   │   │   │   ├── inventory.py     # Phase 2 placeholder
│   │   │   │   ├── sales.py         # Phase 2 placeholder
│   │   │   │   ├── procurement.py   # Phase 2 placeholder
│   │   │   │   ├── finance.py       # Phase 2 placeholder
│   │   │   │   └── reports.py       # Phase 2 placeholder
│   │   │   └── deps.py              # JWT authentication & RBAC dependencies
│   │   ├── core/
│   │   │   ├── config.py            # Pydantic Settings
│   │   │   └── security.py          # Bcrypt hashing & JWT signing
│   │   ├── database/
│   │   │   ├── session.py           # Engine & Session management
│   │   │   ├── init_db.py           # Database initializer
│   │   │   └── seed.py              # Seed script
│   │   ├── models/                  # SQLAlchemy models (User, Role, Customer, Lead, History)
│   │   ├── schemas/                 # Pydantic validation schemas
│   │   ├── services/                # Business logic services
│   │   ├── middleware/              # Logging middleware
│   │   └── main.py                  # FastAPI application entrypoint
│   ├── requirements.txt
│   ├── .env
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── common/              # Reusable UI components (Button, Input, Card, Modal, Table, Badge, Toast)
│   │   │   └── layout/              # Sidebar, Navbar, Layout
│   │   ├── context/                 # AuthContext & NotificationContext
│   │   ├── hooks/                   # useAuth, useNotification
│   │   ├── pages/
│   │   │   ├── auth/                # Login, Register
│   │   │   ├── dashboard/           # Dashboard overview
│   │   │   ├── profile/             # User profile & security
│   │   │   ├── crm/                 # Member 3 CRM (Customers, Leads, History, Detail)
│   │   │   ├── admin/               # Users & Audit logs
│   │   │   └── placeholders/        # Clean Coming Soon placeholders for upcoming modules
│   │   ├── routes/                  # AppRoutes & ProtectedRoute
│   │   ├── services/                # Axios API clients
│   │   ├── utils/                   # Constants, Formatters, TokenStorage
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── index.html
│
├── database/
│   ├── schema.sql                   # Full PostgreSQL DDL
│   └── seed.sql                     # Initial seed SQL
│
├── docs/
│   ├── ARCHITECTURE.md              # System design & ER diagrams
│   ├── API.md                       # REST API reference
│   ├── AUTH_SECURITY_MODULE.md      # Module 1 guide
│   └── CRM_MODULE.md                # Member 3 CRM guide
│
├── tests/
│   ├── conftest.py                  # Pytest fixtures & test database
│   ├── test_auth.py                 # 11 Authentication tests
│   ├── test_roles_permissions.py    # 5 RBAC tests
│   ├── test_audit_logs.py           # 3 Audit log tests
│   └── test_crm.py                  # 5 Member 3 CRM tests
│
├── .gitignore
├── README.md
└── start.bat
```

---

## 8. License & Standards

Built to enterprise standards. No external paid APIs or third-party cloud services are required. All operations run locally.
