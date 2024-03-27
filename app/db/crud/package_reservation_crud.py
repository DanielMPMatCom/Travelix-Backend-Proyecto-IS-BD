from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models import PackageReservation
from schemas import PackageReservationSchema
from db.crud.package_crud import get_package
from db.crud.tourist_crud import get_tourist
from datetime import date


def list_package_reservation(db: Session, skip: int, limit: int):
    return db.query(PackageReservation).offset(skip).limit(limit).all()


def get_package_reservation(db: Session, package_id: int, tourist_id: int, reservation_date: date):
    return db.query(PackageReservation).filter(PackageReservation.package_id == package_id, PackageReservation.tourist_id == tourist_id, PackageReservation.reservation_date == reservation_date).first()

def create_package_reservation(db: Session, package_reservation_create: PackageReservationSchema):

    package = get_package(db, package_reservation_create.package_id)
    if package is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Package not found")
    
    tourist = get_tourist(db, package_reservation_create.tourist_id)
    if tourist is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tourist not found")
    
    package_reservation = get_package_reservation(db, package_reservation_create.package_id, package_reservation_create.tourist_id, package_reservation_create.reservation_date)
    if package_reservation is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Package Reservation already exists")

    package_reservation = toModel(package_reservation_create)
    db.add(package_reservation)
    db.commit()
    db.refresh(package_reservation)

    return "Success"

def delete_package_reservation(db: Session, package_id: int, tourist_id: int, reservation_date: date):

    package = get_package(db, package_id)
    if package is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Package not found")

    tourist = get_tourist(db, tourist_id)
    if tourist is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tourist not found")
    
    package_reservation = get_package_reservation(db, package_id, tourist_id, reservation_date)
    if package_reservation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Package Reservation not found")


    db.delete(package_reservation)
    db.commit()

    return "Success"

def toModel(schema:PackageReservationSchema) -> PackageReservation:
    return PackageReservation(package_id=schema.package_id,
                                tourist_id=schema.tourist_id,
                                reservation_date=schema.reservation_date)

def toShema(model:PackageReservation) -> PackageReservationSchema:
    return PackageReservationSchema(package_id=model.package_id,
                                      tourist_id=model.tourist_id,
                                      reservation_date=model.reservation_date)