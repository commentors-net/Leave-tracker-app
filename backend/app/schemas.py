
from pydantic import BaseModel
from datetime import date

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class AbsenceBase(BaseModel):
    date: date
    duration: str
    reason: str
    type_id: int
    person_id: int

class AbsenceCreate(AbsenceBase):
    pass

class Absence(AbsenceBase):
    id: int

    class Config:
        orm_mode = True

class PeopleBase(BaseModel):
    name: str

class PeopleCreate(PeopleBase):
    pass

class People(PeopleBase):
    id: int

    class Config:
        orm_mode = True

class TypeBase(BaseModel):
    name: str

class TypeCreate(TypeBase):
    pass

class Type(TypeBase):
    id: int

    class Config:
        orm_mode = True
