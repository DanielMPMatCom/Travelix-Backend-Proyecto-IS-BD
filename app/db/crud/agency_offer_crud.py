from sqlalchemy.orm import Session
from models import AgencyOfferAssociation
from schemas import AgencyOfferAssociationSchema


def list_agency_offer(db: Session, skip: int, limit: int):
    return db.query(AgencyOfferAssociation).offset(skip).limit(limit).all()

def toModel(schema:AgencyOfferAssociationSchema) -> AgencyOfferAssociation:
    return AgencyOfferAssociation(agency_id=schema.agency_id,
                                      offer_id=schema.offer_id,
                                      price=schema.price)

def toShema(model:AgencyOfferAssociation) -> AgencyOfferAssociationSchema:
    return AgencyOfferAssociationSchema(agency_id=model.agency_id,
                                            offer_id=model.offer_id,
                                            price=model.price)