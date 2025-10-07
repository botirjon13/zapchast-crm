from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class CustomerBase(BaseModel):
    name: str
    phone: str
    address: str

class CustomerOut(CustomerBase):
    id: int
    class Config:
        from_attributes = True

class PartBase(BaseModel):
    name: str
    price: float
    quantity: int

class PartOut(PartBase):
    id: int
    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    customer_id: int
    part_id: int
    quantity: int

class OrderOut(OrderBase):
    id: int
    class Config:
        from_attributes = True
