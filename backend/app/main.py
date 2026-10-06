import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.database.session import engine, Base, SessionLocal
import app.database.base  # ensure all models are registered
from app.api.routes import auth, sales, master, users, hr, crm, inventory, procurement, finance, reports
from app.models.user import User, Role, Permission
from app.models.customer import Customer
from app.models.product import Product
from app.core.security import get_password_hash

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SmartERP")


def seed_initial_data():
    """Seed initial roles, permissions, admin user, sample customers and products if DB is fresh."""
    db = SessionLocal()
    try:
        # 1. Create Roles
        admin_role = db.query(Role).filter(Role.name == "ADMIN").first()
        if not admin_role:
            admin_role = Role(name="ADMIN", description="System Administrator with full system control")
            manager_role = Role(name="MANAGER", description="Sales & Operations Manager")
            employee_role = Role(name="EMPLOYEE", description="Sales Executive / Staff")
            db.add_all([admin_role, manager_role, employee_role])
            db.commit()
            db.refresh(admin_role)

            # 2. Create Permissions
            perm_codes = [
                ("AUTH_LOGIN", "Login to system"),
                ("AUTH_REGISTER", "Register new users"),
                ("SALES_VIEW", "View sales records"),
                ("SALES_CREATE", "Create quotations and sales orders"),
                ("SALES_INVOICE", "Issue invoices and collect payments"),
                ("SALES_ADMIN", "Full sales administration"),
            ]
            for code, desc in perm_codes:
                p = Permission(code=code, description=desc)
                db.add(p)
                admin_role.permissions.append(p)
            db.commit()

        # 3. Create Default Admin User
        admin_user = db.query(User).filter(User.username == "admin").first()
        if not admin_user:
            admin_user = User(
                full_name="Administrator",
                username="admin",
                email="admin@smarterp.local",
                hashed_password=get_password_hash("Admin@123"),
                is_active=True,
                is_superuser=True,
            )
            admin_user.roles.append(admin_role)
            db.add(admin_user)
            db.commit()
            logger.info("Created default admin user: admin / Admin@123")

        # 4. Create Demo Sales Rep / Manager
        manager_user = db.query(User).filter(User.username == "salesmgr").first()
        if not manager_user:
            mgr_role = db.query(Role).filter(Role.name == "MANAGER").first()
            manager_user = User(
                full_name="Sarah Jenkins (Sales Manager)",
                username="salesmgr",
                email="sarah@smarterp.local",
                hashed_password=get_password_hash("Manager@123"),
                is_active=True,
                is_superuser=False,
            )
            if mgr_role:
                manager_user.roles.append(mgr_role)
            db.add(manager_user)
            db.commit()

        # 5. Create Sample Customers if none
        if db.query(Customer).count() == 0:
            customers = [
                Customer(
                    name="Apex Global Technologies",
                    company_name="Apex Global Ltd.",
                    email="procurement@apextech.io",
                    phone="+91 98765 43210",
                    address="Cyber City Tower 4, Phase 2",
                    city="Hyderabad",
                    tax_id="36AABCA1234F1Z5",
                ),
                Customer(
                    name="Zenith Retail Ventures",
                    company_name="Zenith Retail India",
                    email="finance@zenithretail.com",
                    phone="+91 91234 56789",
                    address="MG Road Commercial Complex",
                    city="Bengaluru",
                    tax_id="29AABCB5678D1Z2",
                ),
                Customer(
                    name="Horizon Logistics Corp",
                    company_name="Horizon Freight Systems",
                    email="billing@horizonlogistics.com",
                    phone="+91 94455 66778",
                    address="Harbour Port Boulevard",
                    city="Mumbai",
                    tax_id="27AABCC9988E1Z9",
                ),
            ]
            db.add_all(customers)
            db.commit()

        # 6. Create Sample Products if none
        if db.query(Product).count() == 0:
            products = [
                Product(
                    sku="PROD-ERP-CORE",
                    name="SmartERP Cloud Subscription (1 Year)",
                    description="Full ERP platform access for up to 25 users with priority support",
                    category="Software",
                    unit="License",
                    unit_price=120000.0,
                    cost_price=30000.0,
                    tax_rate=18.0,
                    stock_quantity=999,
                ),
                Product(
                    sku="PROD-SRV-RACK",
                    name="Enterprise Rack Server X4",
                    description="Dual Xeon Gold, 128GB ECC RAM, 4TB NVMe SSD",
                    category="Hardware",
                    unit="Units",
                    unit_price=245000.0,
                    cost_price=180000.0,
                    tax_rate=18.0,
                    stock_quantity=25,
                ),
                Product(
                    sku="PROD-CNS-IMPL",
                    name="ERP On-Premises Implementation Services",
                    description="Professional deployment, migration, workflow customization and staff onboarding",
                    category="Services",
                    unit="Hours",
                    unit_price=4500.0,
                    cost_price=2000.0,
                    tax_rate=18.0,
                    stock_quantity=500,
                ),
                Product(
                    sku="PROD-IOT-SCAN",
                    name="Industrial Barcode & RFID Scanner",
                    description="Rugged handheld 2D imager with Bluetooth 5.2 and IP65 protection",
                    category="Hardware",
                    unit="Pcs",
                    unit_price=18500.0,
                    cost_price=11000.0,
                    tax_rate=18.0,
                    stock_quantity=80,
                ),
            ]
            db.add_all(products)
            db.commit()

    except Exception as e:
        logger.error(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables if not exist
    Base.metadata.create_all(bind=engine)
    # Seed initial data
    seed_initial_data()
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="SmartERP - Enterprise Resource Planning API. Member 5: Sales (Quotations, Orders, Invoices, Payments).",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all during development for smooth local testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers under /api/v1
api_v1_prefix = settings.API_V1_STR
app.include_router(auth.router, prefix=api_v1_prefix)
app.include_router(sales.router, prefix=api_v1_prefix)
app.include_router(master.router, prefix=api_v1_prefix)
app.include_router(users.router, prefix=api_v1_prefix)

# Future Module placeholders for architectural completeness
app.include_router(hr.router, prefix=api_v1_prefix)
app.include_router(crm.router, prefix=api_v1_prefix)
app.include_router(inventory.router, prefix=api_v1_prefix)
app.include_router(procurement.router, prefix=api_v1_prefix)
app.include_router(finance.router, prefix=api_v1_prefix)
app.include_router(reports.router, prefix=api_v1_prefix)


@app.get("/")
def root():
    return {
        "system": "SmartERP",
        "version": settings.VERSION,
        "module": "Member 5: Sales Management System",
        "docs": "/docs",
        "redoc": "/redoc",
        "status": "online",
        "endpoints": {
            "auth": f"{api_v1_prefix}/auth",
            "sales": f"{api_v1_prefix}/sales",
            "master_data": f"{api_v1_prefix}/master",
            "users": f"{api_v1_prefix}/users",
        }
    }
