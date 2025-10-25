
from fastapi import APIRouter, Depends
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

@router.post("/absences", response_model=schemas.Absence)
def create_absence(absence: schemas.AbsenceCreate, db: Session = Depends(get_db)):
    db_absence = models.Absence(**absence.dict())
    db.add(db_absence)
    db.commit()
    db.refresh(db_absence)
    return db_absence
