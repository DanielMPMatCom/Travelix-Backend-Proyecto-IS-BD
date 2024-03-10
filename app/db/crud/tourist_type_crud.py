from sqlalchemy.orm import Session
from models import TouristTypeModel
from schemas import TouristTypeSchema


def list_tourist_type(db: Session, skip: int, limit: int):
    return db.query(TouristTypeModel).offset(skip).limit(limit).all()

def toModel(schema:TouristTypeSchema) -> TouristTypeModel:
    return TouristTypeModel(id=schema.id,
                          name=schema.name)

def toShema(model:TouristTypeModel) -> TouristTypeSchema:
    return TouristTypeSchema(id=model.id,
                          name=model.name)