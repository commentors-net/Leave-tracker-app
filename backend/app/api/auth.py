from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import pyotp, qrcode, io, base64
from ..models import User
from .. import schemas
from ..database import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=schemas.User)
def register(data: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == data.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    secret = pyotp.random_base32()
    user = User(username=data.username, password=data.password, otp_secret=secret)
    db.add(user)
    db.commit()
    db.refresh(user)

    otp_uri = pyotp.totp.TOTP(secret).provisioning_uri(name=data.username, issuer_name="TeamTracker")
    qr = qrcode.make(otp_uri)
    buffer = io.BytesIO()
    qr.save(buffer, format="PNG")
    img_b64 = base64.b64encode(buffer.getvalue()).decode()
    return {"qr": img_b64, "secret": secret, "user": user}

@router.post("/login")
def login(data: schemas.TokenData, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    totp = pyotp.TOTP(user.otp_secret)
    if totp.verify(data.token):
        return {"success": True}
    raise HTTPException(status_code=401, detail="Invalid token")