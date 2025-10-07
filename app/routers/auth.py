from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import jwt
from app import core

router = APIRouter()

class LoginIn(BaseModel):
    username: str
    password: str

@router.post('/login_json')
def login_json(payload: LoginIn):
    if payload.username == core.DEFAULT_ADMIN_USERNAME and payload.password == core.DEFAULT_ADMIN_PASSWORD:
        token = jwt.encode({'sub': payload.username}, core.SECRET_KEY, algorithm='HS256')
        return {'access_token': token, 'token_type': 'bearer'}
    raise HTTPException(status_code=401, detail='Invalid credentials')
