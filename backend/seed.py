"""
SmartERP - Unified Enterprise Database Seeder
Seeds Users, Roles, HR Data, Inventory Catalog, and Sales Pipeline data.
Run: python seed.py
"""
import sys
import os
from datetime import datetime, timezone, timedelta, date, time

sys.path.insert(0, os.path.dirname(__file__))

from app.database.session import SessionLocal, engine, Base
import app.database.base

# Models
from app.models.user import User, Role, Permission
from app.models.department import Department
from app.models.employee import Employee, EmployeeStatus, Gender
from app.models.attendance import Attendance, AttendanceStatus
from app.models.leave import Leave, LeaveType, LeaveStatus
from app.models.category import Category
from app.models.product import Product
from app.models.customer import Customer
from app.models.quotation import Quotation, QuotationItem
from app.models.sales_order import SalesOrder, SalesOrderItem
from app.models.invoice import Invoice, InvoiceItem
from app.models.payment import Payment
from app.core.security import get_password_hash


def seed_database():
    print("Creating tables if they do not exist...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        print("Checking roles and permissions...")
        admin_role = db.query(Role).filter(Role.name == "ADMIN").first()
        if not admin_role:
            admin_role = Role(name="ADMIN", description="System Administrator")
            mgr_role = Role(name="MANAGER", description="Sales & Operations Manager")
            emp_role = Role(name="EMPLOYEE", description="Staff / Sales Executive")
            db.add_all([admin_role, mgr_role, emp_role])
            db.commit()
            db.refresh(admin_role)

            for code, desc in [
                ("AUTH_LOGIN", "Login"),
                ("AUTH_REGISTER", "Register"),
                ("SALES_ALL", "Full Sales Access"),
            ]:
                p = Permission(code=code, description=desc)
                db.add(p)
                admin_role.permissions.append(p)
            db.commit()

        # Admin user
        admin = db.query(User).filter(User.username == "admin").first()
        if not admin:
            admin = User(
                full_name="System Administrator",
                username="admin",
                email="admin@smarterp.local",
                hashed_password=get_password_hash("Admin@123"),
                is_active=True,
                is_superuser=True,
            )
            admin.roles.append(admin_role)
            db.add(admin)
            db.commit()
            db.refresh(admin)
            print("Created default admin: admin / Admin@123")

        # HR Departments
        dept_data = [
            {"name": "Human Resources", "code": "HR", "description": "HR & People Operations"},
            {"name": "Engineering", "code": "ENG", "description": "Software Development"},
            {"name": "Finance", "code": "FIN", "description": "Finance & Accounting"},
            {"name": "Marketing", "code": "MKT", "description": "Marketing & Growth"},
            {"name": "Sales", "code": "SLS", "description": "Sales & Revenue"},
            {"name": "Operations", "code": "OPS", "description": "Business Operations"},
        ]
        depts = {}
        for d in dept_data:
            existing = db.query(Department).filter(Department.name == d["name"]).first()
            if not existing:
                dept = Department(name=d["name"], description=d["description"])
                db.add(dept)
                db.flush()
                depts[d["code"]] = dept
            else:
                depts[d["code"]] = existing
        db.commit()

        # Customers
        c1 = db.query(Customer).filter(Customer.name == "Apex Global Technologies").first()
        if not c1:
            c1 = Customer(
                name="Apex Global Technologies",
                company_name="Apex Global Ltd.",
                email="procurement@apextech.io",
                phone="+91 98765 43210",
                address="Cyber City Tower 4, Phase 2",
                city="Hyderabad",
                tax_id="36AABCA1234F1Z5",
            )
            c2 = Customer(
                name="Zenith Retail Ventures",
                company_name="Zenith Retail India",
                email="finance@zenithretail.com",
                phone="+91 91234 56789",
                address="MG Road Commercial Complex",
                city="Bengaluru",
                tax_id="29AABCB5678D1Z2",
            )
            db.add_all([c1, c2])
            db.commit()
            db.refresh(c1)
            db.refresh(c2)

        # Categories
        cat = db.query(Category).first()
        if not cat:
            cat = Category(category_code="CAT-GEN", category_name="General Hardware & Software", description="General IT and ERP items")
            db.add(cat)
            db.commit()
            db.refresh(cat)

        # Products
        p1 = db.query(Product).filter(Product.sku == "PROD-ERP-CORE").first()
        if not p1:
            p1 = Product(
                product_code="PRD-ERP-CORE",
                sku="PROD-ERP-CORE",
                product_name="SmartERP Cloud Subscription (1 Year)",
                category_id=cat.id,
                unit="License",
                selling_price=120000.0,
                cost_price=30000.0,
                tax_percentage=18.0,
            )
            p2 = Product(
                product_code="PRD-SRV-RACK",
                sku="PROD-SRV-RACK",
                product_name="Enterprise Rack Server X4",
                category_id=cat.id,
                unit="Units",
                selling_price=245000.0,
                cost_price=180000.0,
                tax_percentage=18.0,
            )
            db.add_all([p1, p2])
            db.commit()
            db.refresh(p1)
            db.refresh(p2)

        # Quotations, Sales Orders, Invoices
        if db.query(Quotation).count() == 0:
            q = Quotation(
                quote_number="QT-2026-0001",
                customer_id=c1.id,
                customer_name=c1.name,
                customer_email=c1.email,
                customer_phone=c1.phone,
                customer_address=c1.address,
                issue_date=datetime.now(timezone.utc) - timedelta(days=5),
                valid_until=datetime.now(timezone.utc) + timedelta(days=25),
                status="Accepted",
                subtotal=365000.0,
                discount_amount=15000.0,
                tax_amount=63000.0,
                total_amount=413000.0,
                notes="Enterprise deployment for Q2 fiscal year.",
                created_by_id=admin.id,
            )
            qi1 = QuotationItem(
                product_id=p1.id,
                product_name=p1.name,
                quantity=1.0,
                unit_price=120000.0,
                tax_rate=18.0,
                total_amount=141600.0,
            )
            qi2 = QuotationItem(
                product_id=p2.id,
                product_name=p2.name,
                quantity=1.0,
                unit_price=245000.0,
                discount_percent=6.12,
                tax_rate=18.0,
                total_amount=271400.0,
            )
            q.items.extend([qi1, qi2])
            db.add(q)
            db.commit()
            db.refresh(q)

            so = SalesOrder(
                order_number="SO-2026-0001",
                quotation_id=q.id,
                customer_id=c1.id,
                customer_name=c1.name,
                customer_email=c1.email,
                customer_phone=c1.phone,
                shipping_address=c1.address,
                billing_address=c1.address,
                order_date=datetime.now(timezone.utc) - timedelta(days=3),
                expected_delivery_date=datetime.now(timezone.utc) + timedelta(days=7),
                status="Confirmed",
                subtotal=365000.0,
                discount_amount=15000.0,
                tax_amount=63000.0,
                total_amount=413000.0,
                notes="Generated from QT-2026-0001",
                created_by_id=admin.id,
            )
            soi1 = SalesOrderItem(
                product_id=p1.id,
                product_name=p1.name,
                quantity=1.0,
                unit_price=120000.0,
                tax_rate=18.0,
                total_amount=141600.0,
            )
            so.items.append(soi1)
            db.add(so)
            db.commit()
            db.refresh(so)
            q.sales_order_id = so.id
            db.commit()

            inv = Invoice(
                invoice_number="INV-2026-0001",
                sales_order_id=so.id,
                customer_id=c1.id,
                customer_name=c1.name,
                customer_email=c1.email,
                customer_phone=c1.phone,
                customer_address=c1.address,
                issue_date=datetime.now(timezone.utc) - timedelta(days=2),
                due_date=datetime.now(timezone.utc) + timedelta(days=28),
                status="Partially Paid",
                subtotal=365000.0,
                discount_amount=15000.0,
                tax_amount=63000.0,
                total_amount=413000.0,
                amount_paid=200000.0,
                balance_due=213000.0,
                payment_terms="Net 30 Days",
                created_by_id=admin.id,
            )
            ii1 = InvoiceItem(
                product_id=p1.id,
                product_name=p1.name,
                quantity=1.0,
                unit_price=120000.0,
                tax_rate=18.0,
                total_amount=141600.0,
            )
            inv.items.append(ii1)
            db.add(inv)
            db.commit()
            db.refresh(inv)
            so.invoice_id = inv.id
            db.commit()

            pay = Payment(
                payment_number="PAY-2026-0001",
                invoice_id=inv.id,
                customer_id=c1.id,
                customer_name=c1.name,
                payment_date=datetime.now(timezone.utc) - timedelta(days=1),
                payment_method="Bank Transfer",
                reference_number="UTR-HDFC-98210344",
                amount=200000.0,
                notes="50% advance bank transfer received.",
                status="Completed",
                created_by_id=admin.id,
            )
            db.add(pay)
            db.commit()
            print("Seeded sample Quotation, Order, Invoice, and Payment!")

        print("Database seeding completed successfully.")
    except Exception as e:
        print(f"Error during seeding: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
