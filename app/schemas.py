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
    id: Optional[int] = None
    username: Optional[str] = None
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None

class UserCreateSchema(UserSchema):
    password: str

class AgentSchema(UserSchema):
    agency_id: Optional[int] = None

class AgentCreateSchema(AgentSchema):
    password: str

class TouristSchema(UserSchema):
    nationality: Optional[str] = None

class TouristCreateSchema(TouristSchema):
    password: str
    
class TouristTypeSchema(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None

class AgencySchema(BaseModel):
    id : Optional[int] = None
    name: Optional[str] = None
    address: Optional[str] = None
    fax_number: Optional[int] = None
    email: Optional[str] = None
    photo_url: Optional[str] = None

class ExcursionSchema(BaseModel):
    id: Optional[int] = None
    departure_day: Optional[str] = None
    departure_hour: Optional[time] = None
    departure_place: Optional[str] = None
    arrival_day: Optional[str] = None
    arrival_hour: Optional[time] = None
    arrival_place: Optional[str] = None
    price: Optional[float] = None
    photo_url: Optional[str] = None

class ExtendedExcursionSchema(ExcursionSchema):
    pass
    # excursion_id: Optional[int]

class OfferSchema(BaseModel):
    id: Optional[int] = None
    price: Optional[float] = None
    description: Optional[str] = None
    hotel_id: Optional[int] = None

class HotelSchema(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    address: Optional[str] = None
    category: Optional[int] = None
    photo_url: Optional[str] = None

class FacilitySchema(BaseModel):
    id: Optional[int] = None
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
    amount_of_people: Optional[int] = None
    air_line: Optional[str] = None
    
class TouristTypeTouristAssociationSchema(BaseModel):
    tourist_id: Optional[int]
    tourist_type_id: Optional[int]

class PackageSchema(BaseModel):
    id: Optional[int] = None
    price: Optional[float] = None
    description: Optional[str] = None
    duration: Optional[int] = None
    agency_id: Optional[int] = None
    extended_excursion_id: Optional[int] = None
    photo_url: Optional[str] = None

class HotelExtendedExcursionAssociationSchema(BaseModel):
    hotel_id: Optional[int]
    extended_excursion_id: Optional[int]
    departure_date: Optional[date] = None
    arrival_date: Optional[date] = None
class PackageFacilityAssociationSchema(BaseModel):
    package_id: Optional[int]
    facility_id: Optional[int]

class PackageReservationSchema(BaseModel):
    tourist_id: Optional[int]
    package_id: Optional[int]
    reservation_date: Optional[date] = None
    amount_of_people: Optional[int] = None
    air_line: Optional[str] = None

class TimeInHotel(BaseModel):
    hotel_id: int
    arrival_date: date
    departure_date: date
