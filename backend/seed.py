"""
Standalone database seeder for SmartERP - Member 5 (Sales Module).
Populates users, customers, catalog products, quotations, orders, invoices, and payments.
"""
from datetime import datetime, timezone, timedelta
from app.database.session import SessionLocal, engine, Base
import app.database.base
from app.models.user import User, Role, Permission
from app.models.customer import Customer
from app.models.product import Product
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
            mgr_role = Role(name="MANAGER", description="Sales Manager")
            emp_role = Role(name="EMPLOYEE", description="Sales Executive")
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

        # Products
        p1 = db.query(Product).filter(Product.sku == "PROD-ERP-CORE").first()
        if not p1:
            p1 = Product(
                sku="PROD-ERP-CORE",
                name="SmartERP Cloud Subscription (1 Year)",
                category="Software",
                unit="License",
                unit_price=120000.0,
                cost_price=30000.0,
                tax_rate=18.0,
                stock_quantity=999,
            )
            p2 = Product(
                sku="PROD-SRV-RACK",
                name="Enterprise Rack Server X4",
                category="Hardware",
                unit="Units",
                unit_price=245000.0,
                cost_price=180000.0,
                tax_rate=18.0,
                stock_quantity=25,
            )
            db.add_all([p1, p2])
            db.commit()
            db.refresh(p1)
            db.refresh(p2)

        # Quotation
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

            # Sales Order
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
            soi2 = SalesOrderItem(
                product_id=p2.id,
                product_name=p2.name,
                quantity=1.0,
                unit_price=245000.0,
                discount_percent=6.12,
                tax_rate=18.0,
                total_amount=271400.0,
            )
            so.items.extend([soi1, soi2])
            db.add(so)
            db.commit()
            db.refresh(so)

            q.sales_order_id = so.id
            db.commit()

            # Invoice
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
            ii2 = InvoiceItem(
                product_id=p2.id,
                product_name=p2.name,
                quantity=1.0,
                unit_price=245000.0,
                discount_percent=6.12,
                tax_rate=18.0,
                total_amount=271400.0,
            )
            inv.items.extend([ii1, ii2])
            db.add(inv)
            db.commit()
            db.refresh(inv)

            so.invoice_id = inv.id
            db.commit()

            # Payment
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
