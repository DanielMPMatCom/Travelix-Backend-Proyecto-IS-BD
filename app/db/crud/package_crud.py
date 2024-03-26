from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models import PackageModel, PackageReservation
from schemas import PackageSchema
from db.crud.agency_crud import get_agency
from db.crud.extended_excursion_crud import get_extended_excursion


def list_package(db: Session, skip: int, limit: int):
    return db.query(PackageModel).offset(skip).limit(limit).all()

def get_package(db: Session, agency_id: int, extended_excursion_id: int):
    return db.query(PackageModel).filter(PackageModel.agency_id == agency_id, PackageModel.extended_excursion_id == extended_excursion_id).first()

def create_package(db: Session, package_create: PackageSchema):

    agency = get_agency(db, package_create.agency_id)
    if agency is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agency not found")
    
    extended_excursion = get_extended_excursion(db, package_create.extended_excursion_id)
    if extended_excursion is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Extended excursion not found")
    
    package = get_package(db, package_create.agency_id, package_create.extended_excursion_id)
    if package is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Package already exists")

    package = toModel(package_create)
    db.add(package)
    db.commit()
    db.refresh(package)

    return "Success"

def delete_package(db: Session, package_delete: PackageSchema):


    agency = get_agency(db, package_delete.agency_id)
    if agency is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agency not found")
    
    extended_excursion = get_extended_excursion(db, package_delete.extended_excursion_id)
    if extended_excursion is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Extended excursion not found")
    
    package = get_package(db, package_delete.agency_id, package_delete.extended_excursion_id)
    if package is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Package not found")

    package_in_reservation = db.query(PackageReservation).filter(PackageReservation.package_id == package_delete.id).first()
    if package_in_reservation is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Can't delete this Package because is is ivolved in a Package Reservation")

    db.delete(package)
    db.commit()

    return "Success"

def update_package(db: Session, package_update: PackageSchema):

    agency = get_agency(db, package_update.agency_id)
    if agency is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agency not found")
    
    extended_excursion = get_extended_excursion(db, package_update.extended_excursion_id)
    if extended_excursion is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Extended excursion not found")
    
    package = get_package(db, package_update.agency_id, package_update.extended_excursion_id)
    if package is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Package not found")
    
    package_in_reservation = db.query(PackageReservation).filter(PackageReservation.package_id == package_update.id).first()
    if package_in_reservation is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Can't update this Package because is is ivolved in a Package Reservation")
    
    if package_update.price is not None:
        package.price = package_update.price
    if package_update.description is not None:
        package.description = package_update.description
    if package_update.duration is not None:
        package.duration = package_update.duration
    if package_update.photo_url is not None:
        package.photo_url = package_update.photo_url
    


    db.commit()

    return "Success"

from models import HotelModel

def get_package_hotels(db:Session, package_id:int):
    package = get_package(db, package_id)
    if package is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Package not found")
    
    


def toModel(schema:PackageSchema) -> PackageModel:
    return PackageModel(
        # id=schema.id,
                        agency_id=schema.agency_id,
                        extended_excursion_id=schema.extended_excursion_id,
                        duration=schema.duration,
                        description=schema.description,
                        price=schema.price,
                        photo_url=schema.photo_url)

def toShema(model:PackageModel) -> PackageSchema:
    return PackageSchema(id=model.id,
                         agency_id=model.agency_id,
                         extended_excursion_id=model.extended_excursion_id,
                         duration=model.duration,
                         description=model.description,
                         price=model.price,
                         photo_url=model.photo_url)