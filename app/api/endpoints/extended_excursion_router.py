from fastapi import APIRouter, HTTPException, Path, Depends, status
from sqlalchemy.orm import Session
from typing import List

from schemas import ExtendedExcursionSchema, HotelExtendedExcursionAssociationSchema, TimeInHotel
from db.config import get_db
import db.crud.extended_excursion_crud as crud


router = APIRouter(prefix="/extended_excursion", tags=["extended_excursion"])


@router.get("/list")
async def list_extended_excursion(db:Session=Depends(get_db), skip:int=0, limit:int=10):
    return crud.list_extended_excursion(db, skip, limit)

@router.post("/create", response_model=str)
async def create_extended_excursion(extended_excursion_create: ExtendedExcursionSchema, associated_hotels: List[TimeInHotel], db: Session = Depends(get_db)):
    return crud.create_extended_excursion(db, extended_excursion_create, associated_hotels)

@router.get("/delete/{extended_excursion_id}", response_model=str)
async def delete_extended_excursion(extended_excursion_id: int, db: Session = Depends(get_db)):
    return crud.delete_extended_excursion(db, extended_excursion_id)

@router.post("/update", response_model=str)
async def update_extended_excursion(extended_excursion_update: ExtendedExcursionSchema, db: Session = Depends(get_db)):
    return crud.update_extended_excursion(db, extended_excursion_update)

@router.get("/get/{extended_excursion_id}")
async def get_extended_excursion(extended_excursion_id: int, db: Session = Depends(get_db)):
    extended_excursion = crud.get_extended_excursion(db, extended_excursion_id)
    return extended_excursion if extended_excursion is not None else HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="Extended Excursion not found")

