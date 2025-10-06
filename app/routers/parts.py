from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from app.routers.auth import get_current_user

router = APIRouter()

@router.post('/', response_model=schemas.PartOut)
def create_part(p: schemas.PartBase, db: Session = Depends(next(get_db)), user=Depends(get_current_user)):
    part = models.Part(**p.dict())
    db.add(part); db.commit(); db.refresh(part)
    return part

@router.get('/', response_model=List[schemas.PartOut])
def list_parts(skip:int=0, limit:int=100, db: Session = Depends(next(get_db)), user=Depends(get_current_user)):
    return db.query(models.Part).offset(skip).limit(limit).all()

@router.get('/{id}', response_model=schemas.PartOut)
def get_part(id:int, db: Session = Depends(next(get_db)), user=Depends(get_current_user)):
    part = db.query(models.Part).get(id)
    if not part:
        raise HTTPException(status_code=404, detail='Not found')
    return part

@router.put('/{id}', response_model=schemas.PartOut)
def update_part(id:int, p: schemas.PartBase, db: Session = Depends(next(get_db)), user=Depends(get_current_user)):
    part = db.query(models.Part).get(id)
    if not part:
        raise HTTPException(status_code=404, detail='Not found')
    for k,v in p.dict().items():
        setattr(part, k, v)
    db.add(part); db.commit(); db.refresh(part)
    return part

@router.delete('/{id}')
def delete_part(id:int, db: Session = Depends(next(get_db)), user=Depends(get_current_user)):
    part = db.query(models.Part).get(id)
    if not part:
        raise HTTPException(status_code=404, detail='Not found')
    db.delete(part); db.commit()
    return {'msg':'deleted'}
