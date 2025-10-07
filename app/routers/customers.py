from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db

router = APIRouter()

@router.post('/', response_model=schemas.CustomerOut)
def create_customer(c: schemas.CustomerBase, db: Session = Depends(get_db), user=Depends(get_current_user)):
    cust = models.Customer(**c.dict())
    db.add(cust); db.commit(); db.refresh(cust)
    return cust

@router.get('/', response_model=List[schemas.CustomerOut])
def list_customers(skip: int=0, limit: int=100, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(models.Customer).offset(skip).limit(limit).all()

@router.get('/{id}', response_model=schemas.CustomerOut)
def get_customer(id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    cust = db.query(models.Customer).get(id)
    if not cust:
        raise HTTPException(status_code=404, detail='Not found')
    return cust

@router.put('/{id}', response_model=schemas.CustomerOut)
def update_customer(id:int, c: schemas.CustomerBase, db: Session = Depends(get_db), user=Depends(get_current_user)):
    cust = db.query(models.Customer).get(id)
    if not cust:
        raise HTTPException(status_code=404, detail='Not found')
    for k,v in c.dict().items():
        setattr(cust, k, v)
    db.add(cust); db.commit(); db.refresh(cust)
    return cust

@router.delete('/{id}')
def delete_customer(id:int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    cust = db.query(models.Customer).get(id)
    if not cust:
        raise HTTPException(status_code=404, detail='Not found')
    db.delete(cust); db.commit()
    return {'msg':'deleted'}
