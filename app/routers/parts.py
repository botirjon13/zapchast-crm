from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models
from app.database import get_db
from app.security import decode_token
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(prefix="/parts", tags=["parts"])

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
def create_part(p: dict, db: Session = Depends(get_db), user = Depends(get_current_user)):
    # p expected: {"sku": "...", "name": "...", "description": "...", "price": 0}
    if not p.get("name"):
        raise HTTPException(status_code=400, detail="Name is required")
    price = p.get("price", 0)
    new = models.Part(
        sku=p.get("sku"),
        name=p.get("name"),
        description=p.get("description"),
        price=price
    )
    db.add(new)
    db.commit()
    db.refresh(new)
    return {"id": new.id, "sku": new.sku, "name": new.name, "description": new.description, "price": float(new.price or 0)}


@router.get("/")
def list_parts(db: Session = Depends(get_db), user = Depends(get_current_user), skip: int = 0, limit: int = 200):
    rows = db.query(models.Part).offset(skip).limit(limit).all()
    out = []
    for r in rows:
        out.append({"id": r.id, "sku": r.sku, "name": r.name, "description": r.description, "price": float(r.price or 0)})
    return out


@router.get("/{part_id}")
def get_part(part_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    r = db.query(models.Part).filter(models.Part.id == part_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Part not found")
    return {"id": r.id, "sku": r.sku, "name": r.name, "description": r.description, "price": float(r.price or 0)}


@router.put("/{part_id}")
def update_part(part_id: int, p: dict, db: Session = Depends(get_db), user = Depends(get_current_user)):
    r = db.query(models.Part).filter(models.Part.id == part_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Part not found")
    for k in ["sku", "name", "description", "price"]:
        if k in p:
            setattr(r, k, p[k])
    db.add(r)
    db.commit()
    db.refresh(r)
    return {"id": r.id, "sku": r.sku, "name": r.name, "description": r.description, "price": float(r.price or 0)}


@router.delete("/{part_id}")
def delete_part(part_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    r = db.query(models.Part).filter(models.Part.id == part_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Part not found")
    db.delete(r)
    db.commit()
    return {"detail": "Part deleted"}
