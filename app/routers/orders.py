from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from app.routers.auth import get_current_user
from decimal import Decimal

router = APIRouter()

@router.post('/', response_model=schemas.OrderOut)
def create_order(o: schemas.OrderCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    customer = db.query(models.Customer).get(o.customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail='Customer not found')
    order = models.Order(customer_id=customer.id, user_id=user.id, status='confirmed')
    db.add(order); db.commit(); db.refresh(order)
    total = Decimal(0)
    for item in o.items:
        part = db.query(models.Part).get(item.part_id)
        if not part:
            raise HTTPException(status_code=404, detail=f'Part {item.part_id} not found')
        unit = part.price
        line = Decimal(item.qty) * Decimal(unit)
        oi = models.OrderItem(order_id=order.id, part_id=part.id, qty=item.qty, unit_price=unit, line_total=line)
        db.add(oi)
        total += line
    order.total_amount = total
    db.add(order); db.commit(); db.refresh(order)
    return order

@router.get('/', response_model=list)
def list_orders(db: Session = Depends(get_db), user=Depends(get_current_user)):
    orders = db.query(models.Order).all()
    out = []
    for o in orders:
        out.append({"id": o.id, "customer_id": o.customer_id, "user_id": o.user_id, "status": o.status, "total_amount": float(o.total_amount or 0)})
    return out
