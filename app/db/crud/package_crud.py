from sqlalchemy.orm import Session
from models import PackageModel
from schemas import PackageSchema


def list_package(db: Session, skip: int, limit: int):
    return db.query(PackageModel).offset(skip).limit(limit).all()

def toModel(schema:PackageSchema) -> PackageModel:
    return PackageModel(id=schema.id,
                        agency_id=schema.agency_id,
                        extended_excursion_id=schema.extended_excursion_id,
                        duration=schema.duration,
                        description=schema.description,
                        price=schema.price)

def toShema(model:PackageModel) -> PackageSchema:
    return PackageSchema(id=model.id,
                         agency_id=model.agency_id,
                         extended_excursion_id=model.extended_excursion_id,
                         duration=model.duration,
                         description=model.description,
                         price=model.price)