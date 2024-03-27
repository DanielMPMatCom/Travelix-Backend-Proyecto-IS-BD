from fastapi import APIRouter, HTTPException, Path, Depends
from sqlalchemy.orm import Session
from datetime import date

from schemas import PackageReservationSchema
from db.config import get_db
import db.crud.package_reservation_crud as crud


router = APIRouter(prefix="/package_reservation", tags=["package_reservation"])


@router.get("/list")
async def list_package_reservation(db:Session=Depends(get_db), skip:int=0, limit:int=10):
    return crud.list_package_reservation(db, skip, limit)

@router.post("/create", response_model=str)
async def create_package_reservation(package_reservation_create: PackageReservationSchema, db: Session = Depends(get_db)):
    return crud.create_package_reservation(db, package_reservation_create)

@router.get("/delete{package_id}{tourist_id}{reservation_date}", response_model=str)
async def delete_package_reservation(package_id: int, tourist_id: int, reservation_date: date, db: Session = Depends(get_db)):
    return crud.delete_package_reservation(db, package_id, tourist_id, reservation_date)
