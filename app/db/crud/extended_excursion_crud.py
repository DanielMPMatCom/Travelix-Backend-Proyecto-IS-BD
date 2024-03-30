from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models import ExtendedExcursionModel, HotelModel, PackageReservation, HotelExtendedExcursionAssociation, PackageModel
from schemas import ExtendedExcursionSchema, TimeInHotel
from typing import List


def list_extended_excursion(db: Session, skip: int, limit: int):
    return db.query(ExtendedExcursionModel).offset(skip).limit(limit).all()

def get_extended_excursion(db: Session, id: int):
    return db.query(ExtendedExcursionModel).filter(ExtendedExcursionModel.id == id).first()

def create_extended_excursion(db: Session, extended_excursion_create: ExtendedExcursionSchema, associated_hotels: List[TimeInHotel]):

    for hotel_excursion_association in associated_hotels:
        hotel = db.query(HotelModel).filter(HotelModel.id == hotel_excursion_association.hotel_id).first()
        if hotel is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hotel not found")
    
    if date_crash(associated_hotels):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Arrival Date must be before Departure Date")

    if date_overlap(associated_hotels):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Date Overlap")

    extended_excursion = toModel(extended_excursion_create)
    db.add(extended_excursion)
    db.commit()
    db.refresh(extended_excursion)

    for hotel_excursion_association in associated_hotels:
        hotel_extended_excursion = HotelExtendedExcursionAssociation(
                                        extended_excursion_id=extended_excursion.id,
                                        hotel_id=hotel_excursion_association.hotel_id,
                                        departure_date = hotel_excursion_association.departure_date,
                                        arrival_date=hotel_excursion_association.arrival_date)
        db.add(hotel_extended_excursion)
        db.commit()
        db.refresh(hotel_extended_excursion)


    return "Success"


def delete_extended_excursion(db: Session, extended_excursion_delete_id: int):

    extended_excursion = get_extended_excursion(db, extended_excursion_delete_id)

    if extended_excursion is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Extended Excursion not found")
    
    reserved_package_with_excursion = db.query(PackageModel).\
        join(PackageReservation, PackageModel.id == PackageReservation.package_id).\
        filter(PackageModel.extended_excursion_id == extended_excursion_delete_id).first()
    
    if reserved_package_with_excursion is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Can't delete this Extended Excursion because is is ivolved in a Package Reservation")
    
    db.delete(extended_excursion)
    db.commit()
    return "Success"

def update_extended_excursion(db: Session, extended_excursion_update: ExtendedExcursionSchema):

    extended_excursion = get_extended_excursion(db, extended_excursion_update.id)

    if extended_excursion is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Extended Excursion not found")
    
    reserved_package_with_excursion = db.query(PackageModel).\
        join(PackageReservation, PackageModel.id == PackageReservation.package_id).\
        filter(PackageModel.extended_excursion_id == extended_excursion_update.id).first()
    
    if reserved_package_with_excursion is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Can't update this Extended Excursion because is is ivolved in a Package Reservation")
    
    if extended_excursion_update.departure_day is not None:
        extended_excursion.departure_day = extended_excursion_update.departure_day
    if extended_excursion_update.departure_hour is not None:
        extended_excursion.departure_hour = extended_excursion_update.departure_hour
    if extended_excursion_update.departure_place is not None:
        extended_excursion.departure_place = extended_excursion_update.departure_place
    if extended_excursion_update.arrival_day is not None:
        extended_excursion.arrival_day = extended_excursion_update.arrival_day
    if extended_excursion_update.arrival_hour is not None:
        extended_excursion.arrival_hour = extended_excursion_update.arrival_hour
    if extended_excursion_update.arrival_place is not None:
        extended_excursion.arrival_place = extended_excursion_update.arrival_place
    if extended_excursion_update.price is not None:
        extended_excursion.price = extended_excursion_update.price
    if extended_excursion_update.photo_url is not None:
        extended_excursion.photo_url = extended_excursion_update.photo_url

    db.commit()

    return "Success"

def toModel(schema:ExtendedExcursionSchema) -> ExtendedExcursionModel:
    return ExtendedExcursionModel(
                            departure_day=schema.departure_day, 
                          departure_hour=schema.departure_hour, 
                          departure_place=schema.departure_place, 
                          arrival_day=schema.arrival_day,
                          arrival_hour=schema.arrival_hour,
                          arrival_place=schema.arrival_place,
                          price=schema.price
        )

def toShema(model:ExtendedExcursionModel) -> ExtendedExcursionSchema:
    return ExtendedExcursionSchema(excursion_id=model.excursion_id,
                                   departure_day=model.departure_day, 
                                    departure_hour=model.departure_hour, 
                                    departure_place=model.departure_place, 
                                    arrival_day=model.arrival_day,
                                    arrival_hour=model.arrival_hour,
                                    arrival_place=model.arrival_place,
                                    price=model.price)


def date_overlap(dates: List[TimeInHotel]):
    dates.sort(key=lambda x: x.arrival_date)

    for i in range(1, len(dates)):
        if dates[i].arrival_date < dates[i-1].departure_date or dates[i].arrival_date == dates[i-1].arrival_date:
            return True

    return False

def date_crash(dates: List[TimeInHotel]):

    for i in range(len(dates)):
        if dates[i].arrival_date >= dates[i].departure_date:
            return True
    return False