# from fastapi import HTTPException, status
# from sqlalchemy.orm import Session
# from models import PackageFacilityAssociation
# from schemas import PackageFacilityAssociationSchema
# from db.crud.extended_excursion_crud import get_extended_excursion
# from db.crud.package_crud import get_package
# from db.crud.agency_crud import get_agency
# from db.crud.facility_crud import get_facility


# def list_package_facility(db: Session, skip: int, limit: int):
#     return db.query(PackageFacilityAssociation).offset(skip).limit(limit).all()


# def get_package_facility(db: Session, extended_excursion_id: int, agency_id: int, package_id: int, facility_id: int):
#     return db.query(PackageFacilityAssociation).filter(
#         PackageFacilityAssociation.extended_excursion_id == extended_excursion_id, 
#         PackageFacilityAssociation.agency_id == agency_id, 
#         PackageFacilityAssociation.package_id == package_id,
#         PackageFacilityAssociation.facility_id == facility_id).first()

# def create_package_facility(db: Session, package_facility_create: PackageFacilityAssociation):

#     excursion = get_extended_excursion(db, package_facility_create.extended_excursion_id)
#     if excursion is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Excursion not found")
    
#     tourist = get_agency(db, package_facility_create.agency_id)
#     if tourist is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tourist not found")
    
#     facility = get_facility(db, package_facility_create.facility_id)
#     if facility is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Facility not found")
    
#     package = get_package(db, package_facility_create.package_id)
#     if package is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Package not found")
    
#     package_facility = get_package_facility(db, package_facility_create.extended_excursion_id, package_facility_create.agency_id)
#     if package_facility is not None:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Excursion Reservation already exists")

#     package_facility = toModel(package_facility_create)
#     db.add(package_facility)
#     db.commit()
#     db.refresh(package_facility)

#     return "Success"

# def toModel(schema:PackageFacilityAssociationSchema) -> PackageFacilityAssociation:
#     return PackageFacilityAssociation(
#         extended_excursion_id=schema.extended_excursion_id,
#         agency_id=schema.agency_id,
#         package_id=schema.package_id,
#         facility_id=schema.facility_id,
#         reservation_date=schema.reservation_date)

# def toShema(model:PackageFacilityAssociation) -> PackageFacilityAssociationSchema:
#     return PackageFacilityAssociationSchema(
#         extended_excursion_id=model.extended_excursion_id,
#                                       agency_id=model.agency_id,
#                                       package_id=model.package_id,
#                                         facility_id=model.facility_id,
#                                       reservation_date=model.reservation_date)