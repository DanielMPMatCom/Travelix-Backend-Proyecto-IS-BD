from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from models import AgencyModel, PackageReservation, AgencyExcursionAssociation, ExcursionReservation, PackageModel, ExcursionModel
from schemas import AgencySchema


def list_agency(db: Session, skip: int, limit: int):
    return db.query(AgencyModel).offset(skip).limit(limit).all()

def get_agency(db: Session, id: int):
    return db.query(AgencyModel).filter(AgencyModel.id == id).first()

def create_agency(db: Session, agency_create: AgencySchema):
    agency = toModel(agency_create)
    db.add(agency)
    db.commit()
    db.refresh(agency)

    return "Success"

def delete_agency(db: Session, agency_delete_id: int):

    agency = get_agency(db, agency_delete_id)
    if agency is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agency not found")
    
    reserved_package_with_agency = db.query(PackageModel).\
        join(PackageReservation, PackageModel.id == PackageReservation.package_id).\
        filter(PackageModel.agency_id == agency_delete_id).first()

    if reserved_package_with_agency is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Can't delete this Agency because is is ivolved in a Package Reservation")

    reserved_excursion_with_agency = db.query(AgencyExcursionAssociation).\
        join(ExcursionReservation, AgencyExcursionAssociation.excursion_id == ExcursionReservation.excursion_id).\
        filter(AgencyExcursionAssociation.agency_id == agency_delete_id).first()
        
    if reserved_excursion_with_agency is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Can't delete this Agency because is is ivolved in an Excursion Reservation")
    
    db.delete(agency)
    db.commit()

    return "Success"

def update_agency(db: Session, agency_update: AgencySchema):

    agency = get_agency(db, agency_update.id)
    if agency is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agency not found")
    
    reserved_package_with_agency = db.query(PackageModel).\
        join(PackageReservation, PackageModel.id == PackageReservation.package_id).\
        filter(PackageModel.agency_id == agency_update.id).first()

    if reserved_package_with_agency is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Can't update this Agency because is is ivolved in a Package Reservation")

    reserved_excursion_with_agency = db.query(AgencyExcursionAssociation).\
        join(ExcursionReservation, AgencyExcursionAssociation.excursion_id == ExcursionReservation.excursion_id).\
        filter(AgencyExcursionAssociation.agency_id == agency_update.id).first()
        
    if reserved_excursion_with_agency is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Can't update this Agency because is is ivolved in an Excursion Reservation")
  
    if agency_update.name is not None:
        agency.name = agency_update.name
    if agency_update.address is not None:
        agency.address = agency_update.address
    if agency_update.fax_number is not None:
        agency.fax_number = agency_update.fax_number
    if agency_update.email is not None:
        agency.email = agency_update.email
    if agency_update.photo_url is not None:
        agency.photo_url = agency_update.photo_url

    db.commit()

    return "Success"

def toModel(schema:AgencySchema) -> AgencyModel:
    return AgencyModel(
                       name=schema.name, 
                       address=schema.address, 
                       fax_number=schema.fax_number, 
                       email=schema.email,
                       photo_url=schema.photo_url)

def toShema(model:AgencyModel) -> AgencySchema:
    return AgencySchema(id=model.id, 
                        name=model.name, 
                        address=model.address, 
                        fax_number=model.fax_number, 
                        email=model.email,
                        photo_url=model.photo_url)

def agency_balance_by_agency(db: Session, agency_id: int):

    excursion_reservation_query = db.query(
        AgencyExcursionAssociation.agency_id.label('agency_id'),
        func.count(ExcursionModel.id).label('excursion_reservation_count'),
        func.sum(ExcursionModel.price).label('excursion_reservation_total')).\
            join(AgencyExcursionAssociation, AgencyExcursionAssociation.excursion_id == ExcursionModel.id).\
            join(ExcursionReservation, ExcursionReservation.excursion_id == ExcursionModel.id).\
            filter(AgencyExcursionAssociation.agency_id == agency_id).\
            group_by(AgencyExcursionAssociation.agency_id)

    package_reservation_query = db.query(
        PackageModel.agency_id.label('agency_id'),
        func.count(PackageModel.id).label('package_reservation_count'),
        func.sum(PackageModel.price).label('package_reservation_total')).\
            join(PackageReservation, PackageReservation.package_id == PackageModel.id).\
            filter(PackageModel.agency_id == agency_id).\
            group_by(PackageModel.agency_id)

    excursion_reservation_subquery = excursion_reservation_query.subquery()
    package_reservation_subquery = package_reservation_query.subquery()

    final_query = db.query(
        AgencyModel.id,
        func.coalesce(excursion_reservation_subquery.c.excursion_reservation_count, 0) + func.coalesce(package_reservation_subquery.c.package_reservation_count, 0), 
        func.coalesce(excursion_reservation_subquery.c.excursion_reservation_total, 0) + func.coalesce(package_reservation_subquery.c.package_reservation_total, 0)).\
            outerjoin(excursion_reservation_subquery, AgencyModel.id == excursion_reservation_subquery.c.agency_id).\
                outerjoin(package_reservation_subquery, AgencyModel.id == package_reservation_subquery.c.agency_id).\
                    filter(AgencyModel.id == agency_id).all()

    final_result = [
        {
        "agency_id": result[0],
        "reservation_count": result[1],
        "reservation_total": result[2]
        }  
        for result in final_query]

    return final_result