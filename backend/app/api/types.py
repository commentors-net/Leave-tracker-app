
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models import Type
from .. import schemas
from ..database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/types", response_model=list[schemas.Type])
def read_types(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    types = db.query(Type).offset(skip).limit(limit).all()
    return types

@router.post("/types", response_model=schemas.Type)
def create_type(type: schemas.TypeCreate, db: Session = Depends(get_db)):
    db_type = Type(name=type.name)
    db.add(db_type)
    db.commit()
    db.refresh(db_type)
    return db_type
