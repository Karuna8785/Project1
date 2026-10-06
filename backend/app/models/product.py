from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from app.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    product_code = Column(String(50), unique=True, index=True, nullable=False)
    sku = Column(String(50), unique=True, index=True, nullable=False)
    barcode = Column(String(100), unique=True, index=True, nullable=True)
    product_name = Column(String(150), index=True, nullable=False)
    description = Column(Text, nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="RESTRICT"), index=True, nullable=False)
    unit = Column(String(30), default="pcs", nullable=False)  # pcs, kg, box, liters, etc.
    
    # Financial fields
    cost_price = Column(Numeric(12, 2), default=0.00, nullable=False)
    selling_price = Column(Numeric(12, 2), default=0.00, nullable=False)
    tax_percentage = Column(Numeric(5, 2), default=0.00, nullable=False)

    # Stock control thresholds
    reorder_level = Column(Integer, default=10, nullable=False)
    minimum_stock_level = Column(Integer, default=5, nullable=False)
    maximum_stock_level = Column(Integer, default=1000, nullable=False)

    is_active = Column(Boolean, default=True, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    category = relationship("Category", back_populates="products")
    creator = relationship("User", foreign_keys=[created_by])
    inventory_items = relationship("WarehouseStock", back_populates="product", cascade="all, delete-orphan")
    stock_movements = relationship("StockMovement", back_populates="product")

    @property
    def total_stock(self) -> int:
        if not self.inventory_items:
            return 0
        return sum(item.available_quantity for item in self.inventory_items)

    @property
    def stock_status(self) -> str:
        stock = self.total_stock
        if stock <= 0:
            return "OUT OF STOCK"
        elif stock <= self.reorder_level:
            return "LOW STOCK"
        return "IN STOCK"
