from fastapi import HTTPException, status
from sqlalchemy import delete
from sqlalchemy.orm import Session
from models import HotelModel, HotelExtendedExcursionAssociation, OfferModel, AgencyOfferAssociation
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