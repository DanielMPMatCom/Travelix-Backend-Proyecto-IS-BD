from sqlalchemy.orm import Session
from models import ExcursionReservation
from schemas import ExcursionReservationSchema


def list_excursion_reservation(db: Session, skip: int, limit: int):
    return db.query(ExcursionReservation).offset(skip).limit(limit).all()

def toModel(schema:ExcursionReservationSchema) -> ExcursionReservation:
    return ExcursionReservation(excursion_id=schema.excursion_id,
                                tourist_id=schema.tourist_id,
                                reservation_date=schema.reservation_date)

def toShema(model:ExcursionReservation) -> ExcursionReservationSchema:
    return ExcursionReservationSchema(excursion_id=model.excursion_id,
                                      tourist_id=model.tourist_id,
                                      reservation_date=model.reservation_date)