from fastapi import APIRouter, HTTPException, Path, Depends
from sqlalchemy.orm import Session

from schemas import TouristTypeSchema
from db.config import get_db
import db.crud.tourist_type_crud as crud


router = APIRouter(prefix="/tourist_type", tags=["tourist_type"])


@router.get("/list")
async def list_tourist_type(db:Session=Depends(get_db), skip:int=0, limit:int=10):
    return crud.list_tourist_type(db, skip, limit)

@router.post("/create", response_model=str)
async def create_tourist_type(tourist_type_create: TouristTypeSchema, db: Session = Depends(get_db)):
    return crud.create_tourist_type(db, tourist_type_create)

@router.get("/delete{tourist_type_id}", response_model=str)
async def delete_tourist_type(tourist_type_id: int, db: Session = Depends(get_db)):
    return crud.delete_tourist_type(db, tourist_type_id)
