from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=schemas.OrderOut)
def create_order(order: schemas.OrderBase, db: Session = Depends(database.get_db)):
    customer = db.query(models.Customer).filter(models.Customer.id == order.customer_id).first()
    part = db.query(models.Part).filter(models.Part.id == order.part_id).first()

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    if not part:
        raise HTTPException(status_code=404, detail="Part not found")

    if order.quantity > part.quantity:
        raise HTTPException(status_code=400, detail="Not enough parts in stock")

    new_order = models.Order(
        customer_id=order.customer_id,
        part_id=order.part_id,
        quantity=order.quantity
    )
    db.add(new_order)

    # Ombordagi miqdorni kamaytirish
    part.quantity -= order.quantity
    db.commit()
    db.refresh(new_order)
    return new_order


@router.get("/", response_model=list[schemas.OrderOut])
def get_orders(db: Session = Depends(database.get_db)):
    return db.query(models.Order).all()


@router.delete("/{order_id}")
def delete_order(order_id: int, db: Session = Depends(database.get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # Buyurtma o‘chirilganda omborga qayta qo‘shish
    part = db.query(models.Part).filter(models.Part.id == order.part_id).first()
    if part:
        part.quantity += order.quantity

    db.delete(order)
    db.commit()
    return {"message": "Order deleted successfully"}
