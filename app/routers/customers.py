from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import Optional
from app import models
from app.database import get_db
from app.security import decode_token
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(prefix="/customers", tags=["customers"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    username = payload.get("sub")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


@router.post("/")
def create_customer(c: dict, db: Session = Depends(get_db), user = Depends(get_current_user)):
    # c expected: {"name": "...", "phone": "...", "email": "...", "address": "..."}
    if not c.get("name"):
        raise HTTPException(status_code=400, detail="Name is required")
    new = models.Customer(
        name=c.get("name"),
        phone=c.get("phone"),
        email=c.get("email"),
        address=c.get("address")
    )
    db.add(new)
    db.commit()
    db.refresh(new)
    return {"id": new.id, "name": new.name, "phone": new.phone, "email": new.email, "address": new.address}


@router.get("/")
def list_customers(db: Session = Depends(get_db), user = Depends(get_current_user), skip: int = 0, limit: int = 200):
    rows = db.query(models.Customer).offset(skip).limit(limit).all()
    out = []
    for r in rows:
        out.append({"id": r.id, "name": r.name, "phone": r.phone, "email": r.email, "address": r.address})
    return out


@router.get("/{customer_id}")
def get_customer(customer_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    r = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"id": r.id, "name": r.name, "phone": r.phone, "email": r.email, "address": r.address}


@router.put("/{customer_id}")
def update_customer(customer_id: int, c: dict, db: Session = Depends(get_db), user = Depends(get_current_user)):
    r = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Customer not found")
    for k in ["name", "phone", "email", "address"]:
        if k in c:
            setattr(r, k, c[k])
    db.add(r)
    db.commit()
    db.refresh(r)
    return {"id": r.id, "name": r.name, "phone": r.phone, "email": r.email, "address": r.address}


@router.delete("/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    r = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Customer not found")
    db.delete(r)
    db.commit()
    return {"detail": "Customer deleted"}
