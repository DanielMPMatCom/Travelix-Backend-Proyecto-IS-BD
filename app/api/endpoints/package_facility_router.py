from fastapi import APIRouter, HTTPException, Path, Depends
from sqlalchemy.orm import Session

from schemas import PackageFacilityAssociationSchema
from db.config import get_db
import db.crud.package_facility_crud as crud


router = APIRouter(prefix="/package_facility", tags=["package_facility"])


@router.get("/list")
async def list_package_facility(db:Session=Depends(get_db), skip:int=0, limit:int=10):
    return crud.list_package_facility(db, skip, limit)

@router.post("/create", response_model=str)
async def create_package_facility(package_facility_create: PackageFacilityAssociationSchema, db: Session = Depends(get_db)):
    return crud.create_package_facility(db, package_facility_create)

@router.get("/delete{package_id}/{faciliy_id}", response_model=str)
async def delete_package_facility(package_id: int, facility_id: int, db: Session = Depends(get_db)):
    return crud.delete_package_facility(db, package_id, facility_id)
