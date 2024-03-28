from fastapi import APIRouter, HTTPException, Path, Depends, status
from sqlalchemy.orm import Session

from schemas import PackageSchema, HotelSchema
from db.config import get_db
import db.crud.package_crud as crud


router = APIRouter(prefix="/package", tags=["package"])


@router.get("/list")
async def list_package(db:Session=Depends(get_db), skip:int=0, limit:int=10):
    return crud.list_package(db, skip, limit)

@router.post("/create", response_model=str)
async def create_package(package_create: PackageSchema, db: Session = Depends(get_db)):
    return crud.create_package(db, package_create)

@router.get("/delete{package_id}", response_model=str)
async def delete_package(package_id: int, db: Session = Depends(get_db)):
    return crud.delete_package(db, package_id)

@router.post("/update", response_model=str)
async def update_package(package_update: PackageSchema, db: Session = Depends(get_db)):
    return crud.update_package(db, package_update)

@router.get("/get/{package_id}", response_model=PackageSchema)
async def get_package(package_id: int, db: Session = Depends(get_db)):
    package = crud.get_package(db, package_id)
    return package if package is not None else HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="Package not found")

@router.get("/get_related_hotels/{package_id}")
async def get_related_hotels(package_id: int, db: Session=Depends(get_db)):
    return crud.get_package_hotels(db, package_id)

