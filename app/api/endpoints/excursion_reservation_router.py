from fastapi import APIRouter, HTTPException, Path, Depends
from sqlalchemy.orm import Session
from datetime import date

from schemas import ExcursionReservationSchema
from db.config import get_db
import db.crud.excursion_reservation_crud as crud


router = APIRouter(prefix="/excursion_reservation", tags=["excursion_reservation"])


@router.get("/list")
async def list_excursion_reservation(db:Session=Depends(get_db), skip:int=0, limit:int=10):
    return crud.list_excursion_reservation(db, skip, limit)

@router.post("/create", response_model=str)
async def create_excursion_reservation(excursion_reservation_create: ExcursionReservationSchema, db: Session = Depends(get_db)):
    return crud.create_excursion_reservation(db, excursion_reservation_create)

@router.get("/delete{excursion_id}{tourist_id}{reservation_date}", response_model=str)
async def delete_excursion_reservation(excursion_id: int, tourist_id: int, reservation_date: date, db: Session = Depends(get_db)):
    return crud.delete_excursion_reservation(db, excursion_id, tourist_id, reservation_date)

@router.get("/get_frequent_tourist_by_excursion/{excursion_id}")
async def get_frequent_tourist_by_excursion(excursion_id:int, db:Session=Depends(get_db)):
    return crud.frequent_tourist_by_excursion(db, excursion_id)