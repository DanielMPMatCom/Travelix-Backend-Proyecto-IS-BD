from fastapi import APIRouter, HTTPException, Path, Depends
from sqlalchemy.orm import Session

from schemas import TouristTypeTouristAssociationSchema
from db.config import get_db
import db.crud.tourist_type_tourist_crud as crud


router = APIRouter(prefix="/tourist_type_tourist", tags=["tourist_type_tourist"])


@router.get("/list")
async def list_tourist_type_tourist(db:Session=Depends(get_db), skip:int=0, limit:int=10):
    return crud.list_tourist_type_tourist(db, skip, limit)

@router.post("/create", response_model=str)
async def create_tourist_type_tourist(tourust_type_tourist_create: TouristTypeTouristAssociationSchema, db: Session = Depends(get_db)):
    return crud.create_tourist_type_tourist(db, tourust_type_tourist_create)

@router.get("/delete/{tourist_id}/{tourist_type_id}", response_model=str)
async def delete_tourist_type_tourist(tourist_id: int, tourist_type_id:int, db: Session = Depends(get_db)):
    return crud.delete_tourist_type_tourist(db, tourist_id, tourist_type_id)
