from fastapi import APIRouter, HTTPException, Path, Depends
from sqlalchemy.orm import Session
from db.config import get_db

from schemas import TouristCreateSchema, TouristSchema, Token, TokenData
from db.crud.auth_crud import login_for_access_token
import db.crud.tourist_crud as crud


router = APIRouter(prefix="/tourist", tags=["tourist"])

@router.get("/list")
async def list_tourist(db:Session=Depends(get_db), skip:int=0, limit:int=10):
    return crud.list_tourist(db, skip, limit)

@router.post("/token", response_model=Token)
async def login(token = Depends(login_for_access_token)):
    return token


@router.post("/create", response_model=str)
async def create_tourist(tourist_create: TouristCreateSchema, db: Session = Depends(get_db)):
    return crud.create_tourist(db, tourist_create)

@router.get("/delete{tourist_id}", response_model=str)
async def delete_tourist(tourist_id: int, db: Session = Depends(get_db)):
    return crud.delete_tourist(db, tourist_id)

# @router.get("/me", response_model=TouristSchema)
# async def get_tourist_me(db: Session = Depends(get_db), current_user: TokenData = Depends(crud.get_current_active_user)):
#     return crud.get_tourist_me(db, current_user)