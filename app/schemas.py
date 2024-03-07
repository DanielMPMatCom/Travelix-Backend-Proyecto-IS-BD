from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import time


class AgencySchema(BaseModel):
    id : Optional[int] = None
    name: Optional[str] = None
    address: Optional[str] = None
    fax_number: Optional[int] = None
    email: Optional[str] = None

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

class TouristSchema(UserSchema):
    nationality: Optional[str] = None

class TouristCreateSchema(TouristSchema):
    password: str
    