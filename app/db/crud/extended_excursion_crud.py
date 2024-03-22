from fastapi import HTTPException, status
from sqlalchemy import delete
from sqlalchemy.orm import Session
from models import ExcursionModel, ExcursionReservation, AgencyExcursionAssociation, ExtendedExcursionModel, HotelExtendedExcursionAssociation, PackageModel
from schemas import ExtendedExcursionSchema


def list_extended_excursion(db: Session, skip: int, limit: int):
    return db.query(ExtendedExcursionModel).offset(skip).limit(limit).all()

def get_extended_excursion(db: Session, id: int):
    return db.query(ExtendedExcursionModel).filter(ExtendedExcursionModel.id == id).first()

def create_extended_excursion(db: Session, extended_excursion_create: ExtendedExcursionSchema):

    extended_excursion = toModel(extended_excursion_create)
    db.add(extended_excursion)
    db.commit()
    db.refresh(extended_excursion)

    return "Success"


def delete_extended_excursion(db: Session, extended_excursion_delete: ExtendedExcursionSchema):

    extended_excursion = get_extended_excursion(db, extended_excursion_delete.id)

    if extended_excursion is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Extended Excursion not found")
    
    # db.execute(delete(AgencyExcursionAssociation).where(AgencyExcursionAssociation.excursion_id == extended_excursion_delete.id))
    # db.execute(delete(ExcursionReservation).where(ExcursionReservation.excursion_id == extended_excursion_delete.id))
    # db.execute(delete(HotelExtendedExcursionAssociation).where(HotelExtendedExcursionAssociation.extended_excursion_id == extended_excursion_delete.id))
    # db.execute(delete(PackageModel).where(PackageModel.extended_excursion_id == extended_excursion_delete.id))
    # db.execute(delete(ExtendedExcursionModel).where(ExtendedExcursionModel.excursion_id == extended_excursion_delete.id))
    db.commit()

    db.delete(extended_excursion)
    db.commit()

    return "Success"

def toModel(schema:ExtendedExcursionSchema) -> ExtendedExcursionModel:
    return ExtendedExcursionModel(
        # excursion_id=schema.excursion_id, 
                            departure_day=schema.departure_day, 
                          departure_hour=schema.departure_hour, 
                          departure_place=schema.departure_place, 
                          arrival_day=schema.arrival_day,
                          arrival_hour=schema.arrival_hour,
                          arrival_place=schema.arrival_place,
                          price=schema.price
        )

def toShema(model:ExtendedExcursionModel) -> ExtendedExcursionSchema:
    return ExtendedExcursionSchema(excursion_id=model.excursion_id,
                                   departure_day=model.departure_day, 
                                    departure_hour=model.departure_hour, 
                                    departure_place=model.departure_place, 
                                    arrival_day=model.arrival_day,
                                    arrival_hour=model.arrival_hour,
                                    arrival_place=model.arrival_place,
                                    price=model.price)
