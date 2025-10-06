from pydantic import BaseModel, Field
from typing import Optional, List
from decimal import Decimal

class UserCreate(BaseModel):
    username: str
    password: str
    full_name: Optional[str]

class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'

class CustomerBase(BaseModel):
    name: str
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None

class CustomerOut(CustomerBase):
    id: int
    created_at: Optional[str]
    class Config:
        orm_mode = True

class PartBase(BaseModel):
    sku: Optional[str] = None
    name: str
    description: Optional[str] = None
    price: Decimal = Field(default=0)

class PartOut(PartBase):
    id: int
    created_at: Optional[str]
    class Config:
        orm_mode = True

class OrderItemCreate(BaseModel):
    part_id: int
    qty: int

class OrderCreate(BaseModel):
    customer_id: int
    items: List[OrderItemCreate]

class OrderOut(BaseModel):
    id: int
    customer_id: int
    user_id: Optional[int]
    status: str
    total_amount: Decimal
    class Config:
        orm_mode = True
