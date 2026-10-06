# SmartERP — Enterprise Resource Planning System

SmartERP is a modular, high-performance Enterprise Resource Planning (ERP) platform designed for commercial excellence, security, and seamless cross-module workflows.

> **Current Implementation Phase**: 
> **Member 5: Sales Management Module** (Quotations, Sales Orders, Invoices, Payments, and Financial Analytics) is **fully implemented, tested, and operational**, built on top of the Member 1 Authentication & Security foundation and master catalog data.

---

## 1. Team Module Allocation

| Member | Responsibility | Status | Scope / Deliverable |
|---|---|---|---|
| **Member 1** | Authentication & Security | **Functional** | Login, Register, JWT, Roles (`ADMIN`, `MANAGER`, `EMPLOYEE`), RBAC, Security Audit Logs |
| **Member 2** | HR Management | Planned | Employees, Departments, Attendance, Leave |
| **Member 3** | CRM | Planned (Master Integrated) | Customers, Leads, Interaction History |
| **Member 4** | Inventory | Planned (Master Integrated) | Products, SKUs, Categories, Warehouses, Stock Movements |
| **Member 5** | **Sales Management** | **FULLY IMPLEMENTED** | **Quotations, Sales Orders, Commercial Invoices, Payment Collections, Pipeline Analytics, Voucher/Invoice Printing** |
| **Member 6** | Procurement & Finance | Planned | Suppliers, Purchase Orders, Expenses, General Ledger |
| **Member 7** | Dashboard & Integration | Planned | Cross-module analytics, executive reporting |

---

## 2. Technology Stack

### Frontend
- **React 18** + **Vite**
- **JavaScript (ES6+)**
- **React Router v6**
- **Tailwind CSS** (Custom enterprise theme, glassmorphism, responsive)
- **Lucide React** (Modern enterprise icons)
- **Axios** (API client with automatic JWT bearer interceptor)

### Backend
- **Python 3.12**
- **FastAPI** (Asynchronous, high performance)
- **SQLAlchemy 2.0** ORM
- **Pydantic V2** (Type validation and schemas)
- **PostgreSQL** (Production database) with **SQLite** auto-fallback for zero-config local development
- **python-jose** (JWT creation and signature validation)
- **bcrypt** (Secure salted password hashing)
- **Pytest** (Automated unit and integration test suites)

### Constraints Respected
- **No Docker required** — Runs 100% locally on Windows.
- **No external paid API keys required** — 100% self-hosted and privacy-respecting.

---

## 3. Member 5: Sales Module Architecture & Features

### 3.1. Quotations (Estimates & Proposals)
- Generate sequential quote numbers (`QT-2026-0001`).
- Customer selection from CRM master data or ad-hoc entry.
- Dynamic line items with real-time computation:
  - Unit Price, Quantity, Discount %, GST/Tax %
  - Automatic Subtotal, Total Discount, Tax Amount, and Grand Total.
- Status workflow: `Draft` &rarr; `Sent` &rarr; `Accepted` &rarr; `Rejected`.
- **One-Click Conversion**: Convert accepted quotation directly into an active Sales Order.
- Official printable quotation preview with company header.

### 3.2. Sales Orders (Fulfilment Bookings)
- Sequential order numbering (`SO-2026-0001`).
- Shipping and billing address management.
- Expected delivery scheduling.
- Lifecycle tracking: `Draft` &rarr; `Confirmed` &rarr; `Processing` &rarr; `Shipped` &rarr; `Delivered` &rarr; `Cancelled`.
- **One-Click Invoicing**: Generate commercial accounts receivable invoice directly from the sales order.
- Printable order picking slip.

### 3.3. Invoices (Accounts Receivable)
- Sequential invoice numbering (`INV-2026-0001`).
- Due date tracking with automatic `Overdue` flagging.
- Real-time balance calculations: `Total Amount`, `Amount Paid`, and `Balance Due`.
- Statuses: `Unpaid`, `Partially Paid`, `Paid`, `Overdue`.
- Direct "Collect Payment" trigger.
- Official printable tax invoice with GST breakdown and signature box.

### 3.4. Payments & Collections
- Sequential receipt vouchers (`PAY-2026-0001`).
- Multi-channel payment recording:
  - Bank Transfer (NEFT/RTGS/IMPS)
  - UPI (Unified Payments Interface)
  - Credit / Debit Cards
  - Cash
  - Bank Cheques
- Real-time auto-settlement: Recording payment automatically recalculates target invoice `amount_paid` and `balance_due`, and updates invoice status to `Paid` or `Partially Paid`.
- Printable payment acknowledgement receipt voucher.

### 3.5. Sales Analytics & Executive KPIs
- High-level KPIs: Total Invoiced Revenue, Collected Cash, Outstanding Receivables, Quotation-to-Order Win Rate %.
- Interactive commercial lifecycle funnel stepper.
- Monthly revenue trajectory chart.
- Top selling products by units and revenue.
- Live activity audit log feed.

---

## 4. Project Directory Structure

