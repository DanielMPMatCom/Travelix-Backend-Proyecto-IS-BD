from sqlalchemy.orm import Session
from models import ExcursionModel
from schemas import ExcursionSchema


def list_excursion(db: Session, skip: int, limit: int):
    return db.query(ExcursionModel).offset(skip).limit(limit).all()

def get_excursion(db: Session, name: str):
    return db.query(ExcursionModel).filter(ExcursionModel.name == name).first()

def create_excursion(db: Session, excursion_create: ExcursionSchema):
    excursion = toModel(excursion_create)
    db.add(excursion)
    db.commit()
    db.refresh(excursion)

    return "Success"

def toModel(schema:ExcursionSchema) -> ExcursionModel:
    return ExcursionModel(
        # id=schema.id, 
                          departure_day=schema.departure_day, 
                          departure_hour=schema.departure_hour, 
                          departure_place=schema.departure_place, 
                          arrival_day=schema.arrival_day,
                          arrival_hour=schema.arrival_hour,
                          arrival_place=schema.arrival_place,
                          price=schema.price)

def toShema(model:ExcursionModel) -> ExcursionSchema:
    return ExcursionSchema(id=model.id, 
                           departure_day=model.departure_day, 
                           departure_hour=model.departure_hour, 
                           departure_place=model.departure_place, 
                           arrival_day=model.arrival_day,
                           arrival_hour=model.arrival_hour,
                           arrival_place=model.arrival_place,
                           price=model.price)