# Leave Tracker - Complete Developer Guide

**Version 1.2.0** | Last Updated: November 3, 2025

A comprehensive guide for developers to understand, develop, and deploy the Leave Tracker application.

---

##  Table of Contents

1. [Project Overview](#1-project-overview)
2. [Quick Start](#2-quick-start)
3. [Architecture](#3-architecture)
4. [Database Abstraction Layer](#4-database-abstraction-layer)
5. [Local Development Setup](#5-local-development-setup)
6. [Technology Stack](#6-technology-stack)
7. [Feature Documentation](#7-feature-documentation)
8. [Security Implementation](#8-security-implementation)
9. [API Reference](#9-api-reference)
10. [Google Cloud Deployment](#10-google-cloud-deployment)
11. [Troubleshooting](#11-troubleshooting)
12. [Maintenance](#12-maintenance)

---

## 1. Project Overview

Leave Tracker is a production-ready web application for managing team absences with:
- **Secure Authentication** (JWT + 2FA)
- **Database Abstraction** (SQLite for dev, Firestore for prod)
- **AI-Powered Parsing** (Google Gemini API)
- **Cloud Deployment** (Google Cloud Run + Storage)
- **Modern Stack** (FastAPI + React + TypeScript)

**Key Features:**
- JWT authentication with 30-minute expiration
- 2FA using Google Authenticator (TOTP)
- People and leave types management
- Absence logging and reporting
- Smart Identification - AI parses chat conversations to extract leave requests
- Registration control (enable/disable)
- Automatic environment switching (dev/prod databases)

---

## 2. Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Git

### Local Development (2 minutes)

```powershell
# Clone and setup backend
git clone https://github.com/commentors-net/Leave-tracker-app.git
cd Leave-tracker-app/backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt

# Create .env file
@"
ENVIRONMENT=development
SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
GEMINI_API_KEY=your_gemini_api_key
"@ | Out-File .env -Encoding utf8

# Run backend (or press F5 in VS Code)
uvicorn app.main:app --reload

# Setup frontend (new terminal)
cd ../frontend
npm install
npm run dev

# Access at http://localhost:5173
```

### Deploy to Cloud (FREE)

```powershell
.\deploy-backend-update.ps1
```

---

## 3. Architecture

### System Diagram

```
Frontend (React)  Backend (FastAPI)  Database
                                         SQLite (dev)
                                         Firestore (prod)
```

### Database Abstraction

The app uses `db_factory.py` to automatically select the right database:
- `ENVIRONMENT=development`  SQLite (local file)
- `ENVIRONMENT=production`  Firestore (Google Cloud)

All API endpoints use the same interface regardless of database.

---

## 4. Database Abstraction Layer

### How It Works

**db_factory.py** - Returns appropriate database instance
**sqlite_db.py** - SQLite implementation  
**firestore_db.py** - Firestore implementation

```python
# db_factory.py
def get_database():
    environment = os.getenv("ENVIRONMENT", "production")
    if environment == "development":
        return SQLiteDatabase()
    else:
        return FirestoreDatabase()

db = get_database()
```

### Usage in API Endpoints

```python
from ..db_factory import db

@router.get("/people")
async def get_people(current_user: str = Depends(get_current_user)):
    return db.get_all_people()
```

### Common Interface

Both databases provide identical methods:
- `create_user()`, `get_user_by_username()`, `get_user_by_id()`
- `create_person()`, `get_all_people()`, `update_person()`, `delete_person()`
- `create_type()`, `get_all_types()`, `update_type()`, `delete_type()`
- `create_absence()`, `get_all_absences()`, `update_absence()`, `delete_absence()`
- `create_or_update_ai_instructions()`, `get_ai_instructions()`

### Data Migration

```powershell
# Export Firestore to JSON
python backend/setup_local_data.py  # Choose option 1

# Import to SQLite
python backend/import_to_sqlite.py

# Import to Firestore
python backend/import_to_firestore.py
```

---

## 5. Local Development Setup

### Backend Setup

```powershell
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

Create `.env`:
```
ENVIRONMENT=development
SECRET_KEY=your-32-byte-hex-key
GEMINI_API_KEY=your-gemini-key
```

Run:
```powershell
uvicorn app.main:app --reload
# Or press F5 in VS Code
```

### Frontend Setup

```powershell
cd frontend
npm install
```

Create `.env.development`:
```
VITE_API_URL=http://localhost:8000
VITE_ENABLE_REGISTRATION=true
```

Run:
```powershell
npm run dev
```

### First Time Use

1. Register at http://localhost:5173/register
2. Scan QR code with Google Authenticator
3. Login with username + password + 2FA token
4. Add people and leave types in Settings
5. Test Smart Identification (needs Gemini API key)

---

## 6. Technology Stack

**Backend:**
- FastAPI - Web framework
- SQLite - Development database
- Firestore - Production database
- JWT + TOTP - Authentication
- Google Gemini - AI parsing
- Docker - Containerization

**Frontend:**
- React 19 - UI framework
- TypeScript - Type safety
- Material-UI 6 - Components
- Vite 7 - Build tool
- Axios - HTTP client

**Cloud:**
- Cloud Run - Backend hosting
- Firestore - NoSQL database
- Cloud Storage - Frontend hosting
- Cloud Build - CI/CD

---

## 7. Feature Documentation

### 7.1 Authentication

**JWT Tokens:**
- 30-minute expiration
- HS256 algorithm
- Automatic refresh via Axios interceptors

**Password Security:**
- Username encrypted with password-derived key
- PBKDF2 with 100,000 iterations
- No password stored in database

**2FA (TOTP):**
- Google Authenticator integration
- QR code generation on registration
- 30-second token window
- Development bypass with `ENVIRONMENT=development`

### 7.2 Smart Identification

**How it works:**
1. User pastes chat conversation
2. Backend gathers context (people, types, AI instructions)
3. Sends structured prompt to Gemini API
4. AI returns parsed JSON with leave entries
5. User reviews and confirms mappings
6. Batch save to database

**Supported formats:** WhatsApp, Slack, Teams, Telegram

**Model:** `gemini-1.5-flash` (configurable via `GEMINI_MODEL`)

**Cost:** FREE (within daily limits)

### 7.3 People & Leave Types

- Add, edit, delete team members
- Add, edit, delete leave categories
- Tabbed interface in Settings page
- Real-time updates

### 7.4 Absence Logging

- Select person, type, date, duration
- Add reason and applied flag
- Form validation
- Auto-clear after save

### 7.5 Reports

- View all absences
- Filter by date range
- Delete entries
- Future: Export to CSV

### 7.6 Registration Control

Environment variable to enable/disable registration:
```
VITE_ENABLE_REGISTRATION=true|false
```

Use case: Enable during setup, disable after team onboarded

---

## 8. Security Implementation

**Implemented:**
 JWT with 30-min expiration  
 2FA mandatory for all users  
 Custom password encryption (PBKDF2)  
 CORS configuration  
 HTTPS (automatic on Cloud Run)  
 SQL injection protection (parameterized queries)  
 XSS protection (React escaping)  
 Environment-based secrets  

**Token Management:**
- Stored in `localStorage`
- Axios interceptor adds to all requests
- Automatic redirect on 401

**Protected Endpoints:**
All `/api/*` endpoints require valid JWT token.

**Public Endpoints:**
- `POST /auth/register`
- `POST /auth/login`

---

## 9. API Reference

### Authentication

**Register:**
```http
POST /auth/register
{"username": "string", "password": "string"}
 {"qr": "base64", "secret": "TOTP", "id": "uuid"}
```

**Login:**
```http
POST /auth/login
{"username": "string", "password": "string", "token": "123456"}
 {"access_token": "JWT", "username": "string"}
```

### People

```http
GET    /api/people
POST   /api/people         {"name": "string"}
PUT    /api/people/{id}    {"name": "string"}
DELETE /api/people/{id}
```

### Leave Types

```http
GET    /api/types
POST   /api/types          {"name": "string"}
PUT    /api/types/{id}     {"name": "string"}
DELETE /api/types/{id}
```

### Absences

```http
GET    /api/absences?date_from=YYYY-MM-DD&date_to=YYYY-MM-DD
POST   /api/absences       {"person_id", "type_id", "date", "duration", "reason"}
PUT    /api/absences/{id}
DELETE /api/absences/{id}
```

### Smart Identification

```http
POST /api/smart-identify   {"conversation": "string"}
 {"entries": [...], "raw_analysis": "string"}

GET  /api/smart-identify/health
 {"status": "success", "model": "gemini-1.5-flash"}
```

### Interactive Docs

- Swagger: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## 10. Google Cloud Deployment

### Quick Deploy

```powershell
# Update backend only
.\deploy-backend-update.ps1

# Full deployment (first time)
.\deploy-to-gcp-complete.ps1 -ProjectId "your-project"
```

Note: The deployment scripts use Cloud Build, so local Docker is not required.

### Production Checklist

- Ensure `gcloud` is authenticated to the correct project.
- Confirm the Cloud Run service uses Firestore (ENVIRONMENT=production).
- Make sure the service account running Cloud Run has Firestore access.
- Verify the frontend bucket name matches `PROJECTID-frontend`.
- If you change the backend URL, rebuild the frontend so `VITE_API_URL` is updated.

### IAM and Firestore Access

The backend uses Firestore in production and relies on the Cloud Run service account.
Grant at least the following IAM roles on the project:

- `roles/datastore.user` (Firestore read/write)
- `roles/cloudbuild.builds.editor` (Cloud Build)
- `roles/artifactregistry.writer` (image push)
- `roles/run.admin` (deploy Cloud Run)
- `roles/storage.admin` (upload frontend assets)

If Firestore calls fail, check that the Cloud Run service account has `roles/datastore.user`
and that Firestore is enabled in the project.

### CORS Notes

The deploy script sets `CORS_ORIGINS` to `https://storage.googleapis.com`.
If you serve the frontend from a custom domain or different bucket URL, update
`CORS_ORIGINS` accordingly and redeploy the backend.

### Manual Deployment

**Enable APIs:**
```powershell
gcloud services enable run.googleapis.com
gcloud services enable firestore.googleapis.com
gcloud services enable artifactregistry.googleapis.com
```

**Deploy Backend:**
```powershell
cd backend
gcloud builds submit --tag us-central1-docker.pkg.dev/PROJECT/leave-tracker-repo/backend:latest
gcloud run deploy leave-tracker-api --image=... --set-env-vars=...
```

**Deploy Frontend:**
```powershell
cd frontend
npm run build
gcloud storage cp dist/* gs://bucket-name/
```

### Cost Estimate

**FREE for small teams:**
- Cloud Run: 2M requests/month
- Firestore: 50K reads, 20K writes/day
- Storage: 5GB + 1GB egress/month
- Gemini API: 15 req/min, 1M tokens/day

**Expected:** $0/month within free tier

---

## 11. Troubleshooting

### Backend Won't Start
- Check Python 3.11+
- Activate venv
- Install requirements
- Verify .env exists with SECRET_KEY
- Check ENVIRONMENT variable

### Database Connection Error
- SQLite: Ensure `ENVIRONMENT=development`
- Firestore: Check `GOOGLE_APPLICATION_CREDENTIALS`
- Verify service account key is valid

### 401 Unauthorized
- Token expired (30 min) - login again
- Check localStorage token
- Verify SECRET_KEY unchanged

### 2FA Token Invalid
- Time sync in authenticator app
- Try new token (30-sec window)
- Development: Check `ENVIRONMENT=development` bypass

### Smart Identification Error
- Set `GEMINI_API_KEY` in .env
- Restart backend
- Verify key at https://aistudio.google.com/
- Check model is `gemini-1.5-flash` (or set `GEMINI_MODEL` to a valid model)

### Frontend Shows Old Version
- Clear browser cache
- Use incognito mode
- Check cache-control headers

---

## 12. Maintenance

### Regular Tasks

**Weekly:**
- Check logs for errors
- Monitor free tier usage

**Monthly:**
- Update dependencies
- Review security advisories

**Quarterly:**
- Full dependency updates
- Security audit

### Updating Dependencies

**Backend:**
```powershell
pip list --outdated
pip install --upgrade package-name
pip freeze > requirements.txt
```

**Frontend:**
```powershell
npm outdated
npm update package-name
npm update
```

### Backup & Restore

**Backup:**
```powershell
python backend/setup_local_data.py  # Export to JSON
```

**Restore to SQLite:**
```powershell
python backend/import_to_sqlite.py
```

**Restore to Firestore:**
```powershell
python backend/import_to_firestore.py
```

### Version Control

**Commit format:**
```
feat: Add Smart Identification
fix: Resolve JWT expiration
docs: Update guide
chore: Update deps
```

---

## Quick Reference

### Development Commands
```powershell
# Backend
cd backend; uvicorn app.main:app --reload

# Frontend
cd frontend; npm run dev

# Build
npm run build
docker build -t backend backend/

# Deploy
.\deploy-backend-update.ps1

# Logs
gcloud run services logs tail leave-tracker-api
```

### Environment Variables

**Backend .env:**
```
ENVIRONMENT=development|production
SECRET_KEY=32-byte-hex
GEMINI_API_KEY=your-key
GOOGLE_APPLICATION_CREDENTIALS=firestore-key.json
```

**Frontend .env.development:**
```
VITE_API_URL=http://localhost:8000
VITE_ENABLE_REGISTRATION=true
```

### Useful Links

- Gemini API: https://aistudio.google.com/apikey
- GCP Console: https://console.cloud.google.com
- FastAPI: https://fastapi.tiangolo.com
- React: https://react.dev
- Material-UI: https://mui.com

---

## Summary

**Status:** Production Ready   
**Version:** 1.2.0  
**Cost:** $0/month (free tier)  
**Updated:** November 3, 2025

This guide provides everything needed to develop and deploy Leave Tracker. For questions or issues, check the troubleshooting section or create a GitHub issue.
