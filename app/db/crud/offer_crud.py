from sqlalchemy.orm import Session
from models import OfferModel
from schemas import OfferSchema


def list_offer(db: Session, skip: int, limit: int):
    return db.query(OfferModel).offset(skip).limit(limit).all()

def toModel(schema:OfferSchema) -> OfferModel:
    return OfferModel(id=schema.id,
                          price=schema.price,
                          description=schema.description,
                          hotel_id=schema.hotel_id)

def toShema(model:OfferModel) -> OfferSchema:
    return OfferSchema(id=model.id, 
                           price=model.price,
                           description=model.description,
                           hotel_id=model.hotel_id)