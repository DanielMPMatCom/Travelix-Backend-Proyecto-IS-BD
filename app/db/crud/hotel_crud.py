from sqlalchemy.orm import Session
from models import HotelModel
from schemas import HotelSchema


def list_hotel(db: Session, skip: int, limit: int):
    return db.query(HotelModel).offset(skip).limit(limit).all()

def toModel(schema:HotelSchema) -> HotelModel:
    return HotelModel(id=schema.id,
                      name=schema.name,
                      address=schema.address,
                      category=schema.category)

def toShema(model:HotelModel) -> HotelSchema:
    return HotelSchema(id=model.id,
                       name=model.name,
                       address=model.address,
                       category=model.category)