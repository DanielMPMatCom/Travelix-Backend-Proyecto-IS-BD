from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models import PackageFacilityAssociation
from schemas import PackageFacilityAssociationSchema
from db.crud.package_crud import get_package
from db.crud.facility_crud import get_facility


def list_package_facility(db: Session, skip: int, limit: int):
    return db.query(PackageFacilityAssociation).offset(skip).limit(limit).all()


def get_package_facility(db: Session, package_id: int, facility_id: int):
    return db.query(PackageFacilityAssociation).\
        filter(PackageFacilityAssociation.package_id == package_id, 
               PackageFacilityAssociation.facility_id == facility_id).first()

def create_package_facility(db: Session, package_facility_create: PackageFacilityAssociationSchema):

    package = get_package(db, package_facility_create.package_id)
    if package is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Package not found")
    
    facility = get_facility(db, package_facility_create.facility_id)
    if facility is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Facility not found")
    
    
    package_facility = get_package_facility(db, package_facility_create.package_id, package_facility_create.facility_id)
    if package_facility is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Excursion Reservation already exists")

    package_facility = toModel(package_facility_create)
    db.add(package_facility)
    db.commit()
    db.refresh(package_facility)

    return "Success"

def delete_package_facility(db: Session, package_id: int, facility_id: int):

    package = get_package(db, package_id)
    if package is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Package not found")

    facility = get_facility(db, facility_id)
    if facility is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Facility not found")
    
    package_facility = get_package_facility(db, package_id, facility_id)
    if package_facility is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Package facility not found")


    db.delete(package_facility)
    db.commit()

    return "Success"

def toModel(schema:PackageFacilityAssociationSchema) -> PackageFacilityAssociation:
    return PackageFacilityAssociation(
        package_id=schema.package_id,
        facility_id=schema.facility_id)

def toShema(model:PackageFacilityAssociation) -> PackageFacilityAssociationSchema:
    return PackageFacilityAssociationSchema(
                                      package_id=model.package_id,
                                        facility_id=model.facility_id)