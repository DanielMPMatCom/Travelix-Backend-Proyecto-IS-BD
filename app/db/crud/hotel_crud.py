from fastapi import HTTPException, status
from sqlalchemy import delete
from sqlalchemy.orm import Session
from models import HotelModel, HotelExtendedExcursionAssociation, PackageModel, PackageReservation
from schemas import HotelSchema


def list_hotel(db: Session, skip: int, limit: int):
    return db.query(HotelModel).offset(skip).limit(limit).all()

def get_hotel_by_name(db: Session, name: str):
    return db.query(HotelModel).filter(HotelModel.name == name).first()

def get_hotel(db: Session, id: int):
    return db.query(HotelModel).filter(HotelModel.id == id).first()

def create_hotel(db: Session, hotel_create: HotelSchema):
    hotel = toModel(hotel_create)
    db.add(hotel)
    db.commit()
    db.refresh(hotel)

    return "Success"

def delete_hotel(db: Session, hotel_delete_id: int):

    hotel = get_hotel(db, hotel_delete_id)

    if hotel is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hotel not found")
    
    
    db.delete(hotel)
    db.commit()

    return "Success"

def update_hotel(db: Session, hotel_update: HotelSchema):

    hotel = get_hotel(db, hotel_update.id)
    if hotel is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hotel not found")

    extended_excursion_with_hotel = db.query(HotelExtendedExcursionAssociation).filter(HotelExtendedExcursionAssociation.hotel_id == hotel_update.id).all()
    if extended_excursion_with_hotel is not None:
        for excursion in extended_excursion_with_hotel:
            packages_with_extended_excursion = db.query(PackageModel).filter(PackageModel.extended_excursion_id == excursion.extended_excursion_id).all()
            if packages_with_extended_excursion is not None:
                for package in packages_with_extended_excursion:
                    package_reservation = db.query(PackageReservation).filter(PackageReservation.package_id == package.id).first()
                    if package_reservation is not None:
                        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Can't update this Hotel because it is involved in a Package Reservation") 

    if hotel_update.name is not None:
        hotel.name = hotel_update.name
    if hotel_update.address is not None:
        hotel.address = hotel_update.address
    if hotel_update.category is not None:
        hotel.category = hotel_update.category
    if hotel_update.photo_url is not None:
        hotel.photo_url = hotel_update.photo_url

    db.commit()

    return "Success"


def toModel(schema:HotelSchema) -> HotelModel:
    return HotelModel(
        # id=schema.id,
                      name=schema.name,
                      address=schema.address,
                      category=schema.category,
                      photo_url=schema.photo_url)

def toShema(model:HotelModel) -> HotelSchema:
    return HotelSchema(id=model.id,
                       name=model.name,
                       address=model.address,
                       category=model.category,
                       photo_url=model.photo_url)