import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.database.session import engine, Base, SessionLocal
import app.database.base  # ensure all models are registered

# Route imports
from app.api.routes import auth, sales, master, users, hr, crm, inventory as inventory_stub, procurement, finance, reports
from app.api.routes import departments, employees, attendance, leaves
from app.routers import categories, products, warehouses, inventory
from app.routers.auth import seed_default_roles_and_admin

# Models for sample seeding
from app.models.user import User, Role, Permission
from app.models.customer import Customer
from app.models.product import Product
from app.models.category import Category
from app.core.security import get_password_hash

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SmartERP")


def seed_initial_data(db=None):
    """Seed initial demo users, customers, and products if DB is fresh."""
    close_db = False
    if db is None:
        db = SessionLocal()
        close_db = True
    try:
        # Roles
        admin_role = db.query(Role).filter(Role.name == "ADMIN").first()
        if not admin_role:
            admin_role = Role(name="ADMIN", description="System Administrator")
            mgr_role = Role(name="MANAGER", description="Sales & Operations Manager")
            emp_role = Role(name="EMPLOYEE", description="Staff / Sales Executive")
            db.add_all([admin_role, mgr_role, emp_role])
            db.commit()
            db.refresh(admin_role)

        # Default Admin
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

        # Sales Manager
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

        # Sample Category
        gen_cat = db.query(Category).first()
        if not gen_cat:
            gen_cat = Category(category_code="CAT-GEN", category_name="General Hardware & Software", description="General IT and ERP items")
            db.add(gen_cat)
            db.commit()
            db.refresh(gen_cat)

        # Sample Customers
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

        # Sample Products
        if db.query(Product).count() == 0:
            products_list = [
                Product(
                    product_code="PRD-ERP-CORE",
                    sku="PROD-ERP-CORE",
                    product_name="SmartERP Cloud Subscription (1 Year)",
                    description="Full ERP platform access for up to 25 users with priority support",
                    category_id=gen_cat.id,
                    unit="License",
                    selling_price=120000.0,
                    cost_price=30000.0,
                    tax_percentage=18.0,
                    reorder_level=10,
                ),
                Product(
                    product_code="PRD-SRV-RACK",
                    sku="PROD-SRV-RACK",
                    product_name="Enterprise Rack Server X4",
                    description="Dual Xeon Gold, 128GB ECC RAM, 4TB NVMe SSD",
                    category_id=gen_cat.id,
                    unit="Units",
                    selling_price=245000.0,
                    cost_price=180000.0,
                    tax_percentage=18.0,
                    reorder_level=5,
                ),
                Product(
                    product_code="PRD-CNS-IMPL",
                    sku="PROD-CNS-IMPL",
                    product_name="ERP On-Premises Implementation Services",
                    description="Professional deployment, migration, workflow customization and staff onboarding",
                    category_id=gen_cat.id,
                    unit="Hours",
                    selling_price=4500.0,
                    cost_price=2000.0,
                    tax_percentage=18.0,
                    reorder_level=20,
                ),
                Product(
                    product_code="PRD-IOT-SCAN",
                    sku="PROD-IOT-SCAN",
                    product_name="Industrial Barcode & RFID Scanner",
                    description="Rugged handheld 2D imager with Bluetooth 5.2 and IP65 protection",
                    category_id=gen_cat.id,
                    unit="Pcs",
                    selling_price=18500.0,
                    cost_price=11000.0,
                    tax_percentage=18.0,
                    reorder_level=15,
                ),
            ]
            db.add_all(products_list)
            db.commit()

    except Exception as e:
        logger.error(f"Error in seed_initial_data: {e}")
        db.rollback()
    finally:
        if close_db:
            db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database tables
    Base.metadata.create_all(bind=engine)
    # Run seed scripts
    try:
        with SessionLocal() as db:
            seed_default_roles_and_admin(db)
            seed_initial_data(db)
    except Exception as e:
        logger.warning(f"Initial seed warning: {e}")
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="SmartERP - Enterprise Resource Planning API with Authentication, HR, Inventory, and Sales modules.",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/api/openapi.json",
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API v1 Prefix
api_v1_prefix = settings.API_V1_STR

# Authentication & Security
app.include_router(auth.router, prefix=api_v1_prefix)
app.include_router(users.router, prefix=api_v1_prefix)

# Sales Module (Member 5)
app.include_router(sales.router, prefix=api_v1_prefix)
app.include_router(master.router, prefix=api_v1_prefix)

# HR Module (Member 2)
app.include_router(departments.router, prefix=api_v1_prefix)
app.include_router(employees.router, prefix=api_v1_prefix)
app.include_router(attendance.router, prefix=api_v1_prefix)
app.include_router(leaves.router, prefix=api_v1_prefix)

# Inventory Module (Member 4)
app.include_router(categories.router, prefix=api_v1_prefix)
app.include_router(products.router, prefix=api_v1_prefix)
app.include_router(warehouses.router, prefix=api_v1_prefix)
app.include_router(inventory.router, prefix=api_v1_prefix)

# Other Module placeholders
app.include_router(crm.router, prefix=api_v1_prefix)
app.include_router(procurement.router, prefix=api_v1_prefix)
app.include_router(finance.router, prefix=api_v1_prefix)
app.include_router(reports.router, prefix=api_v1_prefix)


@app.get("/", tags=["Health"])
def root():
    return {
        "system": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "module": "Member 5: Sales Management System",
        "status": "Online",
        "docs": "/docs",
        "redoc": "/redoc",
        "modules": {
            "auth": f"{api_v1_prefix}/auth",
            "sales": f"{api_v1_prefix}/sales",
            "inventory": f"{api_v1_prefix}/inventory",
            "hr": f"{api_v1_prefix}/employees",
            "master_data": f"{api_v1_prefix}/master",
            "users": f"{api_v1_prefix}/users",
        }
    }


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy", "service": settings.PROJECT_NAME}
