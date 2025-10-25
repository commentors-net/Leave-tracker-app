
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    otp_secret = Column(String)

class Absence(Base):
    __tablename__ = "absences"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    duration = Column(String)
    reason = Column(String)
    type_id = Column(Integer, ForeignKey("types.id"))
    person_id = Column(Integer, ForeignKey("people.id"))

    type = relationship("Type", back_populates="absences")
    person = relationship("People", back_populates="absences")

class People(Base):
    __tablename__ = "people"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    absences = relationship("Absence", back_populates="person")

class Type(Base):
    __tablename__ = "types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    absences = relationship("Absence", back_populates="type")
