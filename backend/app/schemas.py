
from pydantic import BaseModel
from datetime import date

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str
    password: str
    token: str

class RegisterResponse(BaseModel):
    qr: str
    secret: str
    username: str
    id: int

class PasswordChange(BaseModel):
    username: str
    old_password: str
    new_password: str

class AbsenceBase(BaseModel):
    date: date
    duration: str
    reason: str
    type_id: int
    person_id: int

class AbsenceCreate(AbsenceBase):
    applied: int = 0

class AbsenceUpdate(BaseModel):
    applied: int

class Absence(AbsenceBase):
    id: int
    applied: int = 0

    class Config:
        from_attributes = True

class PeopleBase(BaseModel):
    name: str

class PeopleCreate(PeopleBase):
    pass

class People(PeopleBase):
    id: int

    class Config:
        from_attributes = True

class TypeBase(BaseModel):
    name: str

class TypeCreate(TypeBase):
    pass

class Type(TypeBase):
    id: int

    class Config:
        from_attributes = True

# Smart Identification Schemas
class SmartIdentificationRequest(BaseModel):
    conversation: str

class ParsedLeaveEntry(BaseModel):
    person_name: str
    date: str
    leave_type: str
    reason: str
    confidence: str

class SmartIdentificationResponse(BaseModel):
    entries: list[ParsedLeaveEntry]
    raw_analysis: str

# AI Instructions Schemas
class AIInstructionsBase(BaseModel):
    instructions: str

class AIInstructionsCreate(AIInstructionsBase):
    pass

class AIInstructionsUpdate(AIInstructionsBase):
    pass

class AIInstructions(AIInstructionsBase):
    id: int
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True
