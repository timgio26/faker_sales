from app.extension import db
from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import String, Text
from sqlalchemy.sql import func
from datetime import datetime
from uuid import uuid4,UUID

class Product(db.Model):
    id: Mapped[UUID] = mapped_column(default=uuid4,primary_key=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    # updated_at: Mapped[datetime] = mapped_column(onupdate=func.now())
    product_name: Mapped[str] = mapped_column(String(50), unique=True)
    product_category: Mapped[str] = mapped_column(String(50))
    product_price: Mapped[float] = mapped_column()
    stock: Mapped[int] = mapped_column(default=0)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True)

    def to_dict(self):
        return {
            "id": str(self.id),
            "product_name": self.product_name,
            "product_category": self.product_category,
            "product_price": float(self.product_price),
        }
    
class Customer(db.Model):
    id: Mapped[UUID] = mapped_column(default=uuid4,primary_key=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    # updated_at: Mapped[datetime] = mapped_column(onupdate=func.now())
    customer_name: Mapped[str] = mapped_column(String(50), unique=True)

    def to_dict(self):
        return {
            "id": str(self.id),
            "customer_name": self.customer_name,
        }