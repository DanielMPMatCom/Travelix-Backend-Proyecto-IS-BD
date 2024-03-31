from fastapi import APIRouter, HTTPException, Path, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from db.config import get_db

from schemas import TouristCreateSchema, TouristSchema, Token, TokenData, UserSchema
import db.crud.tourist_crud as crud
import db.crud.auth_crud as auth
from db.crud.auth_crud import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from datetime import timedelta

router = APIRouter(prefix="/tourist", tags=["tourist"])

@router.get("/list")
async def list_tourist(db:Session=Depends(get_db), skip:int=0, limit:int=10):
    return crud.list_tourist(db, skip, limit)

@router.post("/create", response_model=str)
async def create_tourist(tourist_create: TouristCreateSchema, db: Session = Depends(get_db)):
    return crud.create_tourist(db, tourist_create)

@router.get("/delete{tourist_id}", response_model=str)
async def delete_tourist(tourist_id: int, db: Session = Depends(get_db)):
    return crud.delete_tourist(db, tourist_id)

@router.get("/me", response_model=TouristSchema)
async def get_tourist_me(db: Session = Depends(get_db), current_user: UserSchema = Depends(auth.get_current_active_user)):
    if current_user.role != "tourist":
        raise HTTPException(status_code=400, detail="User is not a tourist")
    return current_user

@router.get("/get/{tourist_id}")
async def get_tourist(tourist_id: int, db: Session = Depends(get_db)):
    return crud.get_tourist(db, tourist_id)