```
SmartERP/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── common/         # StatCard, Badge, Modal
│   │   │   └── sales/          # QuotationModal, SalesOrderModal, InvoiceModal, PaymentModal, DocumentPrintModal
│   │   ├── context/            # AuthContext, NotificationContext
│   │   ├── layouts/            # DashboardLayout (Sidebar, Navbar, Mobile Menu)
│   │   ├── pages/
│   │   │   ├── auth/           # Login, Register
│   │   │   ├── dashboard/      # SalesDashboard
│   │   │   ├── sales/          # QuotationsPage, SalesOrdersPage, InvoicesPage, PaymentsPage
│   │   │   ├── placeholder/    # Roadmap placeholder for Members 2, 3, 4, 6, 7
│   │   │   └── profile/        # ProfilePage & RBAC tester
│   │   ├── services/           # api.js, authService.js, salesService.js
│   │   ├── utils/              # constants.js, formatters
│   │   ├── routes/             # AppRoutes, ProtectedRoute
│   │   ├── App.jsx
│   │   ├── index.css
│   │   └── main.jsx
│   ├── index.html
│   ├── package.json
│   ├── tailwind.config.js
│   └── vite.config.js
│
├── backend/
│   ├── app/
│   │   ├── api/routes/
│   │   │   ├── auth.py         # Login, Register, Me, Logout, RBAC test routes
│   │   │   ├── sales.py        # Quotations, Orders, Invoices, Payments, Analytics endpoints
│   │   │   ├── master.py       # Customers & Products catalog endpoints
│   │   │   ├── users.py        # Users listing & security audit logs
│   │   │   ├── hr.py           # Member 2 clean placeholder
│   │   │   ├── crm.py          # Member 3 clean placeholder
│   │   │   ├── inventory.py    # Member 4 clean placeholder
│   │   │   ├── procurement.py  # Member 6 clean placeholder
│   │   │   ├── finance.py      # Member 6 clean placeholder
│   │   │   └── reports.py      # Member 7 clean placeholder
│   │   ├── core/               # config.py, security.py (bcrypt + JWT), dependencies.py
│   │   ├── database/           # session.py (SQLAlchemy + auto-fallback), base.py
│   │   ├── models/             # User, Role, Customer, Product, Quotation, SalesOrder, Invoice, Payment
│   │   ├── schemas/            # Pydantic V2 models for all entities
│   │   ├── services/           # Business logic & calculations for all sales entities
│   │   └── main.py             # FastAPI entrypoint, lifespan, auto-seeder, CORS
│   ├── .env.example
│   ├── requirements.txt
│   └── seed.py                 # Standalone database seeder
│
├── database/
│   └── schema.sql              # Production PostgreSQL DDL schema
│
├── docs/
│   ├── ARCHITECTURE.md         # System architecture diagram & module contracts
│   ├── SALES_MODULE_SPEC.md    # Calculations, state machines & API specs
│   └── TEAM_INTEGRATION_GUIDE.md # Guide for other team members
│
├── tests/
│   ├── conftest.py             # Pytest database & seed fixture
│   ├── test_auth.py            # Authentication, registration & JWT tests
│   ├── test_sales_quotations.py# Quotation creation, calculations & order conversion
│   ├── test_sales_orders.py    # Sales order lifecycle & invoice conversion
│   └── test_sales_invoices.py  # Invoices & payment auto-settlement tests
│
├── .gitignore
├── pytest.ini
├── README.md
└── start.bat                   # 1-Click Windows startup script
```

---

## 5. Getting Started (Windows)

### Prerequisites
- Python 3.10+ (Python 3.12 recommended)
- Node.js 18+ (Node.js 20 or 24 recommended)
- Git

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
- Frontend UI: `http://localhost:5173`

---

## 6. Pre-Configured Demo Credentials

The system automatically initializes default roles and users upon first startup:

| Role | Username | Password | Access Level |
|---|---|---|---|
| **Administrator** | `admin` | `Admin@123` | Full system access, audit logs, all modules |
| **Sales Manager** | `salesmgr` | `Manager@123` | Full sales lifecycle, quotations, orders, invoices, payments |

*(You can also register custom accounts with any role directly on `/register`)*

---

## 7. Running Automated Test Suites

Run all 8 automated pytest suites:
```powershell
.\backend\.venv\Scripts\python -m pytest -v tests/
```
Output:
```
tests/test_auth.py::test_root_endpoint PASSED                            [ 12%]
tests/test_auth.py::test_admin_login_success PASSED                      [ 25%]
tests/test_auth.py::test_invalid_login_rejected PASSED                   [ 37%]
tests/test_auth.py::test_user_registration_and_login PASSED              [ 50%]
tests/test_sales_invoices.py::test_invoice_and_payment_auto_settlement PASSED [ 62%]
tests/test_sales_orders.py::test_sales_order_lifecycle PASSED            [ 75%]
tests/test_sales_quotations.py::test_list_quotations PASSED              [ 87%]
tests/test_sales_quotations.py::test_create_and_convert_quotation PASSED [100%]
======================== 8 passed in 2.63s =========================
```

---

## 8. Database Configuration (PostgreSQL vs SQLite)

- **Default Zero-Config Mode**: By default, `backend/.env` is configured to `sqlite:///./smarterp.db`. It starts immediately without requiring PostgreSQL to be running or configured.
- **Production PostgreSQL Mode**:
  1. Create a PostgreSQL database named `smarterp`:
     ```sql
     CREATE DATABASE smarterp;
     ```
  2. In `backend/.env`, set:
     ```env
     DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/smarterp
     ```
  3. Restart the backend. Tables and seeds are created automatically via SQLAlchemy ORM.
