from sqlalchemy.orm import Session
from db.config import get_db

import schemas as s
import models as m


def populate_tables():
    db = get_db()
    # Populate Tourists
    tourist1 = m.TouristModel(
        username="tourist1",
        name="Tourist 1",
        phone="123456789",
        email="random@mail.com"
    )
    db.add(tourist1)
    tourist2 = m.TouristModel(
        username="tourist2",
        name="Tourist 2",
        phone="123456789",
        email="random@mail.com"
    )
    db.add(tourist2)
    tourist3 = m.TouristModel(
        username="tourist3",
        name="Tourist 3",
        phone="123456789",
        email="random@mail.com"
    )
    db.add(tourist3)
    tourist4 = m.TouristModel(
        username="tourist4",
        name="Tourist 4",
        phone="123456789",
        email="random@mail.com"
    )
    db.add(tourist4)
    tourist5 = m.TouristModel(
        username="tourist5",
        name="Tourist 5",
        phone="123456789",
        email="random@mail.com"
    )
    db.add(tourist5)
    agency1 = m.AgencyModel(
        name="Agency 1",
        address="Random address",
        fax_number=123456789,
        email="random@mail.com",
        photo_url="random_url"
    )
    db.add(agency1)
    agency2 = m.AgencyModel(
        name="Agency 2",
        address="Random address",
        fax_number=123456789,
        email="random@mail.com",
        photo_url="random_url"
    )
    db.add(agency2)
    agency3 = m.AgencyModel(
        name="Agency 3",
        address="Random address",
        fax_number=123456789,
        email="random@mail.com",
        photo_url="random_url"
    )
    db.add(agency3)
    agency4 = m.AgencyModel(
        name="Agency 4",
        address="Random address",
        fax_number=123456789,
        email="random@mail.com",
        photo_url="random_url"
    )
    db.add(agency4)
    hotel1 = m.HotelModel(
        name="Hotel 1",
        address="Random address",
        category=1,
        photo_url="random_url"
    )
    db.add(hotel1)
    hotel2 = m.HotelModel(
        name="Hotel 2",
        address="Random address",
        category=2,
        photo_url="random_url"
    )
    db.add(hotel2)
    hotel3 = m.HotelModel(
        name="Hotel 3",
        address="Random address",
        category=3,
        photo_url="random_url"
    )
    db.add(hotel3)
    hotel4 = m.HotelModel(
        name="Hotel 4",
        address="Random address",
        category=4,
        photo_url="random_url"
    )
    db.add(hotel4)
    # Populate Excursions
    excursion1 = m.ExcursionModel(
        departure_day="Monday",
        departure_hour="12:00:00",
        departure_place="Random place",
        arrival_day="Monday",
        arrival_hour="12:00:00",
        arrival_place="Random place",
        price=100,
        photo_url="random_url"
    )
    db.add(excursion1)
    excursion2 = m.ExcursionModel(
        departure_day="Monday",
        departure_hour="12:00:00",
        departure_place="Random place",
        arrival_day="Monday",
        arrival_hour="12:00:00",
        arrival_place="Random place",
        price=200,
        photo_url="random_url"
    )
    db.add(excursion2)
    excursion3 = m.ExcursionModel(
        departure_day="Monday",
        departure_hour="12:00:00",
        departure_place="Random place",
        arrival_day="Monday",
        arrival_hour="12:00:00",
        arrival_place="Random place",
        price=300,
        photo_url="random_url"
    )
    db.add(excursion3)
    excursion4 = m.ExcursionModel(
        departure_day="Monday",
        departure_hour="12:00:00",
        departure_place="Random place",
        arrival_day="Monday",
        arrival_hour="12:00:00",
        arrival_place="Random place",
        price=400,
        photo_url="random_url"
    )
    db.add(excursion4)
    # Populate Packages
    package1 = m.PackageModel(
        price=100,
        description="Random description",
        duration=1,
        agency_id=1,
        extended_excursion_id=1,
        photo_url="random_url"
    )
    db.add(package1)
    package2 = m.PackageModel(
        price=200,
        description="Random description",
        duration=2,
        agency_id=2,
        extended_excursion_id=2,
        photo_url="random_url"
    )
    db.add(package2)
    package3 = m.PackageModel(
        price=300,
        description="Random description",
        duration=3,
        agency_id=3,
        extended_excursion_id=3,
        photo_url="random_url"
    )
    db.add(package3)
    package4 = m.PackageModel(
        price=400,
        description="Random description",
        duration=4,
        agency_id=4,
        extended_excursion_id=4,
        photo_url="random_url"
    )
    db.add(package4)
    # Populate Offers
    offer1 = m.OfferModel(
        price=100,
        description="Random description",
        hotel_id=1
    )
    db.add(offer1)
    offer2 = m.OfferModel(
        price=200,
        description="Random description",
        hotel_id=2
    )
    db.add(offer2)
    offer3 = m.OfferModel(
        price=300,
        description="Random description",
        hotel_id=3
    )
    db.add(offer3)
    offer4 = m.OfferModel(
        price=400,
        description="Random description",
        hotel_id=4
    )
    db.add(offer4)
    # Populate Excursion Reservation
    excursion_reservation1 = m.ExcursionReservation(
        tourist_id=1,
        excursion_id=1,
        reservation_date="2021-01-01"
    )
    db.add(excursion_reservation1)
    excursion_reservation2 = m.ExcursionReservation(
        tourist_id=2,
        excursion_id=2,
        reservation_date="2021-01-01"
    )
    db.add(excursion_reservation2)
    excursion_reservation3 = m.ExcursionReservation(
        tourist_id=3,
        excursion_id=3,
        reservation_date="2021-01-01"
    )
    db.add(excursion_reservation3)
    excursion_reservation4 = m.ExcursionReservation(
        tourist_id=4,
        excursion_id=4,
        reservation_date="2021-01-01"
    )
    db.add(excursion_reservation4)
    # Populate Agency Offer Association
    agency_offer_association1 = m.AgencyOfferAssociation(
        agency_id=1,
        offer_id=1,
        price=100
    )
    db.add(agency_offer_association1)
    agency_offer_association2 = m.AgencyOfferAssociation(
        agency_id=2,
        offer_id=2,
        price=200
    )
    db.add(agency_offer_association2)
    agency_offer_association3 = m.AgencyOfferAssociation(
        agency_id=3,
        offer_id=3,
        price=300
    )
    db.add(agency_offer_association3)
    agency_offer_association4 = m.AgencyOfferAssociation(
        agency_id=4,
        offer_id=4,
        price=400
    )
    db.add(agency_offer_association4)
    # Populate Agency Excursion Association
    agency_excursion_association1 = m.AgencyExcursionAssociation(
        agency_id=1,
        excursion_id=1
    )
    db.add(agency_excursion_association1)
    agency_excursion_association2 = m.AgencyExcursionAssociation(
        agency_id=2,
        excursion_id=2
    )
    db.add(agency_excursion_association2)
    agency_excursion_association3 = m.AgencyExcursionAssociation(
        agency_id=3,
        excursion_id=3
    )
    db.add(agency_excursion_association3)
    agency_excursion_association4 = m.AgencyExcursionAssociation(
        agency_id=4,
        excursion_id=4
    )
    db.add(agency_excursion_association4)
    # Populate Package Reservation
    package_reservation1 = m.PackageReservation(
        tourist_id=1,
        package_id=1,
        agency_id=1,
        reservation_date="2021-01-01"
    )
    db.add(package_reservation1)
    package_reservation2 = m.PackageReservation(
        tourist_id=2,
        package_id=2,
        agency_id=2,
        reservation_date="2021-01-01"
    )
    db.add(package_reservation2)
    package_reservation3 = m.PackageReservation(
        tourist_id=3,
        package_id=3,
        agency_id=3,
        reservation_date="2021-01-01"
    )
    db.add(package_reservation3)
    package_reservation4 = m.PackageReservation(
        tourist_id=4,
        package_id=4,
        agency_id=4,
        reservation_date="2021-01-01"
    )
    db.add(package_reservation4)
    db.commit()

if __name__ == "__main__":
    populate_tables()