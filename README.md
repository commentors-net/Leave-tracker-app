# 🧭 Team Attendance Tracker (Google Cloud Free Tier, FastAPI + React)

A **Google Cloud–hosted web app** built with **FastAPI (Python)** backend and **React (TypeScript)** frontend.  
It provides secure **login with 2FA (QR-based, e.g. Google Authenticator)** and a **dashboard form** to track team members’ leaves, WFH, or medical absences.

---

## 🚀 Features

- 🔐 **Login with 2FA (Google Authenticator QR)**
- 👥 **People Management** under Settings
- 📅 **Form to log team absences** (with date, type, and reason)
- ⚙️ **Dynamic dropdowns** (Types, People)
- 🧱 **React + TypeScript + Material UI frontend**
- ☁️ **FastAPI + SQLite backend**, deployable on **Google Cloud Run**
- 💰 **Completely Free Tier–Compatible**

---

## 🏗️ System Overview

### Architecture
```
React (Frontend)
   ↓ REST API calls
FastAPI (Backend)
   ↓
SQLite Database
   ↓
Google Cloud Run (Deployment)
```

---

## 📋 Dashboard Form Fields

| Field | Type | Description |
|-------|------|-------------|
| **People** | Dropdown | Select from People list (Settings > People) |
| **Date** | Date Picker | Choose absence date |
| **Duration** | Dropdown | Options: First Half / Second Half / Full |
| **Type** | Dropdown | e.g., Annual, Medical, Medical Dependent, WFH (customizable via Settings > Types) |
| **Reason** | Textbox | Free text reason for absence |

---

## ⚙️ Backend Setup (FastAPI + SQLite)

### 1️⃣ Install dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn sqlalchemy pydantic pyotp qrcode pillow python-jose[cryptography]
```

### 2️⃣ Project structure

```
backend/
│
├── main.py
├── models.py
├── database.py
├── schemas.py
├── auth.py
├── requirements.txt
└── routers/
    ├── users.py
    ├── people.py
    ├── types.py
    └── absences.py
```

---

### 3️⃣ Example `main.py`

```python
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pyotp, qrcode, io, base64

DATABASE_URL = "sqlite:///./database.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False)
Base = declarative_base()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password = Column(String)
    otp_secret = Column(String)

Base.metadata.create_all(bind=engine)

class RegisterRequest(BaseModel):
    username: str
    password: str

class LoginRequest(BaseModel):
    username: str
    token: str

@app.post("/register")
def register(data: RegisterRequest):
    db = SessionLocal()
    secret = pyotp.random_base32()
    user = User(username=data.username, password=data.password, otp_secret=secret)
    db.add(user)
    db.commit()

    otp_uri = pyotp.totp.TOTP(secret).provisioning_uri(name=data.username, issuer_name="TeamTracker")
    qr = qrcode.make(otp_uri)
    buffer = io.BytesIO()
    qr.save(buffer, format="PNG")
    img_b64 = base64.b64encode(buffer.getvalue()).decode()
    return {"qr": img_b64, "secret": secret}

@app.post("/login")
def login(data: LoginRequest):
    db = SessionLocal()
    user = db.query(User).filter(User.username == data.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    totp = pyotp.TOTP(user.otp_secret)
    if totp.verify(data.token):
        return {"success": True}
    raise HTTPException(status_code=401, detail="Invalid token")
```

Run locally:
```bash
uvicorn main:app --reload
```

Then open: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🌐 Frontend Setup (React + TypeScript)

### 4️⃣ Create React App with Vite (TypeScript template)

```bash
npm create vite@latest frontend -- --template react-ts
cd frontend
npm install
npm install @mui/material @emotion/react @emotion/styled axios
```

### 5️⃣ Example Login Page

`src/pages/Login.tsx`

```tsx
import { useState } from "react";
import axios from "axios";
import { TextField, Button, Card, Typography } from "@mui/material";

export default function Login() {
  const [username, setUsername] = useState("");
  const [token, setToken] = useState("");

  const handleLogin = async () => {
    try {
      const res = await axios.post("http://localhost:8000/login", { username, token });
      alert(res.data.success ? "Login success!" : "Invalid 2FA token");
    } catch (err) {
      alert("Login failed");
    }
  };

  return (
    <Card sx={{ p: 4, width: 300, mx: "auto", mt: 10 }}>
      <Typography variant="h6">2FA Login</Typography>
      <TextField label="Username" value={username} onChange={e => setUsername(e.target.value)} fullWidth margin="normal" />
      <TextField label="2FA Token" value={token} onChange={e => setToken(e.target.value)} fullWidth margin="normal" />
      <Button variant="contained" fullWidth onClick={handleLogin}>Login</Button>
    </Card>
  );
}
```

---

## 🧩 6️⃣ Google Cloud Deployment

### Steps:
1. Enable **Cloud Run**, **Cloud Build**, and **Artifact Registry**.
2. Create a `Dockerfile` inside `backend/`:

```dockerfile
FROM python:3.10
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```

3. Build and deploy:
```bash
gcloud builds submit --tag gcr.io/PROJECT-ID/team-tracker
gcloud run deploy team-tracker --image gcr.io/PROJECT-ID/team-tracker --platform managed --allow-unauthenticated
```

4. For frontend, you can host via:
   - Google Cloud Storage (Static Website)
   - Vercel / Netlify (recommended for free)

---

## 🧱 7️⃣ Key Endpoints

| Endpoint | Method | Description |
|-----------|--------|-------------|
| `/register` | POST | Register a user & return QR code for Google Authenticator |
| `/login` | POST | Verify username + 2FA token |
| `/people` | GET/POST | Manage team members |
| `/types` | GET/POST | Manage absence types |
| `/absences` | POST | Submit form data |

---

## 🕒 Estimated Time to Build

| Task | Time |
|------|------|
| Backend setup (FastAPI + DB + 2FA) | 2–3 hrs |
| Frontend setup (React + MUI + routing) | 2 hrs |
| Form UI + API integration | 2 hrs |
| Deployment on Cloud Run & Storage | 1 hr |
| **Total** | **~1 day max** |

---

## ✅ Summary

You’ll get a simple but production-ready **attendance tracker** app where:
- You log in securely via 2FA.
- Submit absences or WFH notices.
- Manage dropdown options dynamically.
- Deploy for **free on Google Cloud Run** + **React hosted frontend**.

---

**Next Step:**  
Would you like me to generate the actual FastAPI + React folder structure with base files as a ready-to-run zip package?
