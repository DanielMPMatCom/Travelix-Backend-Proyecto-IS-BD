from fastapi import HTTPException, status
from sqlalchemy import delete
from sqlalchemy.orm import Session
from models import ExcursionModel, ExcursionReservation, AgencyExcursionAssociation, PackageReservation, ExtendedExcursionModel, HotelExtendedExcursionAssociation, PackageModel
from schemas import ExcursionSchema


def list_excursion(db: Session, skip: int, limit: int):
    return db.query(ExcursionModel).offset(skip).limit(limit).all()

def get_excursion(db: Session, id: int):
    return db.query(ExcursionModel).filter(ExcursionModel.id == id).first()

def create_excursion(db: Session, excursion_create: ExcursionSchema):
    excursion = toModel(excursion_create)
    db.add(excursion)
    db.commit()
    db.refresh(excursion)

    return "Success"


def delete_excursion(db: Session, excursion_delete: ExcursionSchema):

    excursion = get_excursion(db, excursion_delete.id)

    if excursion is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Excursion not found")
    
    excursion_in_package_reservation = db.query(PackageReservation).filter(PackageReservation.extended_excursion_id == excursion_delete.id).first()
    if excursion_in_package_reservation is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Can't delete this Excursion because is is ivolved in a Package Reservation")
    
    excursion_reservation = db.query(ExcursionReservation).filter(ExcursionReservation.excursion_id == excursion_delete.id).first()
    if excursion_reservation is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Can't delete this Excursiom because is is ivolved in an Excursion Reservation")
    

    db.delete(excursion)
    db.commit()

    return "Success"

def update_excursion(db: Session, excursion_update: ExcursionSchema):

    excursion = get_excursion(db, excursion_update.id)

    if excursion is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Excursion not found")
    
    excursion_in_package_reservation = db.query(PackageReservation).filter(PackageReservation.extended_excursion_id == excursion_update.id).first()
    if excursion_in_package_reservation is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Can't update this Excursion because is is ivolved in a Package Reservation")
    
    excursion_reservation = db.query(ExcursionReservation).filter(ExcursionReservation.excursion_id == excursion_update.id).first()
    if excursion_reservation is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Can't update this Excursiom because is is ivolved in an Excursion Reservation")

    
    if excursion_update.departure_day is not None:
        excursion.departure_day = excursion_update.departure_day
    if excursion_update.departure_hour is not None:
        excursion.departure_hour = excursion_update.departure_hour
    if excursion_update.departure_place is not None:
        excursion.departure_place = excursion_update.departure_place
    if excursion_update.arrival_day is not None:
        excursion.arrival_day = excursion_update.arrival_day
    if excursion_update.arrival_hour is not None:
        excursion.arrival_hour = excursion_update.arrival_hour
    if excursion_update.arrival_place is not None:
        excursion.arrival_place = excursion_update.arrival_place
    if excursion_update.price is not None:
        excursion.price = excursion_update.price
    if excursion_update.photo_url is not None:
        excursion.photo_url = excursion_update.photo_url

    db.commit()

    return "Success"

def toModel(schema:ExcursionSchema) -> ExcursionModel:
    return ExcursionModel(
        # id=schema.id, 
                          departure_day=schema.departure_day, 
                          departure_hour=schema.departure_hour, 
                          departure_place=schema.departure_place, 
                          arrival_day=schema.arrival_day,
                          arrival_hour=schema.arrival_hour,
                          arrival_place=schema.arrival_place,
                          price=schema.price,
                          photo_url=schema.photo_url)

def toShema(model:ExcursionModel) -> ExcursionSchema:
    return ExcursionSchema(id=model.id, 
                           departure_day=model.departure_day, 
                           departure_hour=model.departure_hour, 
                           departure_place=model.departure_place, 
                           arrival_day=model.arrival_day,
                           arrival_hour=model.arrival_hour,
                           arrival_place=model.arrival_place,
                           price=model.price,
                           photo_url=model.photo_url)