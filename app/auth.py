from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter(prefix="/api/auth", tags=["Autenticação"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

@router.post("/login")
def login_corporativo():
    return {"access_token": "token_corporativo_folgaguard", "token_type": "bearer"}
