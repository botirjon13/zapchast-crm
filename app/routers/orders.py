from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from decimal import Decimal
from app import models
from app.database import get_db
from app.security import decode_token
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(prefix="/orders", tags=["orders"])

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
def create_order(body: dict, db: Session = Depends(get_db), user = Depends(get_current_user)):
    """
    Expected body:
    {
      "customer_id": 1,
      "items": [{"part_id": 1, "qty": 2}, ...]
    }
    """
    customer_id = body.get("customer_id")
    items = body.get("items") or []
    if not customer_id:
        raise HTTPException(status_code=400, detail="customer_id is required")
    customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    order = models.Order(customer_id=customer.id, user_id=user.id, status="confirmed", total_amount=Decimal(0))
    db.add(order)
    db.commit()
    db.refresh(order)

    total = Decimal(0)
    for it in items:
        part_id = it.get("part_id")
        qty = int(it.get("qty", 1))
        part = db.query(models.Part).filter(models.Part.id == part_id).first()
        if not part:
            db.delete(order)
            db.commit()
            raise HTTPException(status_code=404, detail=f"Part {part_id} not found")
        unit = Decimal(part.price or 0)
        line = unit * qty
        oi = models.OrderItem(order_id=order.id, part_id=part.id, qty=qty, unit_price=unit, line_total=line)
        db.add(oi)
        total += line

    order.total_amount = total
    db.add(order)
    db.commit()
    db.refresh(order)

    return {"id": order.id, "customer_id": order.customer_id, "user_id": order.user_id, "status": order.status, "total_amount": float(order.total_amount or 0)}


@router.get("/")
def list_orders(db: Session = Depends(get_db), user = Depends(get_current_user)):
    rows = db.query(models.Order).all()
    out = []
    for o in rows:
        out.append({
            "id": o.id,
            "customer_id": o.customer_id,
            "user_id": o.user_id,
            "status": o.status,
            "total_amount": float(o.total_amount or 0)
        })
    return out


@router.get("/{order_id}")
def get_order(order_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    o = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not o:
        raise HTTPException(status_code=404, detail="Order not found")
    items = db.query(models.OrderItem).filter(models.OrderItem.order_id)
