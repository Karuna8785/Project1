# SmartERP — Enterprise Resource Planning System

SmartERP is a modular, high-performance Enterprise Resource Planning (ERP) platform designed for commercial excellence, security, CRM, inventory tracking, HR management, and seamless cross-module workflows.

## 1. Team Module Allocation & Status

| Module | Owner | Scope & Deliverables | Status |
|---|---|---|---|
| **Authentication & Security** | Member 1 | Login, Register, JWT, Roles (`ADMIN`, `MANAGER`, `EMPLOYEE`), RBAC, Security Audit Logs | ✅ **Active** |
| **HR Management** | Member 2 | Employees, Departments, Attendance Tracking, Leave Approvals | ✅ **Active** |
| **CRM** | Member 3 | Customers, Leads, Interaction History, Pipelines | ✅ **Active** |
| **Inventory Management** | Member 4 | Products, Categories, Multi-Warehouse Stock, Movements, Low Stock Alerts | ✅ **Active** |
| **Sales Management** | **Member 5** | **Quotations, Sales Orders, Commercial Invoices, Payment Collections, Pipeline Analytics, Voucher/Invoice Printing** | ✅ **Active** |
| **Procurement & Finance** | Member 6 | Suppliers, Purchase Orders, Line Items, Expenses, General Ledger | 📋 Planned |
| **Dashboard & Reports** | Member 7 | Cross-module executive analytics, consolidated KPI reporting | 📋 Planned |

---

## 2. Technology Stack

### Frontend
- **React 18 / 19** + **Vite**
- **JavaScript (ES6+)**
- **React Router v7**
- **Tailwind CSS** (Custom enterprise theme, dark mode, responsive glassmorphism)
- **Lucide React** (Modern enterprise icons)
- **Axios** (API client with automatic JWT bearer interceptor)

### Backend
- **Python 3.10+** (Python 3.12 recommended)
- **FastAPI** (Asynchronous, high-performance REST API)
- **SQLAlchemy 2.0** ORM
- **Pydantic V2** (Type validation and schemas)
- **PostgreSQL** (Production database) with **SQLite** auto-fallback for zero-config local development
- **python-jose / PyJWT** (JWT authentication)
- **bcrypt** (Secure salted password hashing)
- **Pytest & HTTPX** (Automated integration test suites)

---

## 3. Getting Started (Windows)

### 1-Click Launch (Recommended)
Double-click `start.bat` from the root directory or run in terminal:
```cmd
start.bat
```
This automatically launches both backend and frontend servers in separate windows.

---

### Manual Setup

#### 1. Backend Setup
```powershell
cd backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
.\.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
- Backend API: `http://localhost:8000`
- Interactive Swagger Docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

#### 2. Frontend Setup
```powershell
cd frontend

# Install packages
npm install

# Start Vite dev server
npm run dev
```
- Frontend Portal: `http://localhost:5173`

---

## 4. Pre-Configured Demo Credentials

| Role | Username | Password | Access Level |
|---|---|---|---|
| **Administrator** | `admin` | `Admin@123` | Full system access, audit logs, all modules |
| **Sales Manager** | `salesmgr` | `Manager@123` | Full sales lifecycle, quotations, orders, invoices, payments |

---

## 5. Automated Test Suites

Run automated pytest suites:
```powershell
# Sales module tests
.\backend\.venv\Scripts\python -m pytest -v tests/

# Cross-module (Auth, HR, Inventory, CRM) tests
.\backend\.venv\Scripts\python -m pytest -v backend/tests/
```
