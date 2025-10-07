from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database

router = APIRouter(prefix='/customers', tags=['Customers'])

@router.post('/', response_model=schemas.CustomerOut)
def create_customer(customer: schemas.CustomerBase, db: Session = Depends(database.get_db)):
    new_customer = models.Customer(**customer.model_dump())
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer

@router.get('/', response_model=list[schemas.CustomerOut])
def list_customers(db: Session = Depends(database.get_db)):
    return db.query(models.Customer).all()

@router.get('/{customer_id}', response_model=schemas.CustomerOut)
def get_customer(customer_id: int, db: Session = Depends(database.get_db)):
    c = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if not c:
        raise HTTPException(status_code=404, detail='Customer not found')
    return c

@router.delete('/{customer_id}')
def delete_customer(customer_id: int, db: Session = Depends(database.get_db)):
    c = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if not c:
        raise HTTPException(status_code=404, detail='Customer not found')
    db.delete(c)
    db.commit()
    return {'detail': 'Customer deleted'}
