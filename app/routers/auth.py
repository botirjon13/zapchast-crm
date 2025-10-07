from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from app.security import hash_password, verify_password, create_access_token, decode_token
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

@router.post('/login', response_model=schemas.Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username==form.username).first()
    if not user or not verify_password(form.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials')
    token = create_access_token({'sub': user.username, 'user_id': user.id})
    return {'access_token': token, 'token_type':'bearer'}

@router.post('/login_json', response_model=schemas.Token)
def login_json(payload: dict, db: Session = Depends(get_db)):
    username = payload.get('username')
    password = payload.get('password')
    if not username or not password:
        raise HTTPException(status_code=400, detail='username and password required')
    user = db.query(models.User).filter(models.User.username==username).first()
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials')
    token = create_access_token({'sub': user.username, 'user_id': user.id})
    return {'access_token': token, 'token_type':'bearer'}
