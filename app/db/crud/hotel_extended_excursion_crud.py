from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models import HotelExtendedExcursionAssociation
from schemas import HotelExtendedExcursionAssociationSchema
from db.crud.hotel_crud import get_hotel
from db.crud.extended_excursion_crud import get_extended_excursion

def list_hotel_extended_excursion(db: Session, skip: int, limit: int):
    return db.query(HotelExtendedExcursionAssociation).offset(skip).limit(limit).all()

def get_hotel_extended_excursion(db: Session, hotel_id: int, extended_excursion_id: int):
    return db.query(HotelExtendedExcursionAssociation).filter(HotelExtendedExcursionAssociation.hotel_id == hotel_id, HotelExtendedExcursionAssociation.extended_excursion_id == extended_excursion_id).first()

def create_hotel_extended_excursion(db: Session, hotel_extended_excursion_create: HotelExtendedExcursionAssociation):

    hotel = get_hotel(db, hotel_extended_excursion_create.hotel_id)
    if hotel is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hotel not found")
    
    extended_excursion = get_extended_excursion(db, hotel_extended_excursion_create.extended_excursion_id)
    if extended_excursion is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Extended excursion not found")
    
    hotel_extended_excursion = get_hotel_extended_excursion(db, hotel_extended_excursion_create.hotel_id, hotel_extended_excursion_create.extended_excursion_id)
    if hotel_extended_excursion is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Hotel extended excursion association already exists")

    hotel_extended_excursion = toModel(hotel_extended_excursion_create)
    db.add(hotel_extended_excursion)
    db.commit()
    db.refresh(hotel_extended_excursion)

    return "Success"

def toModel(schema:HotelExtendedExcursionAssociationSchema) -> HotelExtendedExcursionAssociation:
    return HotelExtendedExcursionAssociation(hotel_id=schema.hotel_id,
                                      extended_excursion_id=schema.extended_excursion_id,
                                      departure_date = schema.departure_date,
                                        arrival_date=schema.arrival_date)

def toShema(model:HotelExtendedExcursionAssociation) -> HotelExtendedExcursionAssociationSchema:
    return HotelExtendedExcursionAssociationSchema(hotel_id=model.hotel_id,
                                      extended_excursion_id=model.extended_excursion_id,
                                      departure_date = model.departure_date,
                                        arrival_date=model.arrival_date)