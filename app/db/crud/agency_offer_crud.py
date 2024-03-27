from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models import AgencyOfferAssociation
from schemas import AgencyOfferAssociationSchema
from db.crud.agency_crud import get_agency
from db.crud.offer_crud import get_offer

def list_agency_offer(db: Session, skip: int, limit: int):
    return db.query(AgencyOfferAssociation).offset(skip).limit(limit).all()

def get_agency_offer(db: Session, agency_id: int, offer_id: int):
    return db.query(AgencyOfferAssociation).filter(AgencyOfferAssociation.agency_id == agency_id, AgencyOfferAssociation.offer_id == offer_id).first()

def create_agency_offer(db: Session, agency_offer_create: AgencyOfferAssociation):

    agency = get_agency(db, agency_offer_create.agency_id)
    if agency is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agency not found")
    
    offer = get_offer(db, agency_offer_create.offer_id)
    if offer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Offer not found")
    
    agency_offer = get_agency_offer(db, agency_offer_create.agency_id, agency_offer_create.offer_id)
    if agency_offer is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Agency offer already exists")

    agency_offer = toModel(agency_offer_create)
    db.add(agency_offer)
    db.commit()
    db.refresh(agency_offer)

    return "Success"

def delete_agency_offer(db: Session, agency_id: int, offer_id: int):


    agency = get_agency(db, agency_id)
    if agency is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agency not found")
    
    offer = get_offer(db, offer_id)
    if offer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Offer not found")
    
    agency_offer = get_agency_offer(db, agency_id, offer_id)
    if agency_offer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agency Offer not found")


    db.delete(agency_offer)
    db.commit()

    return "Success"

def update_agency_offer(db: Session, agency_offer_update: AgencyOfferAssociationSchema):

    agency = get_agency(db, agency_offer_update.agency_id)
    if agency is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agency not found")
    
    offer = get_offer(db, agency_offer_update.offer_id)
    if offer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Offer not found")
    
    agency_offer = get_agency_offer(db, agency_offer_update.agency_id, agency_offer_update.offer_id)
    if agency_offer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agency Offer not found")
    
    if agency_offer_update.price is not None:
        agency_offer.price = agency_offer_update.price

    db.commit()

    return "Success"

def toModel(schema:AgencyOfferAssociationSchema) -> AgencyOfferAssociation:
    return AgencyOfferAssociation(agency_id=schema.agency_id,
                                      offer_id=schema.offer_id,
                                      price=schema.price)

def toShema(model:AgencyOfferAssociation) -> AgencyOfferAssociationSchema:
    return AgencyOfferAssociationSchema(agency_id=model.agency_id,
                                            offer_id=model.offer_id,
                                            price=model.price)