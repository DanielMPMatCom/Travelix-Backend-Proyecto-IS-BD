from fastapi import APIRouter, HTTPException, Path, Depends
from sqlalchemy.orm import Session

from schemas import FacilitySchema
from db.config import get_db
import db.crud.facility_crud as crud


router = APIRouter(prefix="/facility", tags=["facility"])


@router.get("/list")
async def list_facility(db:Session=Depends(get_db), skip:int=0, limit:int=10):
    return crud.list_facility(db, skip, limit)

@router.post("/create", response_model=str)
async def create_facility(facility_create: FacilitySchema, db: Session = Depends(get_db)):
    return crud.create_facility(db, facility_create)

@router.get("/delete{facility_id}", response_model=str)
async def delete_facility(facility_id: int, db: Session = Depends(get_db)):
    return crud.delete_facility(db, facility_id)

@router.post("/update", response_model=str)
async def update_facility(facility_update: FacilitySchema, db: Session = Depends(get_db)):
    return crud.update_facility(db, facility_update)

@router.get("/package_facilities/{package_id}")
async def get_package_facilities(package_id: int, db: Session = Depends(get_db)):
    return crud.get_package_facilities(db, package_id)
