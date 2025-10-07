# app/models.py
from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    Numeric,
    Text,
)
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    tablename = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(150), unique=True, index=True, nullable=False)
    # Some parts of your code may expect "hashed_password" or "password_hash".
    # To be safe we store both columns (they can be set to same value by your auth logic).
    hashed_password = Column(String(512), nullable=True)
    password_hash = Column(String(512), nullable=True)
    is_admin = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # convenience relationship if you reference user.orders
    orders = relationship("Order", back_populates="user")


class Customer(Base):
    tablename = "customers"

    id = Column(Integer, primary_key=True, index=True)
    # Some frontends/schemas used "full_name", some used "name".
    # We keep both to avoid breaking changes; one can be empty.
    full_name = Column(String(250), nullable=True, index=True)
    name = Column(String(250), nullable=True, index=True)
    phone = Column(String(50), nullable=True)
    email = Column(String(150), nullable=True)
    address = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    orders = relationship("Order", back_populates="customer")


class Part(Base):
    tablename = "parts"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(100), nullable=True, index=True)
    name = Column(String(250), nullable=False, index=True)
    description = Column(Text, nullable=True)
    # price/quantity used by business logic — Numeric is safer for money
    price = Column(Numeric(12, 2), default=0, nullable=False)
    quantity = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    order_items = relationship("OrderItem", back_populates="part")


class Order(Base):
    tablename = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    status = Column(String(50), default="created", nullable=False)
    total_amount = Column(Numeric(14, 2), default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    customer = relationship("Customer", back_populates="orders")
    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    tablename = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, index=True)
    part_id = Column(Integer, ForeignKey("parts.id"), nullable=False, index=True)
    qty = Column(Integer, default=1, nullable=False)
    unit_price = Column(Numeric(12, 2), default=0, nullable=False)
    line_total = Column(Numeric(14, 2), default=0, nullable=False)

    order = relationship("Order", back_populates="items")
    part = relationship("Part", back_populates="order_items")
