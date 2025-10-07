from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from app.security import hash_password, verify_password, create_access_token, decode_token
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from typing import Optional

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
@router.post("/login_json")
def login_json(payload: dict, db: Session = Depends(get_db)):
    username = payload.get("username")
    password = payload.get("password")
    if not username or not password:
        raise HTTPException(status_code=400, detail="username and password required")
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user.username, "user_id": user.id})
    return {"access_token": token, "token_type": "bearer"}

@router.post('/register', response_model=dict)
def register(u: schemas.UserCreate, db: Session = Depends(get_db)):
    # simple registration, no duplicate check for brevity
    existing = db.query(models.User).filter(models.User.username==u.username).first()
    if existing:
        raise HTTPException(status_code=400, detail='Username already exists')
    user = models.User(username=u.username, full_name=u.full_name, password_hash=hash_password(u.password))
    db.add(user); db.commit(); db.refresh(user)
    return {"msg":"user created","username":user.username}

@router.post('/login', response_model=schemas.Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username==form.username).first()
    if not user or not verify_password(form.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials')
    token = create_access_token({"sub": user.username, "user_id": user.id})
    return {"access_token": token, "token_type":"bearer"}

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail='Invalid token')
    username = payload.get('sub')
    user = db.query(models.User).filter(models.User.username==username).first()
    if not user:
        raise HTTPException(status_code=401, detail='User not found')
    return user
