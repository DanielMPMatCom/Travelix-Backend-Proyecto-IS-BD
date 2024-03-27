from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from models import PackageModel, PackageReservation
from models import AgencyExcursionAssociation, ExcursionReservation, ExcursionModel
from models import AgencyModel
from db.exporter import export_to_excel, export_to_excel2

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

    agencies = db.query(AgencyModel).all()
    excursions = db.query(ExcursionModel).all()
    packages = db.query(PackageModel).all()
    reserved_excursions = db.query(ExcursionReservation).all()
    reserved_packages = db.query(PackageReservation).all()
    agency_excursions = db.query(AgencyExcursionAssociation).all()
    agency_balance = []

    for agency in agencies:
        total_price = 0
        reservation_count = 0
        for excursion in excursions:
            for reservation in reserved_excursions:
                if reservation.excursion_id == excursion.id:
                    for association in agency_excursions:
                        if association.agency_id == agency.id and association.excursion_id == excursion.id:
                            total_price += excursion.price
                            reservation_count+=1
        for package in packages:
            for reservation in reserved_packages:
                if reservation.package_id == package.id:
                    if package.agency_id == agency.id:
                        total_price += package.price
                        reservation_count+=1
        if reservation_count:
            agency_balance.append({
                'agency_name': agency.name,
                'total_price': total_price,
                'reservation_count': reservation_count
            })
    

    # Llamar a la función export_to_excel con los resultados convertidos
    return export_to_excel2(excel, agency_balance)

























    # # Get excurision reservations
    # excursion_query = db.query(
    #     AgencyExcursionAssociation.agency_id,
    #     func.count(ExcursionReservation.tourist_id).label('excursion_count'),
    #     func.sum(ExcursionModel.price).label('excursion_price')
    # ).join(
    #     ExcursionModel, ExcursionModel.id == ExcursionReservation.excursion_id
    # ).join(
    #     AgencyExcursionAssociation, AgencyExcursionAssociation.excursion_id == ExcursionModel.id
    # ).group_by(
    #     AgencyExcursionAssociation.agency_id
    # )
    
    # # Get package reservations
    # package_query = db.query(
    #     AgencyModel.id.label('agency_id'),
    #     func.count(PackageReservation.tourist_id).label('package_count'),
    #     func.sum(PackageModel.price).label('package_price')
    # ).join(
    #     AgencyModel, AgencyModel.id == PackageModel.agency_id
    # ).join(
    #     PackageModel, PackageModel.id == PackageReservation.package_id
    # ).group_by(
    #     AgencyModel.id
    # )

    # # Final Query
    # final_query = db.query(
    #     AgencyModel.name,
    #     func.coalesce(excursion_query.subquery().c.excursion_count, 0) + 
    #     func.coalesce(package_query.subquery().c.package_count, 0),
    #     func.coalesce(excursion_query.subquery().c.excursion_price, 0) +
    #     func.coalesce(package_query.subquery().c.package_price, 0)
    # ).join(
    #     excursion_query.subquery(), AgencyModel.id == excursion_query.subquery().c.agency_id, isouter=True
    # ).join(
    #     package_query.subquery(), AgencyModel.id == package_query.subquery().c.agency_id, isouter=True
    # )


    # # Consulta para las reservas de excursiones
    # excursion_query = db.query(
    #     AgencyModel.name.label('agency_name'),
    #     func.count(ExcursionReservation.tourist_id).label('excursion_count'),
    #     func.sum(ExcursionModel.price).label('excursion_total')
    # ).join(
    #     AgencyExcursionAssociation, AgencyExcursionAssociation.excursion_id == ExcursionReservation.excursion_id
    # ).join(
    #     AgencyModel, AgencyModel.id == AgencyExcursionAssociation.agency_id
    # ).join(
    #     ExcursionModel, ExcursionModel.id == AgencyExcursionAssociation.excursion_id
    # ).group_by(
    #     AgencyModel.name
    # )

    # # Consulta para las reservas de paquetes
    # package_query = db.query(
    #     AgencyModel.name.label('agency_name'),
    #     func.count(PackageReservation.package_id).label('package_count'),
    #     func.sum(PackageModel.price).label('package_total')
    # ).join(
    #     PackageModel, PackageModel.id == PackageReservation.package_id
    # ).join(
    #     AgencyModel, AgencyModel.id == PackageModel.agency_id
    # ).group_by(
    #     AgencyModel.name
    # )

    # # Convertir las consultas en subconsultas
    # excursion_subquery = excursion_query.subquery()
    # package_subquery = package_query.subquery()

    # # Crear la consulta final utilizando las subconsultas
    # final_query = db.query(
    #     excursion_subquery.c.agency_name,
    #     (excursion_subquery.c.excursion_count + package_subquery.c.package_count).label('reservation_count'),
    #     (excursion_subquery.c.excursion_total + package_subquery.c.package_total).label('total_amount')
    # ).outerjoin(
    #     package_subquery, package_subquery.c.agency_name == excursion_subquery.c.agency_name
    # )
    # results = final_query.all()
    # results_as_dicts = [
    #     {'agency_name': row[0], 'reservation_count': row[1], 'total_amount': row[2]}
    #     for row in results
    # ]
