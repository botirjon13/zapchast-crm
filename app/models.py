from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Numeric
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(200))
    password_hash = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())

class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    phone = Column(String(50))
    email = Column(String(200))
    address = Column(Text)
    created_at = Column(DateTime, server_default=func.now())

class Part(Base):
    __tablename__ = 'parts'
    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(100), unique=True, index=True)
    name = Column(String(300), nullable=False)
    description = Column(Text)
    price = Column(Numeric(12,2), nullable=False, default=0)
    created_at = Column(DateTime, server_default=func.now())

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    status = Column(String(50), nullable=False, default='draft')
    total_amount = Column(Numeric(12,2), default=0)
    created_at = Column(DateTime, server_default=func.now())
    customer = relationship('Customer')
    user = relationship('User')

class OrderItem(Base):
    __tablename__ = 'order_items'
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    part_id = Column(Integer, ForeignKey('parts.id'))
    qty = Column(Integer, nullable=False, default=1)
    unit_price = Column(Numeric(12,2), nullable=False)
    line_total = Column(Numeric(12,2), nullable=False)
