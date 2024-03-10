from sqlalchemy.orm import Session
from models import AgencyExcursionAssociation
from schemas import AgencyExcursionAssociationSchema


def list_agency_excursion(db: Session, skip: int, limit: int):
    return db.query(AgencyExcursionAssociation).offset(skip).limit(limit).all()

def toModel(schema:AgencyExcursionAssociationSchema) -> AgencyExcursionAssociation:
    return AgencyExcursionAssociation(agency_id=schema.agency_id,
                                      excursion_id=schema.excursion_id)

def toShema(model:AgencyExcursionAssociation) -> AgencyExcursionAssociationSchema:
    return AgencyExcursionAssociationSchema(agency_id=model.agency_id,
                                            excursion_id=model.excursion_id)