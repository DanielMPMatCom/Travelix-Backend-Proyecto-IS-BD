from sqlalchemy import Column, Integer, String, Float, Time, ForeignKey, Date, UniqueConstraint, Boolean
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
    disabled = Column(Boolean, nullable=False, default=False)

class AgentModel(UserModel):

    __tablename__ = "agent"

    id = Column(Integer, ForeignKey('user.id'), primary_key=True, nullable=False)
    agency_id = Column(Integer, ForeignKey('agency.id'), nullable=False)

class TouristModel(UserModel):

    __tablename__ = "tourist"

    id = Column(Integer, ForeignKey('user.id'), primary_key=True, nullable=False)
    nationality = Column(String(50), nullable=False)

    excursions = relationship("ExcursionReservation", back_populates="tourists", cascade='all, delete-orphan')
    tourist_types = relationship("TouristTypeTouristAssociation", back_populates="tourists", cascade='all, delete-orphan')
    packages = relationship("PackageReservation", back_populates='tourists', cascade="all, delete-orphan")
class TouristTypeModel(Base):

    __tablename__ = "tourist_type"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(50), nullable=False)

    tourists = relationship("TouristTypeTouristAssociation", back_populates="tourist_types", cascade='all, delete-orphan')

class AgencyModel(Base):

    __tablename__ = "agency"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(50), nullable=False)
    address = Column(String(100), nullable=False)
    fax_number = Column(Integer, nullable=False)
    email = Column(String(100), nullable=False)
    photo_url = Column(String(500))

    excursions = relationship("AgencyExcursionAssociation", back_populates="agencies", cascade="all, delete-orphan")
    offers = relationship("AgencyOfferAssociation", back_populates="agencies", cascade='all, delete-orphan')
    extended_excursions = relationship("PackageModel", back_populates="agency", cascade='all, delete-orphan')
    agents = relationship("AgentModel", cascade='all, delete-orphan')
    
class ExcursionModel(Base):

    __tablename__ = "excursion"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    departure_day = Column(String(50), nullable=False)
    departure_hour = Column(Time, nullable=False)
    departure_place = Column(String(100), nullable=False)
    arrival_day = Column(String(50), nullable=False)
    arrival_hour = Column(Time, nullable=False)
    arrival_place = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    photo_url = Column(String(500))


    agencies = relationship("AgencyExcursionAssociation", back_populates="excursions", cascade="all, delete-orphan")
    tourists = relationship("ExcursionReservation", back_populates="excursions", cascade='all, delete-orphan')

class ExtendedExcursionModel(ExcursionModel):

    __tablename__ = "extended_excursion"

    excursion_id = Column(Integer, ForeignKey('excursion.id'), primary_key=True, nullable=False)

    
    hotels = relationship("HotelExtendedExcursionAssociation", back_populates='extended_excursions', cascade="all, delete-orphan")
    agencies = relationship("PackageModel", back_populates="extended_excursions", cascade='all, delete-orphan')

class OfferModel(Base):

    __tablename__ = "offer"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    price = Column(Float, nullable=False)
    description = Column(String(100), nullable=False)
    hotel_id = Column(Integer, ForeignKey('hotel.id'), nullable=False)

    hotel = relationship("HotelModel", back_populates="offers")
    agencies = relationship("AgencyOfferAssociation", back_populates="offers", cascade='all, delete-orphan')

class HotelModel(Base):

    __tablename__ = "hotel"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(50), nullable=False)
    address = Column(String(100), nullable=False)
    category = Column(Integer, nullable=False)
    photo_url = Column(String(500))


    offers = relationship("OfferModel", back_populates="hotel", cascade="all, delete-orphan")
    extended_excursions = relationship("HotelExtendedExcursionAssociation", back_populates="hotels", cascade="all, delete-orphan")

class FacilityModel(Base):

    __tablename__ = "facility"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    description = Column(String(100), nullable=False)

    packages = relationship("PackageFacilityAssociation", back_populates="facilities", cascade="all, delete-orphan")













