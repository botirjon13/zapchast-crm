from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import models, database

router = APIRouter(prefix='/stats', tags=['Stats'])

@router.get('/summary')
def summary(db: Session = Depends(database.get_db)):
    total_orders = db.query(models.Order).count()
    rows = db.query(models.Order.total_amount).all()
    total_revenue = float(sum([r[0] or 0 for r in rows]))
    parts = db.query(models.Part).all()
    stock_value = sum([float((p.price or 0) * (p.quantity or 0)) for p in parts])
    return {'total_orders': total_orders, 'total_revenue': total_revenue, 'stock_value': stock_value}
