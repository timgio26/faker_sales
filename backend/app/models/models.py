from app.extension import db
from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import String, Text,ForeignKey,Float,Integer,Boolean,DateTime,Uuid
from sqlalchemy.sql import func
from datetime import datetime
from uuid import uuid4,UUID

class Product(db.Model):
    id: Mapped[UUID] = mapped_column(Uuid,default=uuid4,primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    # updated_at: Mapped[datetime] = mapped_column(onupdate=func.now())
    product_name: Mapped[str] = mapped_column(String(50), unique=True)
    product_category: Mapped[str] = mapped_column(String(50))
    product_price: Mapped[float] = mapped_column(Float)
    stock: Mapped[int] = mapped_column(Integer,default=0)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean,default=True)


    def to_dict(self):
        return {
            "id": str(self.id),
            "product_name": self.product_name,
            "product_category": self.product_category,
            "product_price": float(self.product_price),
        }
    
class Customer(db.Model):
    id: Mapped[UUID] = mapped_column(Uuid,default=uuid4,primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime,server_default=func.now())
    customer_name: Mapped[str] = mapped_column(String(50), unique=True)
    phone_number: Mapped[str] =mapped_column(String(20))

    orders:Mapped[list['Order']] = relationship(back_populates="customer")

    def to_dict(self):
        return {
            "id": str(self.id),
            "customer_name": self.customer_name,
            "phone_number":self.phone_number
        }

class Order(db.Model):
    order_id: Mapped[str] = mapped_column(String,unique=True,primary_key=True)
    order_timestamp: Mapped[datetime] = mapped_column(DateTime)
    order_status:Mapped[str] = mapped_column(String)

    order_items:Mapped[list["Order_Item"]]=relationship()

    customer_id:Mapped[UUID] = mapped_column(ForeignKey(Customer.id))
    customer:Mapped[Customer] = relationship(back_populates="orders")

    shipping_region:Mapped[str] = mapped_column(String)
    product_cost:Mapped[float] = mapped_column(Float)
    shipping_cost:Mapped[float] = mapped_column(Float)
    payment_method:Mapped[str] = mapped_column(String)
    def to_dict(self):
        return{
            'order_id':self.order_id,
            'order_timestamp':self.order_timestamp,
            'order_status':self.order_status,
            'order_items':[i.to_dict() for i in self.order_items],
            'customer_name':self.customer.to_dict().get("customer_name"),
            'phone_number':self.customer.to_dict().get("phone_number"),
            'shipping_region':self.shipping_region,
            'product_cost':self.product_cost,
            'shipping_cost':self.shipping_cost,
            'payment_method':self.payment_method

        }

class Order_Item(db.Model):
    order_item_id:Mapped[UUID] = mapped_column(Uuid,default=uuid4,primary_key=True)

    product_id:Mapped[UUID]=mapped_column(ForeignKey(Product.id))
    product:Mapped['Product']=relationship()

    order_id:Mapped[str]=mapped_column(ForeignKey(Order.order_id))

    qty:Mapped[int]=mapped_column(Integer)
    sub_total:Mapped[float]=mapped_column(Float)
    def to_dict(self):
        return{
            'product_id':self.product.to_dict().get('id'),
            "product_name": self.product.to_dict().get("product_name"),
            "product_category": self.product.to_dict().get("product_category"),
            "product_price": self.product.to_dict().get("product_price"),
            'qty':self.qty,
            'sub_total':self.sub_total
        }

    