class AgencyExcursionAssociation(Base):

    __tablename__ = "agency_excursion_association"

    agency_id = Column(Integer, ForeignKey('agency.id'), primary_key=True, nullable=False)
    excursion_id = Column(Integer, ForeignKey('excursion.id'), primary_key=True, nullable=False)

    agencies = relationship('AgencyModel', back_populates='excursions')
    excursions = relationship('ExcursionModel', back_populates='agencies')


class AgencyOfferAssociation(Base):

    __tablename__ = "agency_offer_association"

    agency_id = Column(Integer, ForeignKey('agency.id'), primary_key=True, nullable=False)
    offer_id = Column(Integer, ForeignKey('offer.id'), primary_key=True, nullable=False)
    price = Column(Float, nullable=False)

    agencies = relationship('AgencyModel', back_populates='offers')
    offers = relationship('OfferModel', back_populates='agencies')


class ExcursionReservation(Base):

    __tablename__ = "excursion_reservation"

    tourist_id = Column(Integer, ForeignKey('tourist.id'), primary_key=True, nullable=False)
    excursion_id = Column(Integer, ForeignKey('excursion.id'), primary_key=True, nullable=False)
    agency_id = Column(Integer, ForeignKey('agency.id'), primary_key=True, nullable=False)
    reservation_date = Column(Date, primary_key=True, nullable=False)
    amount_of_people = Column(Integer, nullable=False)
    air_line = Column(String(50), nullable=False)

    excursions = relationship("ExcursionModel", back_populates='tourists')
    tourists = relationship("TouristModel", back_populates='excursions')

class TouristTypeTouristAssociation(Base):

    __tablename__ = "tourist_type_tourist_association"

    tourist_type_id = Column(Integer, ForeignKey('tourist_type.id'), primary_key=True, nullable=False)
    tourist_id = Column(Integer, ForeignKey('tourist.id'), primary_key=True, nullable=False)

    tourist_types = relationship("TouristTypeModel", back_populates='tourists')
    tourists = relationship("TouristModel", back_populates='tourist_types')





class HotelExtendedExcursionAssociation(Base):

    __tablename__ = "hotel_extended_excursion_association"

    hotel_id = Column(Integer, ForeignKey('hotel.id'), primary_key=True, nullable=False)
    extended_excursion_id = Column(Integer, ForeignKey('extended_excursion.excursion_id'), primary_key=True, nullable=False)
    departure_date = Column(Date, primary_key=True, nullable=False)
    arrival_date = Column(Date, primary_key=True, nullable=False)

    hotels = relationship("HotelModel", back_populates='extended_excursions')
    extended_excursions = relationship("ExtendedExcursionModel", back_populates='hotels')

class PackageModel(Base):

    __tablename__ = "package"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    agency_id = Column(Integer, ForeignKey('agency.id'), nullable=False)
    extended_excursion_id = Column(Integer, ForeignKey('extended_excursion.excursion_id'), nullable=False)
    duration = Column(Integer, nullable=False)
    description = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    photo_url = Column(String(500))

    agency = relationship("AgencyModel", back_populates="extended_excursions")
    extended_excursions = relationship("ExtendedExcursionModel", back_populates="agencies")
    tourists = relationship('PackageReservation', back_populates='packages', cascade="all, delete-orphan")
    facilities = relationship("PackageFacilityAssociation", back_populates="packages", cascade="all, delete-orphan")

class PackageReservation(Base):

    __tablename__ = "package_reservation"

    tourist_id = Column(Integer, ForeignKey('tourist.id'), primary_key=True, nullable=False)
    package_id = Column(Integer, ForeignKey('package.id'), primary_key=True, nullable=False)
    reservation_date = Column(Date, primary_key=True, nullable=False)
    amount_of_people = Column(Integer, nullable=False)
    air_line = Column(String(50), nullable=False)

    packages = relationship("PackageModel", back_populates='tourists')
    tourists = relationship("TouristModel", back_populates='packages')
    
class PackageFacilityAssociation(Base):

    __tablename__ = "package_facility_association"

    package_id = Column(Integer, ForeignKey('package.id'), primary_key=True, nullable=False)
    facility_id = Column(Integer, ForeignKey('facility.id'), primary_key=True, nullable=False)

    packages = relationship('PackageModel', back_populates="facilities")
    facilities = relationship("FacilityModel", back_populates="packages")