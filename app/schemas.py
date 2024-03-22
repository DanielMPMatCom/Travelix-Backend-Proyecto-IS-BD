from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import time, date

class Token(BaseModel):
    access_token: str
    token_type: str
    role: str

class TokenData(BaseModel):
    username: Optional[str] = None
class UserSchema(BaseModel):
    disabled: Optional[bool] = None
    id: Optional[int]
    username: Optional[str] = None
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None

class TouristSchema(UserSchema):
    nationality: Optional[str] = None

class TouristCreateSchema(TouristSchema):
    password: str
    
class TouristTypeSchema(BaseModel):
    id: Optional[int]
    name: Optional[str] = None

class AgencySchema(BaseModel):
    id : Optional[int]
    name: Optional[str] = None
    address: Optional[str] = None
    fax_number: Optional[int] = None
    email: Optional[str] = None
    photo_url: Optional[str]

class ExcursionSchema(BaseModel):
    id: Optional[int]
    departure_day: Optional[str] = None
    departure_hour: Optional[time] = None
    departure_place: Optional[str] = None
    arrival_day: Optional[str] = None
    arrival_hour: Optional[time] = None
    arrival_place: Optional[str] = None
    price: Optional[float] = None
    photo_url: Optional[str]

class ExtendedExcursionSchema(ExcursionSchema):
    pass
    # excursion_id: Optional[int]

class OfferSchema(BaseModel):
    id: Optional[int]
    price: Optional[float] = None
    description: Optional[str] = None
    hotel_id: Optional[int] = None

class HotelSchema(BaseModel):
    id: Optional[int]
    name: Optional[str] = None
    address: Optional[str] = None
    category: Optional[int] = None
    photo_url: Optional[str]

class FacilitySchema(BaseModel):
    id: Optional[int]
    description: Optional[str] = None

class AgencyOfferAssociationSchema(BaseModel):
    agency_id: Optional[int]
    offer_id: Optional[int]
    price: Optional[float] = None

class AgencyExcursionAssociationSchema(BaseModel):
    agency_id: Optional[int]
    excursion_id: Optional[int]

class ExcursionReservationSchema(BaseModel):
    tourist_id: Optional[int]
    excursion_id: Optional[int]
    reservation_date: Optional[date] = None
    
class TouristTypeTouristAssociationSchema(BaseModel):
    tourist_id: Optional[int]
    tourist_type_id: Optional[int]

class PackageSchema(BaseModel):
    id: Optional[int]
    price: Optional[float] = None
    description: Optional[str] = None
    duration: Optional[int] = None
    agency_id: Optional[int] = None
    extended_excursion_id: Optional[int] = None
    photo_url: Optional[str]

class HotelExtendedExcursionAssociationSchema(BaseModel):
    hotel_id: Optional[int]
    extended_excursion_id: Optional[int]
    departure_date: Optional[date] = None
    arrival_date: Optional[date] = None
class PackageFacilityAssociationSchema(BaseModel):
    package_id: Optional[int]
    facility_id: Optional[int]
    agency_id: Optional[int]
    extended_excursion_id: Optional[int]

class PackageReservationSchema(BaseModel):
    tourist_id: Optional[int]
    package_id: Optional[int]
    agency_id: Optional[int]
    extended_excursion_id: Optional[int]
    reservation_date: Optional[date] = None