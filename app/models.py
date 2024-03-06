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
