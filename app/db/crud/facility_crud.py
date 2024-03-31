from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models import FacilityModel, PackageFacilityAssociation
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

def delete_facility(db: Session, facility_delete_id: int):

    facility = get_facility(db, facility_delete_id)

    if facility is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Facility not found")

    db.delete(facility)
    db.commit()

    return "Success"

def update_facility(db: Session, facility_update: FacilitySchema):

    facility = get_facility(db, facility_update.id)

    if facility is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Facility not found")
    
    if facility_update.description is not None:
        facility.description = facility_update.description

    db.commit()

    return "Success"

def get_package_facilities(db: Session, package_id: int):
    return db.query(FacilityModel).join(PackageFacilityAssociation, PackageFacilityAssociation.facility_id == FacilityModel.id)\
    .filter(PackageFacilityAssociation.package_id == package_id).all()


def toModel(schema:FacilitySchema) -> FacilityModel:
    return FacilityModel(
                          description=schema.description)

def toShema(model:FacilityModel) -> FacilitySchema:
    return FacilitySchema(id=model.id,
                          description=model.description)