from fastapi import HTTPException, status
from sqlalchemy import delete
from sqlalchemy.orm import Session
from models import AgencyModel, AgencyExcursionAssociation, AgencyOfferAssociation, PackageModel
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

def delete_agency(db: Session, agency_delete: AgencySchema):

    agency = get_agency(db, agency_delete.id)

    if agency is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agency not found")
    
    db.execute(delete(AgencyExcursionAssociation).where(AgencyExcursionAssociation.agency_id == agency_delete.id))
    db.execute(delete(AgencyOfferAssociation).where(AgencyOfferAssociation.agency_id == agency_delete.id))
    db.execute(delete(PackageModel).where(PackageModel.agency_id == agency_delete.id))
    db.commit()

    db.delete(agency)
    db.commit()

    return "Success"

def toModel(schema:AgencySchema) -> AgencyModel:
    return AgencyModel(
        # id=schema.id, 
                       name=schema.name, 
                       address=schema.address, 
                       fax_number=schema.fax_number, 
                       email=schema.email)

def toShema(model:AgencyModel) -> AgencySchema:
    return AgencySchema(id=model.id, 
                        name=model.name, 
                        address=model.address, 
                        fax_number=model.fax_number, 
                        email=model.email)
