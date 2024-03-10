from sqlalchemy.orm import Session
from models import TouristTypeTouristAssociation
from schemas import TouristTypeTouristAssociationSchema


def list_tourist_type_tourist(db: Session, skip: int, limit: int):
    return db.query(TouristTypeTouristAssociation).offset(skip).limit(limit).all()

def toModel(schema:TouristTypeTouristAssociationSchema) -> TouristTypeTouristAssociation:
    return TouristTypeTouristAssociation(tourist_id=schema.tourist_id,
                                tourist_type_id=schema.tourist_type_id)

def toShema(model:TouristTypeTouristAssociation) -> TouristTypeTouristAssociationSchema:
    return TouristTypeTouristAssociationSchema(tourist_id=model.tourist_id,
                                               tourist_type_id=model.tourist_type_id)