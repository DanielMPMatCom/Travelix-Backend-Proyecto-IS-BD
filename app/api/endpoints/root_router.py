from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import db.crud.auth_crud as auth
from db.config import get_db
from schemas import Token, AuthSchema
from datetime import timedelta

router = APIRouter(prefix="", tags=["root"])

@router.post("/token")
async def login(from_data:OAuth2PasswordRequestForm=Depends(), db: Session = Depends(get_db)) -> Token:
    print(from_data.username)
    user = auth.authenticate_user(db, from_data.username, from_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username, "role": user.role}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer", role=user.role)



@router.post("/fake_token")
async def fake_login(from_data: AuthSchema, db: Session = Depends(get_db)):
    print(from_data.username)
    user = auth.authenticate_user(db, from_data.username, from_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username, "role": user.role}, expires_delta=access_token_expires
    )
    return {"Token" : Token(access_token=access_token, token_type="bearer", role=user.role), "id" : user.id}