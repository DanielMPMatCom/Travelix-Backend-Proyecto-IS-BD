from sqlalchemy.orm import Session
from sqlalchemy import func
from models import PackageModel, PackageReservation
from models import AgencyExcursionAssociation, ExcursionReservation, ExcursionModel
from models import AgencyModel

def packages_above_average(db: Session):

    packages_above_average = db.query(PackageModel).\
        filter(PackageModel.price > db.query(func.avg(PackageModel.price)).scalar()).all()
    
    return packages_above_average

def agencies_balance(db: Session):

    excursion_reservation_query = db.query(
        AgencyModel.name,
        func.count(ExcursionModel.id).label('excursion_reservation_count'),
        func.sum(ExcursionModel.price).label('excursion_reservation_total')).\
            join(AgencyExcursionAssociation, AgencyExcursionAssociation.agency_id == AgencyModel.id).\
                join(ExcursionModel, ExcursionModel.id == AgencyExcursionAssociation.excursion_id).\
                    join(ExcursionReservation, ExcursionReservation.excursion_id == ExcursionModel.id).\
                        group_by(AgencyModel.name)

    package_reservation_query = db.query(
        AgencyModel.name,
        func.count(PackageModel.id).label('package_reservation_count'),
        func.sum(PackageModel.price).label('package_reservation_total')).\
            join(PackageModel, PackageModel.agency_id == AgencyModel.id).\
                join(PackageReservation, PackageReservation.package_id == PackageModel.id).\
                    group_by(AgencyModel.name)

    excursion_reservation_subquery = excursion_reservation_query.subquery()
    package_reservation_subquery = package_reservation_query.subquery()

    final_query = db.query(
        AgencyModel.name, 
        func.coalesce(excursion_reservation_subquery.c.excursion_reservation_count, 0) + func.coalesce(package_reservation_subquery.c.package_reservation_count, 0), 
        func.coalesce(excursion_reservation_subquery.c.excursion_reservation_total, 0) + func.coalesce(package_reservation_subquery.c.package_reservation_total, 0)
    ).select_from(AgencyModel).outerjoin(
        excursion_reservation_subquery, 
        AgencyModel.name == excursion_reservation_subquery.c.name
    ).outerjoin(
        package_reservation_subquery, 
        AgencyModel.name == package_reservation_subquery.c.name
    ).all()

    final_result = [
        {
            "name": result[0],
            "reservation_count": result[1],
            "reservation_total": result[2]
        }
        for result in final_query
    ]

    return final_result