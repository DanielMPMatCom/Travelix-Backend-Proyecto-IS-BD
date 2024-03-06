from sqlalchemy.orm import Session
from models import AgencyModel
from schemas import AgencySchema


def list_agency(db: Session, skip: int = 0, limit: int = 100):
    return db.query(AgencyModel).offset(skip).limit(limit).all()

