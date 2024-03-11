from sqlalchemy.orm import Session
from models import HotelModel
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

def toModel(schema:HotelSchema) -> HotelModel:
    return HotelModel(
        # id=schema.id,
                      name=schema.name,
                      address=schema.address,
                      category=schema.category)

def toShema(model:HotelModel) -> HotelSchema:
    return HotelSchema(id=model.id,
                       name=model.name,
                       address=model.address,
                       category=model.category)