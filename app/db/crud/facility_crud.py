from sqlalchemy.orm import Session
from models import FacilityModel
from schemas import FacilitySchema


def list_facility(db: Session, skip: int, limit: int):
    return db.query(FacilityModel).offset(skip).limit(limit).all()

def get_facility(db: Session, id: int):
    return db.query(FacilityModel).filter(FacilityModel.id == id).first()

def create_facility(db: Session, facility_create: FacilitySchema):
    facility = toModel(facility_create)
    db.add(facility)
    db.commit()
    db.refresh(facility)

    return "Success"

def toModel(schema:FacilitySchema) -> FacilityModel:
    return FacilityModel(
        # id=schema.id,
                          description=schema.description)

def toShema(model:FacilityModel) -> FacilitySchema:
    return FacilitySchema(id=model.id,
                          description=model.description)