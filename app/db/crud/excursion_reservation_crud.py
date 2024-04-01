from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models import (
    ExcursionReservation,
    TouristModel,
    ExtendedExcursionModel,
    AgencyExcursionAssociation,
    ExcursionModel,
    AgencyModel
)
from schemas import ExcursionReservationSchema
from db.crud.excursion_crud import get_excursion
from db.crud.tourist_crud import get_tourist
from db.crud.agency_excursion_crud import get_agency_excursion_by_excursion
from datetime import date


def list_excursion_reservation(db: Session, skip: int, limit: int):
    return db.query(ExcursionReservation).offset(skip).limit(limit).all()


def get_excursion_reservation(
    db: Session,
    excursion_id: int,
    tourist_id: int,
    agency_id: int,
    reservation_date: date,
):
    return (
        db.query(ExcursionReservation)
        .filter(
            ExcursionReservation.excursion_id == excursion_id,
            ExcursionReservation.tourist_id == tourist_id,
            ExcursionReservation.reservation_date == reservation_date,
            ExcursionReservation.agency_id == agency_id,
        )
        .first()
    )


def create_excursion_reservation(
    db: Session, excursion_reservation_create: ExcursionReservationSchema
):

    agency_exists = db.query(AgencyModel.id).filter(AgencyModel.id == excursion_reservation_create.agency_id).first()
    if agency_exists is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Agency not found"
        )
    
    excursion = get_excursion(db, excursion_reservation_create.excursion_id)
    if excursion is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Excursion not found"
        )

    extended_excursion = (
        db.query(ExtendedExcursionModel)
        .filter(
            ExtendedExcursionModel.excursion_id
            == excursion_reservation_create.excursion_id
        )
        .first()
    )

    if extended_excursion is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Extended Excursions must be reserved in Package Reservations",
        )

    tourist = get_tourist(db, excursion_reservation_create.tourist_id)
    if tourist is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tourist not found"
        )

    excursion_associated_with_agency = get_agency_excursion_by_excursion(
        db, excursion_reservation_create.excursion_id
    )
    if excursion_associated_with_agency is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can't reserve an excursion not associated with an agency",
        )

    excursion_reservation = get_excursion_reservation(
        db,
        excursion_reservation_create.excursion_id,
        excursion_reservation_create.tourist_id,
        excursion_reservation_create.agency_id,
        excursion_reservation_create.reservation_date,
    )
    if excursion_reservation is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Excursion Reservation already exists",
        )

    if excursion_reservation_create.amount_of_people < 1:
        excursion_reservation_create.amount_of_people = 1

    excursion_reservation = toModel(excursion_reservation_create)
    db.add(excursion_reservation)
    db.commit()
    db.refresh(excursion_reservation)

    return "Success"


def delete_excursion_reservation(
    db: Session, excursion_id: int, tourist_id: int, agency_id: int, reservation_date: date
):

    excursion = get_excursion(db, excursion_id)
    if excursion is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Excursion not found"
        )

    tourist = get_tourist(db, tourist_id)
    if tourist is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tourist not found"
        )
    
    agency_exists = db.query(AgencyModel.id).filter(AgencyModel.id == agency_id).first()
    if agency_exists is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Agency not found"
        )

    excursion_reservation = get_excursion_reservation(
        db, excursion_id, tourist_id, agency_id ,reservation_date
    )
    if excursion_reservation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Excursion Reservation not found",
        )

    db.delete(excursion_reservation)
    db.commit()

    return "Success"


from sqlalchemy import func


def frequent_tourist_by_excursion(db: Session, excursion_id: int):

    excursion = get_excursion(db, excursion_id)
    if excursion is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Excursion not found"
        )

    reserved_excursion = db.query(ExcursionReservation).filter(ExcursionReservation.excursion_id == excursion_id).first()
    if reserved_excursion is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Excursion Reservation not found",
        )

    result = (
        db.query(TouristModel.name, TouristModel.email)
        .join(ExcursionReservation, ExcursionReservation.tourist_id == TouristModel.id)
        .filter(ExcursionReservation.excursion_id == excursion_id)
        .group_by(TouristModel.name, TouristModel.email)
        .having(func.count(ExcursionReservation.excursion_id) > 1)
        .all()
    )

    # Convert the result to a list of dictionaries
    result = [{"name": name, "email": email} for name, email in result]

    return result


def frequent_tourist_by_agency(db: Session, agency_id: int, excursion_id: int):

    excursion = get_excursion(db, excursion_id)
    if excursion is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Excursion not found"
        )

    agency_exists = db.query(AgencyModel.id).filter(AgencyModel.id == agency_id).first()
    if agency_exists is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Agency not found"
        )
    
    
    reserved_excursion = db.query(ExcursionReservation).filter(ExcursionReservation.excursion_id == excursion_id).first()
    if reserved_excursion is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Excursion Reservation not found",
        )
    

    result = (
        db.query(TouristModel.name, TouristModel.email)
        .join(ExcursionReservation, ExcursionReservation.tourist_id == TouristModel.id)
        .filter(ExcursionReservation.excursion_id == excursion_id)
        .filter(ExcursionReservation.agency_id == agency_id)
        .group_by(TouristModel.name, TouristModel.email)
        .having(func.count(ExcursionReservation.excursion_id) > 1)
        .all()
    )

    # Convert the result to a list of dictionaries
    result = [{"name": name, "email": email} for name, email in result]

    return result


def toModel(schema: ExcursionReservationSchema) -> ExcursionReservation:
    return ExcursionReservation(
        excursion_id=schema.excursion_id,
        tourist_id=schema.tourist_id,
        agency_id=schema.agency_id,
        reservation_date=schema.reservation_date,
        amount_of_people=schema.amount_of_people,
        air_line=schema.air_line,
    )


def toShema(model: ExcursionReservation) -> ExcursionReservationSchema:
    return ExcursionReservationSchema(
        excursion_id=model.excursion_id,
        tourist_id=model.tourist_id,
        agency_id=model.agency_id,
        reservation_date=model.reservation_date,
        amount_of_people=model.amount_of_people,
        air_line=model.air_line,
    )
