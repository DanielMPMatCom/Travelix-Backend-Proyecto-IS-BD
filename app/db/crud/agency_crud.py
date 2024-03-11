from sqlalchemy.orm import Session
from models import AgencyModel
from schemas import AgencySchema


def list_agency(db: Session, skip: int, limit: int):
    return db.query(AgencyModel).offset(skip).limit(limit).all()

def get_agency(db: Session, name: str):
    return db.query(AgencyModel).filter(AgencyModel.name == name).first()

def create_agency(db: Session, agency_create: AgencySchema):
    agency = toModel(agency_create)
    db.add(agency)
    db.commit()
    db.refresh(agency)

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
