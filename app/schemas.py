from pydantic import BaseModel
from typing import Optional, List

class CustomerBase(BaseModel):
    full_name: str
    phone: Optional[str] = None
    address: Optional[str] = None

class CustomerOut(CustomerBase):
    id: int
    created_at: Optional[str] = None
    model_config = {"from_attributes": True}

class PartBase(BaseModel):
    name: str
    price: float
    quantity: int
    sku: Optional[str] = None
    description: Optional[str] = None

class PartOut(PartBase):
    id: int
    created_at: Optional[str] = None
    model_config = {"from_attributes": True}

class OrderItemIn(BaseModel):
    part_id: int
    qty: int

class OrderIn(BaseModel):
    customer_id: int
    items: List[OrderItemIn]

class OrderOut(BaseModel):
    id: int
    customer_id: int
    status: str
    total_amount: float
    items: List[dict] = []
    created_at: Optional[str] = None
    model_config = {"from_attributes": True}
