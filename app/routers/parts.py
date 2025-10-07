from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database

router = APIRouter(prefix='/parts', tags=['Parts'])

@router.post('/', response_model=schemas.PartOut)
def create_part(part: schemas.PartBase, db: Session = Depends(database.get_db)):
    new_part = models.Part(**part.model_dump())
    db.add(new_part)
    db.commit()
    db.refresh(new_part)
    return new_part

@router.get('/', response_model=list[schemas.PartOut])
def list_parts(db: Session = Depends(database.get_db)):
    return db.query(models.Part).all()

@router.get('/{part_id}', response_model=schemas.PartOut)
def get_part(part_id: int, db: Session = Depends(database.get_db)):
    p = db.query(models.Part).filter(models.Part.id == part_id).first()
    if not p:
        raise HTTPException(status_code=404, detail='Part not found')
    return p

@router.put('/{part_id}', response_model=schemas.PartOut)
def update_part(part_id: int, updated: schemas.PartBase, db: Session = Depends(database.get_db)):
    p = db.query(models.Part).filter(models.Part.id == part_id).first()
    if not p:
        raise HTTPException(status_code=404, detail='Part not found')
    for k, v in updated.model_dump().items():
        setattr(p, k, v)
    db.commit()
    db.refresh(p)
    return p

@router.delete('/{part_id}')
def delete_part(part_id: int, db: Session = Depends(database.get_db)):
    p = db.query(models.Part).filter(models.Part.id == part_id).first()
    if not p:
        raise HTTPException(status_code=404, detail='Part not found')
    db.delete(p)
    db.commit()
    return {'detail': 'Part deleted'}
