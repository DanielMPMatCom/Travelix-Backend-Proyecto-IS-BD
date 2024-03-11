from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models import ExcursionReservation
from schemas import ExcursionReservationSchema
from db.crud.excursion_crud import get_excursion
from db.crud.tourist_crud import get_tourist


def list_excursion_reservation(db: Session, skip: int, limit: int):
    return db.query(ExcursionReservation).offset(skip).limit(limit).all()


def get_excursion_reservation(db: Session, excursion_id: int, tourist_id: int):
    return db.query(ExcursionReservation).filter(ExcursionReservation.excursion_id == excursion_id, ExcursionReservation.tourist_id == tourist_id).first()

def create_excursion_reservation(db: Session, excursion_reservation_create: ExcursionReservation):

    excursion = get_excursion(db, excursion_reservation_create.excursion_id)
    if excursion is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Excursion not found")
    
    tourist = get_tourist(db, excursion_reservation_create.tourist_id)
    if tourist is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tourist not found")
    
    excursion_reservation = get_excursion_reservation(db, excursion_reservation_create.excursion_id, excursion_reservation_create.tourist_id)
    if excursion_reservation is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Excursion Reservation already exists")

    excursion_reservation = toModel(excursion_reservation_create)
    db.add(excursion_reservation)
    db.commit()
    db.refresh(excursion_reservation)

    return "Success"

def toModel(schema:ExcursionReservationSchema) -> ExcursionReservation:
    return ExcursionReservation(excursion_id=schema.excursion_id,
                                tourist_id=schema.tourist_id,
                                reservation_date=schema.reservation_date)

def toShema(model:ExcursionReservation) -> ExcursionReservationSchema:
    return ExcursionReservationSchema(excursion_id=model.excursion_id,
                                      tourist_id=model.tourist_id,
                                      reservation_date=model.reservation_date)