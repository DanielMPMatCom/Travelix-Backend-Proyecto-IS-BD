from sqlalchemy.orm import Session
from models import TouristTypeModel
from schemas import TouristTypeSchema


def list_tourist_type(db: Session, skip: int, limit: int):
    return db.query(TouristTypeModel).offset(skip).limit(limit).all()

def get_tourist_type(db: Session, name: str):
    return db.query(TouristTypeModel).filter(TouristTypeModel.name == name).first()

def create_tourist_type(db: Session, tourist_type_create: TouristTypeSchema):
    tourist_type = toModel(tourist_type_create)
    db.add(tourist_type)
    db.commit()
    db.refresh(tourist_type)

    return "Success"

def toModel(schema:TouristTypeSchema) -> TouristTypeModel:
    return TouristTypeModel(
        # id=schema.id,
                          name=schema.name)

def toShema(model:TouristTypeModel) -> TouristTypeSchema:
    return TouristTypeSchema(id=model.id,
                          name=model.name)