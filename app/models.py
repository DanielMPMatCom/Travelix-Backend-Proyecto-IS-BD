from sqlalchemy import Column, Integer, String, Float, Time, ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from db.config import Base


class AgencyModel(Base):

    __tablename__ = "agency"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(50), nullable=False)
    address = Column(String(100), nullable=False)
    fax_number = Column(Integer, nullable=False)
    email = Column(String(100), nullable=False)

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
    