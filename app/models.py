from sqlalchemy import Column, Integer, String, Float, Time, ForeignKey, Date, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from db.config import Base



class UserModel(Base):

    __tablename__ = "user"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    name = Column(String(50), nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(100), nullable=False)
    role = Column(String(20), nullable=False)
    password = Column(String(100), nullable=False)

class TouristModel(UserModel):

    __tablename__ = "tourist"

    id = Column(Integer, ForeignKey('user.id'), primary_key=True, nullable=False)
    nationality = Column(String(50), nullable=False)
class TouristTypeModel(Base):

    __tablename__ = "tourist_type"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(50), nullable=False)

class AgencyModel(Base):

    __tablename__ = "agency"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(50), nullable=False)
    address = Column(String(100), nullable=False)
    fax_number = Column(Integer, nullable=False)
    email = Column(String(100), nullable=False)

    excursions = relationship("ExcursionModel", secondary="agency_excursion_association", back_populates="agencies")
    
class ExcursionModel(Base):

    __tablename__ = "excursion"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    departure_day = Column(String(20), nullable=False)
    departure_hour = Column(Time, nullable=False)
    departure_place = Column(String(100), nullable=False)
    arrival_day = Column(String(20), nullable=False)
    arrival_hour = Column(Time, nullable=False)
    arrival_place = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)

    agencies = relationship("AgencyModel", secondary="agency_excursion_association", back_populates="excursions")

class ExtendedExcursionModel(ExcursionModel):

    __tablename__ = "extended_excursion"

    excursion_id = Column(Integer, ForeignKey('excursion.id'), primary_key=True, nullable=False)

class OfferModel(Base):

    __tablename__ = "offer"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    price = Column(Float, nullable=False)
    description = Column(String(100), nullable=False)

    hotel_id = Column(Integer, ForeignKey('hotel.id'), nullable=False)
    hotel = relationship("HotelModel", back_populates="offers")

class HotelModel(Base):

    __tablename__ = "hotel"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(50), nullable=False)
    address = Column(String(100), nullable=False)
    category = Column(Integer, nullable=False)

    offers = relationship("OfferModel", back_populates="hotel")

class FacilityModel(Base):

    __tablename__ = "facility"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    description = Column(String(100), nullable=False)

class AgencyExcursionAssociation(Base):

    __tablename__ = "agency_excursion_association"

    agency_id = Column(Integer, ForeignKey('agency.id'), primary_key=True, nullable=False)
    excursion_id = Column(Integer, ForeignKey('excursion.id'), primary_key=True, nullable=False)

class AgencyOfferAssociation(Base):

    __tablename__ = "agency_offer_association"

    agency_id = Column(Integer, ForeignKey('agency.id'), primary_key=True, nullable=False)
    offer_id = Column(Integer, ForeignKey('offer.id'), primary_key=True, nullable=False)
    price = Column(Float, nullable=False)

class ExcursionReservation(Base):

    __tablename__ = "excursion_reservation"

    tourist_id = Column(Integer, ForeignKey('tourist.id'), primary_key=True, nullable=False)
    excursion_id = Column(Integer, ForeignKey('excursion.id'), primary_key=True, nullable=False)
    reservation_date = Column(Date, primary_key=True, nullable=False)

class TouristTypeTouristAssociation(Base):

    __tablename__ = "tourist_type_tourist_association"

    tourist_type_id = Column(Integer, ForeignKey('tourist_type.id'), primary_key=True, nullable=False)
    tourist_id = Column(Integer, ForeignKey('tourist.id'), primary_key=True, nullable=False)


class PackageModel(Base):

    __tablename__ = "package"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    agency_id = Column(Integer, ForeignKey('agency.id'), primary_key=True, nullable=False, unique=True)
    extended_excursion_id = Column(Integer, ForeignKey('extended_excursion.excursion_id'), primary_key=True, nullable=False, unique=True)
    duration = Column(Integer, nullable=False)
    description = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)

    __table_args__ = (
        UniqueConstraint('id', 'agency_id', 'extended_excursion_id'),
    )
    # Establecer relación inversa
    # facility_associations = relationship('PackageFacilityAssociation', foreign_keys=[PackageFacilityAssociation.package_id, PackageFacilityAssociation.agency_id, PackageFacilityAssociation.extended_excursion_id])


# class PackageReservation(Base):

#     __tablename__ = "package_reservation"

#     tourist_id = Column(Integer, ForeignKey('tourist.id'), primary_key=True, nullable=False)
#     package_id = Column(Integer, ForeignKey('package.id'), primary_key=True, nullable=False)
#     agency_id = Column(Integer, ForeignKey('agency.id'), primary_key=True, nullable=False)
#     extended_excursion_id = Column(Integer, ForeignKey('extended_excursion.id'), primary_key=True, nullable=False)
#     reservation_date = Column(Date, primary_key=True, nullable=False)

class HotelExtendedExcursionAssociation(Base):

    __tablename__ = "hotel_extended_excursion_association"

    hotel_id = Column(Integer, ForeignKey('hotel.id'), primary_key=True, nullable=False)
    extended_excursion_id = Column(Integer, ForeignKey('extended_excursion.excursion_id'), primary_key=True, nullable=False)
    departure_date = Column(Date, primary_key=True, nullable=False)
    arrival_date = Column(Date, primary_key=True, nullable=False)
    
# class PackageFacilityAssociation(Base):

#     __tablename__ = "package_facility_association"

#     package_id = Column(Integer, ForeignKey('package.id'), primary_key=True, nullable=False, unique=True)
#     agency_id = Column(Integer, ForeignKey('package.agency_id'), primary_key=True, nullable=False, unique=True)
#     extended_excursion_id = Column(Integer, ForeignKey('package.extended_excursion_id'), primary_key=True, nullable=False, unique=True)
#     facility_id = Column(Integer, ForeignKey('facility.id'), primary_key=True, nullable=False)

#     package = relationship('PackageModel', foreign_keys=[package_id, agency_id, extended_excursion_id])