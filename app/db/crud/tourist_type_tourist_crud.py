from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models import TouristTypeTouristAssociation
from schemas import TouristTypeTouristAssociationSchema
from db.crud.tourist_crud import get_tourist
from db.crud.tourist_type_crud import get_tourist_type


def list_tourist_type_tourist(db: Session, skip: int, limit: int):
    return db.query(TouristTypeTouristAssociation).offset(skip).limit(limit).all()

def get_tourist_type_tourist(db: Session, tourist_type_id: int, tourist_id: int):
    return db.query(TouristTypeTouristAssociation).filter(TouristTypeTouristAssociation.tourist_type_id == tourist_type_id, TouristTypeTouristAssociation.tourist_id == tourist_id).first()

def create_tourist_type_tourist(db: Session, tourist_type_tourist_create: TouristTypeTouristAssociationSchema):

    tourist_type = get_tourist_type(db, tourist_type_tourist_create.tourist_type_id)
    if tourist_type is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tourist type not found")
    
    tourist = get_tourist(db, tourist_type_tourist_create.tourist_id)
    if tourist is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tourist not found")
    
    tourist_type_tourist = get_tourist_type_tourist(db, tourist_type_tourist_create.tourist_type_id, tourist_type_tourist_create.tourist_id)
    if tourist_type_tourist is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tourist_type tourist association already exists")

    tourist_type_tourist = toModel(tourist_type_tourist_create)
    db.add(tourist_type_tourist)
    db.commit()
    db.refresh(tourist_type_tourist)

    return "Success"

def delete_tourist_type_tourist(db: Session, tourist_id: int, tourist_type_id: int):


    tourist_type = get_tourist_type(db, tourist_type_id)
    if tourist_type is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tourist type not found")
    
    tourist = get_tourist(db, tourist_id)
    if tourist is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tourist not found")
    
    tourist_type_tourist = get_tourist_type_tourist(db, tourist_type_id, tourist_id)
    if tourist_type_tourist is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tourist_type tourist association not found")


    db.delete(tourist_type_tourist)
    db.commit()

    return "Success"

def toModel(schema:TouristTypeTouristAssociationSchema) -> TouristTypeTouristAssociation:
    return TouristTypeTouristAssociation(tourist_id=schema.tourist_id,
                                tourist_type_id=schema.tourist_type_id)

def toShema(model:TouristTypeTouristAssociation) -> TouristTypeTouristAssociationSchema:
    return TouristTypeTouristAssociationSchema(tourist_id=model.tourist_id,
                                               tourist_type_id=model.tourist_type_id)