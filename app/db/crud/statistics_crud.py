from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from models import PackageModel, PackageReservation
from models import AgencyExcursionAssociation, ExcursionReservation, ExcursionModel
from models import AgencyModel
from db.exporter import export_to_excel

def packages_above_average(db: Session, excel: str):
    packages = db.query(PackageModel).all()
    total_price = 0
    for package in packages:
        total_price += package.price
    average_price = total_price / len(packages)
    packages_above_average = []
    for package in packages:
        if package.price > average_price:
            packages_above_average.append(package)
    return export_to_excel(excel, packages_above_average)

def agencies_balance(db: Session, excel: str):
    
    # Get excurision reservations
    excursion_query = db.query(
        AgencyExcursionAssociation.agency_id,
        func.count(ExcursionReservation.tourist_id).label('excursion_count'),
        func.sum(ExcursionReservation.price).label('excursion_price')
    ).join(
        ExcursionModel, ExcursionModel.id == ExcursionReservation.excursion_id
    ).join(
        AgencyExcursionAssociation, AgencyExcursionAssociation.excursion_id == ExcursionModel.id
    ).group_by(
        AgencyExcursionAssociation.agency_id
    )
    
    # Get package reservations
    package_query = db.query(
        PackageReservation.agency_id,
        func.count(PackageReservation.tourist_id).label('package_count'),
        func.sum(PackageReservation.price).label('package_price')
    ).join(
        PackageModel, PackageModel.id == PackageReservation.package_id
    ).group_by(
        PackageReservation.agency_id
    )

    # Final Query
    final_query = db.query(
        AgencyModel.name,
        func.coalesce(excursion_query.subquery().c.excursion_count, 0) + 
        func.coalesce(package_query.subquery().c.package_count, 0),
        func.coalesce(excursion_query.subquery().c.excursion_price, 0) +
        func.coalesce(package_query.subquery().c.package_price, 0)
    ).join(
        excursion_query.subquery(), AgencyModel.id == excursion_query.subquery().c.agency_id, isouter=True
    ).join(
        package_query.subquery(), AgencyModel.id == package_query.subquery().c.agency_id, isouter=True
    )

    return export_to_excel(excel, final_query.all())

# Obtener los nombres y la dirección electrónica de los turistas que han viajado más de una vez a Cuba de manera individual.
def tourists_more_than_one_trip(db: Session, excel: str):
    
    # 

    return export_to_excel(excel, tourists_more_than_one_trip)
