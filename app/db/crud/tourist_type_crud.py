from fastapi import HTTPException, status
from sqlalchemy import delete
from sqlalchemy.orm import Session
from models import TouristTypeModel, TouristTypeTouristAssociation
from schemas import TouristTypeSchema


def list_tourist_type(db: Session, skip: int, limit: int):
    return db.query(TouristTypeModel).offset(skip).limit(limit).all()

def get_tourist_type(db: Session, id: int):
    return db.query(TouristTypeModel).filter(TouristTypeModel.id == id).first()

def create_tourist_type(db: Session, tourist_type_create: TouristTypeSchema):
    tourist_type = toModel(tourist_type_create)
    db.add(tourist_type)
    db.commit()
    db.refresh(tourist_type)

    return "Success"

def delete_tourist_type(db: Session, tourist_type_delete: TouristTypeSchema):

    tourist_type = get_tourist_type(db, tourist_type_delete.id)

    if tourist_type is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tourist type not found")
    
    db.execute(delete(TouristTypeTouristAssociation).where(TouristTypeTouristAssociation.tourist_type_id == tourist_type_delete.id))
    db.commit()

    db.delete(tourist_type)
    db.commit()

    return "Success"

def toModel(schema:TouristTypeSchema) -> TouristTypeModel:
    return TouristTypeModel(
        # id=schema.id,
                          name=schema.name)

def toShema(model:TouristTypeModel) -> TouristTypeSchema:
    return TouristTypeSchema(id=model.id,
                          name=model.name)