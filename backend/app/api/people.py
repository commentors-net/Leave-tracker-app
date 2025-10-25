
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/people", response_model=list[schemas.People])
def read_people(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    people = db.query(models.People).offset(skip).limit(limit).all()
    return people

@router.post("/people", response_model=schemas.People)
def create_people(people: schemas.PeopleCreate, db: Session = Depends(get_db)):
    db_people = models.People(name=people.name)
    db.add(db_people)
    db.commit()
    db.refresh(db_people)
    return db_people
