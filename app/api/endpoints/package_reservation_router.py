from fastapi import APIRouter, HTTPException, Path, Depends
from sqlalchemy.orm import Session

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

@router.post("/delete", response_model=str)
async def delete_package_reservation(package_reservation_delete: PackageReservationSchema, db: Session = Depends(get_db)):
    return crud.delete_package_reservation(db, package_reservation_delete)
