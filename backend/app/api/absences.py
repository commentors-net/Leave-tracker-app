
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..models import Absence
from .. import schemas
from ..database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/absences", response_model=list[schemas.Absence])
def read_absences(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    absences = db.query(Absence).offset(skip).limit(limit).all()
    return absences

@router.post("/absences", response_model=schemas.Absence)
def create_absence(absence: schemas.AbsenceCreate, db: Session = Depends(get_db)):
    db_absence = Absence(**absence.dict())
    db.add(db_absence)
    db.commit()
    db.refresh(db_absence)
    return db_absence
