from fastapi import APIRouter, HTTPException, Path, Depends
from sqlalchemy.orm import Session

from schemas import HotelExtendedExcursionAssociationSchema
from db.config import get_db
import db.crud.hotel_extended_excursion_crud as crud


router = APIRouter(prefix="/hotel_extended_excursion", tags=["hotel_extended_excursion"])


@router.get("/list")
async def list_hotel_extended_excursion(db:Session=Depends(get_db), skip:int=0, limit:int=10):
    return crud.list_hotel_extended_excursion(db, skip, limit)

@router.post("/create", response_model=str)
async def create_hotel_extended_excursion(hotel_extended_excursion_create: HotelExtendedExcursionAssociationSchema, db: Session = Depends(get_db)):
    return crud.create_hotel_extended_excursion(db, hotel_extended_excursion_create)
