# SmartERP — Enterprise Resource Planning Platform

SmartERP is a production-grade, collaborative Enterprise Resource Planning system built with modern Python (FastAPI, SQLAlchemy 2.0, Pydantic v2), React.js (Vite, Tailwind CSS, Recharts), and PostgreSQL.

---

## 1. Collaborative Team Allocation

SmartERP is divided into specialized modules owned by 7 developers:

| Member | Responsibility | Modules / Scope | Status |
|---|---|---|---|
| **Member 1** | **Authentication & Security** | JWT, Login, Register, Roles, Permissions, Audit Logging | **Fully Implemented** |
| Member 2 | HR Management | Employees, Departments, Attendance, Leave | Placeholder Ready |
| Member 3 | CRM | Customers, Leads, Customer History | Placeholder Ready |
| **Member 4** | **Inventory Management** | Products, Categories, Warehouses, Stock In/Out/Transfer, Low Stock Alerts, Stock Movements | **Fully Implemented** |
| Member 5 | Sales Management | Quotations, Orders, Invoices (uses Inventory `deduct_stock`) | Integration Point Ready |
| Member 6 | Procurement & Finance | Suppliers, Purchase Orders, Invoices (uses Inventory `add_stock`) | Integration Point Ready |
| Member 7 | Dashboard & Reports | Executive Analytics (uses Inventory `get_inventory_summary`) | Integration Point Ready |

---

## 2. Technology Stack

- **Backend**: Python 3.12, FastAPI, SQLAlchemy 2.0 (declarative), Pydantic v2, PyJWT, bcrypt, Alembic, psycopg2-binary
- **Frontend**: React 18, Vite, React Router v6, Tailwind CSS, Lucide React icons, Recharts
- **Database**: PostgreSQL (with automated SQLite fallback for offline local testing)
- **Testing**: Pytest, FastAPI TestClient
- **No external cloud APIs or Docker required** — self-hosted and self-contained.

---

## 3. Directory Layout

```
SmartERP/
├── backend/
│   ├── app/
│   │   ├── core/           # Security, password hashing, JWT, settings
│   │   ├── database/       # SQLAlchemy engine & session management
│   │   ├── models/         # User, Role, Permission, AuditLog, Product, Category, Warehouse, WarehouseStock, StockMovement
│   │   ├── schemas/        # Pydantic v2 schemas for all modules
│   │   ├── services/       # InventoryService (Stock In/Out/Adjust/Transfer), AuditService
│   │   ├── routers/        # auth, users, categories, products, warehouses, inventory, hr, crm
│   │   └── main.py         # FastAPI application entrypoint
│   ├── alembic/            # Database migration environment
│   ├── tests/              # Pytest test suite (auth, categories, products, warehouses, transactions, transfers, low-stock)
│   ├── pytest.ini
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── api/            # API clients with automatic JWT headers
│   │   ├── components/     # Layout, Navbar, Sidebar, DataTable, Modals, StatCards, Search, FilterPanel
│   │   ├── context/        # AuthContext, NotificationContext
│   │   ├── pages/
│   │   │   ├── auth/       # Login, Register
│   │   │   ├── dashboard/  # Main Dashboard
│   │   │   ├── profile/    # User Profile & Roles/Permissions
│   │   │   ├── inventory/  # Member 4 Inventory (Overview, Products, Categories, Warehouses, Stock, Movements, Low Stock)
│   │   │   └── placeholders/ # Team module placeholders
│   │   ├── routes/         # ProtectedRoute guard
│   │   └── App.jsx
│   ├── index.html
│   ├── tailwind.config.js
│   └── package.json
├── database/
│   ├── schema.sql          # Raw PostgreSQL DDL script
│   └── seed.py             # Database seed script for roles, permissions, users, initial stock
├── docs/
│   └── INVENTORY_MODULE.md # Comprehensive Member 4 technical documentation
├── start.bat               # Windows one-click startup runner
└── README.md
```

---

## 4. Quick Start (Windows Setup)

### Prerequisites
- Python 3.10+ installed
- Node.js 18+ and npm installed
- PostgreSQL installed (optional for development; system automatically runs with SQLite fallback if PostgreSQL is not active)

### Step 1: Install Backend Dependencies
```powershell
cd backend
python -m pip install -r requirements.txt
```

### Step 2: Install Frontend Dependencies
```powershell
cd ../frontend
npm install
```

### Step 3: Run Database Migrations and Seed
```powershell
# From project root:
python database/seed.py
```

### Step 4: Start Applications
You can start both services with a single click using `start.bat`, or in separate shells:

**Backend:**
```powershell
cd backend
python -m uvicorn app.main:app --reload --port 8000
```

**Frontend:**
```powershell
cd frontend
npm run dev
```

- **Frontend Portal**: [http://localhost:5173](http://localhost:5173)
- **FastAPI Backend**: [http://localhost:8000](http://localhost:8000)
- **Swagger Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc Documentation**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 5. Default Credentials

The initial seed script creates two operational enterprise accounts:

| Role | Username | Password | Access Scope |
|---|---|---|---|
| **Administrator** | `admin` | `Admin@123` | Full system access across all modules |
| **Inventory Manager** | `inventory_manager` | `Inventory@123` | Full access to Member 4 Inventory Subsystem |

---

## 6. Member 4 Inventory Management Subsystem

The Inventory Subsystem contains complete operational features:
- **Products**: Full CRUD, SKU/Barcode unique enforcement, non-negative pricing validation, category assignment, warehouse breakdown, safe deactivation protection.
- **Categories**: Full CRUD, product count tracking, deletion blocked if items are assigned.
- **Warehouses**: Multi-warehouse facility management, contact tracking, facility stock views, deletion blocked if stock is held.
- **Stock In**: Increases on-hand and available quantities, logs immutable `STOCK_IN` movement.
- **Stock Out**: Decreases on-hand quantity, prevents negative stock, raises readable insufficient stock alerts (`"Insufficient stock. Only X units are available."`).
- **Stock Adjustment**: Increase or Decrease inventory with mandatory audit reason (`Physical Count Correction`, `Damaged Goods`, `Expired Goods`, etc.).
- **Stock Transfer**: Atomic multi-warehouse stock relocation (`TRANSFER_OUT` + `TRANSFER_IN`). Source and destination cannot be identical; rolls back completely on any failure.
- **Low Stock Alerts**: Automatically triggers when `available_quantity <= reorder_level` with shortage calculation and direct restock action.
- **Audit Ledger**: Immutable history log tracking every stock change with timestamp, before/after balances, reference numbers, and operator ID.
- **Inventory Valuation**: Dynamic calculation `SUM(quantity_on_hand * cost_price)`.

---

## 7. Running Backend Tests

Run the complete Pytest suite:
```powershell
cd backend
pytest -v
```

Test coverage includes:
- Authentication, registration, duplicate checks, password hashing, JWT validation, role checks, audit logs
- Category CRUD and safe deletion
- Product CRUD, validation, search, and filtering
- Warehouse CRUD and stock view
- Stock In, Stock Out, Insufficient stock rejection
- Stock Adjustment with reason
- Warehouse Transfer and atomic rollback
- Low stock and out-of-stock detection
- Member 5 (Sales `deduct_stock`) and Member 6 (Procurement `add_stock`) integration services
