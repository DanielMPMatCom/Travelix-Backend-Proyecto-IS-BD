from sqlalchemy.orm import Session
from models import FacilityModel
from schemas import FacilitySchema


def list_facility(db: Session, skip: int, limit: int):
    return db.query(FacilityModel).offset(skip).limit(limit).all()

def toModel(schema:FacilitySchema) -> FacilityModel:
    return FacilityModel(id=schema.id,
                          description=schema.description)

def toShema(model:FacilityModel) -> FacilitySchema:
    return FacilitySchema(id=model.id,
                          description=model.description)