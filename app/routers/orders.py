from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from decimal import Decimal
from app import models, schemas, database

router = APIRouter(prefix='/orders', tags=['Orders'])

@router.post('/', response_model=schemas.OrderOut)
def create_order(o: schemas.OrderIn, db: Session = Depends(database.get_db)):
    customer = db.query(models.Customer).filter(models.Customer.id == o.customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail='Customer not found')
    order = models.Order(customer_id=customer.id, status='created', total_amount=0)
    db.add(order)
    db.commit()
    db.refresh(order)
    total = Decimal(0)
    for it in o.items:
        part = db.query(models.Part).filter(models.Part.id == it.part_id).first()
        if not part:
            db.delete(order); db.commit()
            raise HTTPException(status_code=404, detail=f'Part {it.part_id} not found')
        if part.quantity < it.qty:
            db.delete(order); db.commit()
            raise HTTPException(status_code=400, detail=f'Not enough stock for part {part.id}')
        unit = Decimal(part.price or 0)
        line = unit * it.qty
        oi = models.OrderItem(order_id=order.id, part_id=part.id, qty=it.qty, unit_price=unit, line_total=line)
        db.add(oi)
        part.quantity -= it.qty
        total += line
    order.total_amount = total
    db.commit()
    db.refresh(order)
    items = []
    for it in order.items:
        items.append({'id': it.id, 'part_id': it.part_id, 'qty': it.qty, 'unit_price': float(it.unit_price), 'line_total': float(it.line_total)})
    return {'id': order.id, 'customer_id': order.customer_id, 'status': order.status, 'total_amount': float(order.total_amount), 'items': items, 'created_at': order.created_at.isoformat()}

@router.get('/', response_model=list[schemas.OrderOut])
def list_orders(db: Session = Depends(database.get_db)):
    orders = db.query(models.Order).all()
    out = []
    for o in orders:
        items = []
        for it in o.items:
            items.append({'id': it.id, 'part_id': it.part_id, 'qty': it.qty, 'unit_price': float(it.unit_price), 'line_total': float(it.line_total)})
        out.append({'id': o.id, 'customer_id': o.customer_id, 'status': o.status, 'total_amount': float(o.total_amount), 'items': items, 'created_at': o.created_at.isoformat()})
    return out

@router.get('/{order_id}', response_model=schemas.OrderOut)
def get_order(order_id: int, db: Session = Depends(database.get_db)):
    o = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not o:
        raise HTTPException(status_code=404, detail='Order not found')
    items = []
    for it in o.items:
        items.append({'id': it.id, 'part_id': it.part_id, 'qty': it.qty, 'unit_price': float(it.unit_price), 'line_total': float(it.line_total)})
    return {'id': o.id, 'customer_id': o.customer_id, 'status': o.status, 'total_amount': float(o.total_amount), 'items': items, 'created_at': o.created_at.isoformat()}

@router.delete('/{order_id}')
def delete_order(order_id: int, db: Session = Depends(database.get_db)):
    o = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not o:
        raise HTTPException(status_code=404, detail='Order not found')
    for it in o.items:
        part = db.query(models.Part).filter(models.Part.id == it.part_id).first()
        if part:
            part.quantity += it.qty
    db.delete(o)
    db.commit()
    return {'detail': 'Order deleted'}
