from fastapi import APIRouter, HTTPException, Path, Depends, status
from sqlalchemy.orm import Session

from schemas import HotelSchema
from db.config import get_db
import db.crud.hotel_crud as crud


router = APIRouter(prefix="/hotel", tags=["hotel"])


@router.get("/list")
async def list_hotel(db:Session=Depends(get_db), skip:int=0, limit:int=10):
    return crud.list_hotel(db, skip, limit)

@router.post("/create", response_model=str)
async def create_hotel(hotel_create: HotelSchema, db: Session = Depends(get_db)):
    return crud.create_hotel(db, hotel_create)

@router.get("/delete{hotel_id}", response_model=str)
async def delete_hotel(hotel_id: int, db: Session = Depends(get_db)):
    return crud.delete_hotel(db, hotel_id)

@router.post("/update", response_model=str)
async def update_hotel(hotel_update: HotelSchema, db: Session = Depends(get_db)):
    return crud.update_hotel(db, hotel_update)

@router.get("/get/{hotel_id}", response_model=HotelSchema)
async def get_hotel(hotel_id: int, db: Session = Depends(get_db)):
    hotel = crud.get_hotel(db, hotel_id)
    return hotel if hotel is not None else HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="Hotel not found")
