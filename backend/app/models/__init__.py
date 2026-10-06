"""
SmartERP - Enterprise Models Registry
Registers all ORM models across Authentication, HR, Inventory, and Sales modules.
"""
from app.database.session import Base

# Authentication & Security
from app.models.user import User, Role, Permission, user_roles, role_permissions
from app.models.audit_log import AuditLog

# HR Management
from app.models.department import Department
from app.models.employee import Employee, EmployeeStatus, Gender
from app.models.attendance import Attendance, AttendanceStatus
from app.models.leave import Leave, LeaveType, LeaveStatus

# Inventory & Master Catalog
from app.models.category import Category
from app.models.product import Product
from app.models.warehouse import Warehouse
from app.models.inventory import WarehouseStock
from app.models.stock_movement import StockMovement

# Sales Management
from app.models.customer import Customer
from app.models.quotation import Quotation, QuotationItem
from app.models.sales_order import SalesOrder, SalesOrderItem
from app.models.invoice import Invoice, InvoiceItem
from app.models.payment import Payment

__all__ = [
    "Base",
    # Auth
    "User",
    "Role",
    "Permission",
    "AuditLog",
    "user_roles",
    "role_permissions",
    # HR
    "Department",
    "Employee",
    "EmployeeStatus",
    "Gender",
    "Attendance",
    "AttendanceStatus",
    "Leave",
    "LeaveType",
    "LeaveStatus",
    # Inventory
    "Category",
    "Product",
    "Warehouse",
    "WarehouseStock",
    "StockMovement",
    # Sales
    "Customer",
    "Quotation",
    "QuotationItem",
    "SalesOrder",
    "SalesOrderItem",
    "Invoice",
    "InvoiceItem",
    "Payment",
]
