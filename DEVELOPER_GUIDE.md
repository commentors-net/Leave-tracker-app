# Leave Tracker - Complete Developer Guide

**Version 1.1.0** | Last Updated: November 2, 2025

A comprehensive guide for developers to understand, develop, and deploy the Leave Tracker application.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Local Development Setup](#local-development-setup)
4. [Technology Stack](#technology-stack)
5. [Project Structure](#project-structure)
6. [Feature Documentation](#feature-documentation)
7. [Security Implementation](#security-implementation)
8. [API Reference](#api-reference)
9. [Google Cloud Deployment](#google-cloud-deployment)
10. [Configuration Management](#configuration-management)
11. [Troubleshooting](#troubleshooting)
12. [Maintenance & Updates](#maintenance--updates)

---

## Project Overview

### What is Leave Tracker?

Leave Tracker is a production-ready web application for managing team absences and leave requests. It features:

- **Secure authentication** with JWT tokens and 2FA (TOTP)
- **Leave management** with people, types, and absence tracking
- **Smart Identification** using AI to parse chat conversations and extract leave information
- **Google Cloud deployment** using free tier services
- **Modern tech stack** with FastAPI (Python) backend and React (TypeScript) frontend

### Key Features

#### Core Features
- ✅ **JWT Authentication** with 30-minute token expiration
- ✅ **2FA (TOTP)** using Google Authenticator
- ✅ **People Management** - Add, edit, delete team members
- ✅ **Leave Types** - Customizable leave categories (Medical, Annual, WFH, etc.)
- ✅ **Absence Logging** - Track leaves with date, duration, type, and reason
- ✅ **Settings Interface** - Manage people and leave types

#### Advanced Features
- ✅ **Smart Identification** - AI-powered chat conversation parsing (Gemini API)
- ✅ **Registration Control** - Enable/disable public registration
- ✅ **Secure Password Handling** - Username encrypted with password-derived key
- ✅ **Automatic Token Management** - Axios interceptors handle JWT seamlessly
- ✅ **Path Aliases** - Clean imports using `@services/api`, `@pages/`, etc.

### Technology Highlights

- **Backend**: FastAPI + SQLAlchemy + PostgreSQL
- **Frontend**: React 19 + TypeScript + Material-UI + Vite 7
- **Authentication**: JWT + TOTP (pyotp)
- **AI**: Google Gemini 1.5 Flash (free tier)
- **Deployment**: Google Cloud Run + Cloud SQL + Cloud Storage
- **Build**: Docker (Cloud Build) + npm

---

## Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND (React)                          │
│  Cloud Storage - Static Website Hosting                         │
│  - React 19 + TypeScript + Material-UI                          │
│  - Vite 7 Build System                                          │
│  - JWT Token Management                                          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ HTTPS/REST API
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                       BACKEND (FastAPI)                          │
│  Cloud Run - Serverless Container                               │
│  - FastAPI + Uvicorn                                            │
│  - JWT Authentication + 2FA                                      │
│  - SQLAlchemy ORM                                               │
│  - Google Gemini AI Integration                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ Cloud SQL Proxy
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    DATABASE (PostgreSQL)                         │
│  Cloud SQL - Managed Database                                   │
│  - db-f1-micro (Free Tier)                                      │
│  - 10GB Storage                                                 │
│  - Automatic Backups                                            │
└─────────────────────────────────────────────────────────────────┘

External Services:
  - Google Gemini API (Smart Identification)
  - Artifact Registry (Docker Images)
  - Cloud Build (CI/CD)
```

### Data Flow

#### Authentication Flow
```
User → Login Page → Backend (/auth/login)
  ↓
Verify username + password + 2FA token
  ↓
Generate JWT token
  ↓
Return token to frontend
  ↓
Store in localStorage
  ↓
Include in all API requests (Authorization header)
```

#### Smart Identification Flow
```
User pastes chat → Smart Identification Page
  ↓
Send to Backend (/api/smart-identify)
  ↓
Backend queries database for context (people, types)
  ↓
Send to Gemini AI with structured prompt
  ↓
Parse AI response (JSON)
  ↓
Return parsed leave entries to frontend
  ↓
User reviews and maps entries
  ↓
Save to database (/api/absences)
```

### Database Schema

```sql
-- Users Table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    hashed_username TEXT NOT NULL,  -- Encrypted with password
    totp_secret TEXT NOT NULL
);

-- People Table
CREATE TABLE people (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Leave Types Table
CREATE TABLE types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Absences Table
CREATE TABLE absences (
    id SERIAL PRIMARY KEY,
    person_id INTEGER REFERENCES people(id),
    type_id INTEGER REFERENCES types(id),
    date DATE NOT NULL,
    duration VARCHAR(50) NOT NULL,  -- "Full Day", "First Half", "Second Half"
    reason TEXT
);
```

---

## Local Development Setup

### Prerequisites

- **Python 3.11+** - Backend runtime
- **Node.js 18+** - Frontend build tool
- **PostgreSQL 14+** (optional for local dev, can use SQLite)
- **Git** - Version control
- **VS Code** (recommended) - IDE with debugging configured

### Step 1: Clone Repository

```powershell
git clone https://github.com/commentors-net/Leave-tracker-app.git
cd Leave-tracker-app
```

### Step 2: Backend Setup

```powershell
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Create .env file
@"
SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=sqlite:///./database.db
CORS_ORIGINS=http://localhost:5173
GEMINI_API_KEY=your_gemini_api_key_here
"@ | Out-File -FilePath .env -Encoding utf8

# Run backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: http://localhost:8000

### Step 3: Frontend Setup

```powershell
cd frontend

# Install dependencies
npm install

# Create .env.development file
@"
VITE_API_URL=http://localhost:8000
VITE_ENABLE_REGISTRATION=true
"@ | Out-File -FilePath .env.development -Encoding utf8

# Run frontend
npm run dev
```

Frontend will be available at: http://localhost:5173

### Step 4: First Time Setup

1. **Register a User**:
   - Go to http://localhost:5173/register
   - Create username and password
   - Scan QR code with Google Authenticator
   - Save the secret key shown

2. **Add People and Leave Types**:
   - Login with your credentials + 2FA code
   - Go to Settings
   - Add team members (e.g., John Doe, Jane Smith)
   - Add leave types (e.g., Medical, Annual, WFH, Dependent)

3. **Test Smart Identification** (requires Gemini API key):
   - Get free API key from https://makersuite.google.com/app/apikey
   - Add to backend `.env`: `GEMINI_API_KEY=your_key`
   - Restart backend
   - Go to Smart Identification page
   - Click "Load Example" and test

### VS Code Debugging (F5)

The project includes `.vscode/launch.json` with two debug configurations:

1. **Backend (FastAPI)** - Port 8000
2. **Frontend (npm)** - Port 5173

Press **F5** to start both simultaneously!

---

## Technology Stack

### Backend Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.11+ | Runtime |
| FastAPI | Latest | Web framework |
| Uvicorn | Latest | ASGI server |
| SQLAlchemy | Latest | ORM |
| Pydantic | 2.x | Data validation |
| PostgreSQL | 14+ | Production database |
| SQLite | - | Development database |
| python-jose | Latest | JWT handling |
| passlib | Latest | Password hashing |
| pyotp | Latest | TOTP (2FA) |
| qrcode | Latest | QR code generation |
| google-generativeai | Latest | Gemini AI |
| psycopg2-binary | Latest | PostgreSQL driver |

### Frontend Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| React | 19.x | UI framework |
| TypeScript | 5.x | Type safety |
| Vite | 7.x | Build tool |
| Material-UI | 6.x | Component library |
| Axios | Latest | HTTP client |
| React Router | 7.x | Routing |

### DevOps Stack

| Technology | Purpose |
|------------|---------|
| Docker | Backend containerization |
| Google Cloud Build | Remote Docker builds |
| Google Cloud Run | Backend hosting |
| Google Cloud SQL | PostgreSQL database |
| Google Cloud Storage | Frontend static hosting |
| Google Artifact Registry | Docker image storage |

---

## Project Structure

```
Leave-tracker-app/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                    # FastAPI app entry point
│   │   ├── database.py                # Database connection
│   │   ├── models.py                  # SQLAlchemy models
│   │   ├── schemas.py                 # Pydantic schemas
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   └── security.py            # JWT + password encryption
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py                # Authentication endpoints
│   │   │   ├── people.py              # People CRUD
│   │   │   ├── types.py               # Leave types CRUD
│   │   │   ├── absences.py            # Absences CRUD
│   │   │   └── smart_identification.py # AI parsing
│   │   └── services/
│   │       └── __init__.py
│   ├── Dockerfile                     # Backend container
│   ├── requirements.txt               # Python dependencies
│   └── test_auth.py                   # Auth tests
│
├── frontend/
│   ├── src/
│   │   ├── main.tsx                   # React entry point
│   │   ├── App.tsx                    # Main app component
│   │   ├── config.ts                  # API configuration
│   │   ├── index.css                  # Global styles
│   │   ├── pages/
│   │   │   ├── Login.tsx              # Login page
│   │   │   ├── Register.tsx           # Registration page
│   │   │   ├── Dashboard.tsx          # Absence logging
│   │   │   ├── Settings.tsx           # People/types management
│   │   │   └── SmartIdentification.tsx # AI parsing UI
│   │   └── services/
│   │       └── api.ts                 # API client + TypeScript types
│   ├── public/
│   │   └── vite.svg                   # Favicon
│   ├── index.html                     # HTML template
│   ├── package.json                   # npm dependencies
│   ├── tsconfig.json                  # TypeScript config
│   ├── vite.config.ts                 # Vite dev config
│   ├── vite.prod.config.ts            # Vite production config
│   └── .env.production                # Production environment
│
├── .vscode/
│   └── launch.json                    # VS Code debug config
│
├── deploy-frontend.ps1                # Frontend deployment script
├── deploy-to-gcp.ps1                  # Full GCP deployment script
├── DEVELOPER_GUIDE.md                 # This file
└── README.md                          # Project overview
```

---

## Feature Documentation

### 1. Authentication System

#### JWT Token Authentication

**Implementation**: `backend/app/core/security.py`

```python
def create_access_token(data: dict, expires_delta: timedelta = None):
    """Generate JWT token with expiration"""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=30))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    """Verify and decode JWT token"""
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload
```

**Features**:
- 30-minute token expiration (configurable)
- HS256 algorithm
- Includes username in payload
- Automatic token refresh on API calls

#### Password Encryption

**Unique Approach**: Username encrypted with password-derived key

```python
def encrypt_username_with_password(username: str, password: str) -> str:
    """Encrypt username using password as key"""
    # Derive key from password
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b'fixed_salt_for_this_app',
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    
    # Encrypt username
    f = Fernet(key)
    return f.encrypt(username.encode()).decode()
```

**Why this approach?**
- Username is sensitive data
- Password never stored in plain text or standard hash
- Username can only be decrypted with correct password
- Adds extra layer of security

#### 2FA (TOTP)

**Implementation**: Uses `pyotp` library

**Registration Flow**:
1. Generate secret: `pyotp.random_base32()`
2. Create QR code: `pyotp.totp.TOTP(secret).provisioning_uri()`
3. Store secret in database
4. User scans QR with authenticator app

**Login Verification**:
```python
totp = pyotp.TOTP(user.totp_secret)
if not totp.verify(token, valid_window=1):
    raise HTTPException(status_code=401, detail="Invalid 2FA token")
```

### 2. People & Leave Types Management

**API Endpoints**:
- `GET /api/people` - List all people
- `POST /api/people` - Create person
- `PUT /api/people/{id}` - Update person
- `DELETE /api/people/{id}` - Delete person
- Same pattern for `/api/types`

**Frontend Implementation**: `frontend/src/pages/Settings.tsx`

Features:
- Tabbed interface (People | Leave Types)
- Add new entries with text input + button
- Inline editing with Material-UI dialog
- Delete with confirmation
- Real-time updates

### 3. Absence Logging

**API Endpoint**: `POST /api/absences`

**Request Schema**:
```typescript
{
  person_id: number;
  type_id: number;
  date: string;        // YYYY-MM-DD
  duration: string;    // "Full Day" | "First Half" | "Second Half"
  reason: string;
}
```

**Frontend Implementation**: `frontend/src/pages/Dashboard.tsx`

Features:
- Dropdowns for person and leave type
- Date picker
- Duration selector
- Reason text field
- Form validation
- Success feedback

### 4. Smart Identification (AI-Powered)

**API Endpoint**: `POST /api/smart-identify`

**How it works**:

1. **User Input**: Paste chat conversation
2. **Context Gathering**: Backend queries database for people and leave types
3. **AI Prompt**: Send structured prompt to Gemini API:
   ```
   You are an expert at parsing chat conversations...
   
   CONTEXT:
   - Known people: John, Jane, Bob
   - Known leave types: Medical, Annual, WFH
   
   CHAT CONVERSATION:
   [11:51 AM, 10/31/2025] John: Not feeling well, taking MC
   
   TASK:
   Extract leave information in JSON format...
   ```

4. **AI Response**: Parse JSON response
5. **Smart Mapping**: Auto-match names to database people
6. **User Review**: User confirms/adjusts mappings
7. **Save**: Batch save to database

**Implementation**: `backend/app/api/smart_identification.py`

**Frontend**: `frontend/src/pages/SmartIdentification.tsx`

**Features**:
- Supports WhatsApp, Telegram, Slack, Teams formats
- Detects actual leave requests (ignores "GWS" responses)
- Confidence levels (high/medium/low)
- Fuzzy name matching
- Leave type keyword detection
- Batch processing
- Review table with dropdowns
- Save individual or all at once

**Configuration**:
```bash
# Backend .env
GEMINI_API_KEY=your_api_key_here

# Get free key from: https://makersuite.google.com/app/apikey
```

**Cost**: FREE (Gemini 1.5 Flash free tier: 15 requests/min, 1M tokens/day)

### 5. Registration Control

**Feature Toggle**: Enable/disable public registration

**Configuration**:
```bash
# frontend/.env.production
VITE_ENABLE_REGISTRATION=false  # Default: disabled
```

**Implementation**: `frontend/src/config.ts` + `frontend/src/App.tsx`

When disabled:
- Register button hidden from navigation
- `/register` route redirects to `/login`
- Direct URL access blocked

When enabled:
- Register button visible
- Full registration flow available

**Use Case**: Disable after initial team setup to prevent unauthorized registrations

---

## Security Implementation

### Authentication & Authorization

#### 1. JWT Token Management

**Token Storage**: `localStorage`
- Key: `access_token`
- Value: JWT token string

**Token Inclusion**: Axios interceptor automatically adds to all requests

```typescript
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
```

**Token Expiration Handling**:

```typescript
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem("access_token");
      localStorage.removeItem("username");
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);
```

#### 2. API Endpoint Protection

**Backend Dependency**:

```python
from ..core.security import get_current_user

@router.get("/protected-endpoint")
async def protected_route(current_user: User = Depends(get_current_user)):
    # Only accessible with valid JWT
    return {"user": current_user.username}
```

**Public Endpoints** (no JWT required):
- `POST /auth/register`
- `POST /auth/login`

**Protected Endpoints** (JWT required):
- `GET /api/people`
- `POST /api/people`
- `GET /api/types`
- `POST /api/absences`
- `POST /api/smart-identify`
- All other API endpoints

#### 3. Password Security

**Never Stored in Plain Text**:
- Username encrypted with password-derived key
- Password never stored (only used for encryption/decryption)
- PBKDF2 key derivation with 100,000 iterations

**Login Verification**:
1. Receive username, password, 2FA token
2. Try to decrypt stored encrypted username with provided password
3. If decryption succeeds → password correct
4. Verify 2FA token
5. Generate JWT token

#### 4. CORS Configuration

**Backend**: `backend/app/main.py`

```python
cors_origins = os.getenv("CORS_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Production Configuration**:
```bash
CORS_ORIGINS=https://storage.googleapis.com
```

#### 5. Environment Variables

**Sensitive Data** (never commit to git):
- `SECRET_KEY` - JWT signing key
- `DATABASE_URL` - Database connection string
- `GEMINI_API_KEY` - AI API key

**`.gitignore` includes**:
- `.env`
- `.env.local`
- `.env.production`
- `DEPLOYMENT_COMPLETE.md`
- `deploy-*.ps1`

### Security Best Practices Implemented

✅ **JWT Expiration**: 30-minute tokens prevent long-term hijacking  
✅ **2FA**: Additional authentication factor  
✅ **HTTPS**: Cloud Run provides automatic HTTPS  
✅ **CORS**: Restricted to frontend domain  
✅ **SQL Injection Protection**: SQLAlchemy ORM parameterization  
✅ **XSS Protection**: React escapes output by default  
✅ **Secrets Management**: Environment variables  
✅ **Database Access**: Cloud SQL Proxy (no public IP)  

### Security Recommendations

🔒 **Rotate Secrets Regularly**:
```powershell
# Generate new JWT secret
$newSecret = python -c "import secrets; print(secrets.token_hex(32))"

# Update Cloud Run
gcloud run services update leave-tracker-api `
  --update-env-vars="SECRET_KEY=$newSecret" `
  --region=us-central1
```

🔒 **Enable Cloud Armor** (DDoS protection):
```powershell
gcloud compute security-policies create leave-tracker-policy
```

🔒 **Set Up Budget Alerts**:
- Cloud Console → Billing → Budgets
- Alert at $5/month threshold

🔒 **Review IAM Permissions**:
- Principle of least privilege
- Remove unnecessary service accounts

---

## API Reference

### Base URL

- **Development**: `http://localhost:8000`
- **Production**: `https://leave-tracker-api-427212681311.us-central1.run.app`

### Authentication Endpoints

#### Register User

```http
POST /auth/register
Content-Type: application/json

{
  "username": "string",
  "password": "string"
}
```

**Response**:
```json
{
  "qr": "base64_qr_code_image",
  "secret": "TOTP_SECRET_KEY",
  "username": "string",
  "id": 1
}
```

#### Login

```http
POST /auth/login
Content-Type: application/json

{
  "username": "string",
  "password": "string",
  "token": "123456"
}
```

**Response**:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "username": "string"
}
```

#### Change Password

```http
POST /auth/change-password
Authorization: Bearer <token>
Content-Type: application/json

{
  "username": "string",
  "old_password": "string",
  "new_password": "string"
}
```

### People Endpoints

#### Get All People

```http
GET /api/people
Authorization: Bearer <token>
```

**Response**:
```json
[
  {
    "id": 1,
    "name": "John Doe"
  }
]
```

#### Create Person

```http
POST /api/people
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "string"
}
```

#### Update Person

```http
PUT /api/people/{id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "string"
}
```

#### Delete Person

```http
DELETE /api/people/{id}
Authorization: Bearer <token>
```

### Leave Types Endpoints

Same pattern as People:
- `GET /api/types`
- `POST /api/types`
- `PUT /api/types/{id}`
- `DELETE /api/types/{id}`

### Absences Endpoints

#### Get All Absences

```http
GET /api/absences
Authorization: Bearer <token>
```

**Response**:
```json
[
  {
    "id": 1,
    "person_id": 1,
    "type_id": 1,
    "date": "2025-10-31",
    "duration": "Full Day",
    "reason": "Not feeling well"
  }
]
```

#### Create Absence

```http
POST /api/absences
Authorization: Bearer <token>
Content-Type: application/json

{
  "person_id": 1,
  "type_id": 1,
  "date": "2025-10-31",
  "duration": "Full Day",
  "reason": "string"
}
```

### Smart Identification Endpoints

#### Analyze Conversation

```http
POST /api/smart-identify
Authorization: Bearer <token>
Content-Type: application/json

{
  "conversation": "string (chat messages)"
}
```

**Response**:
```json
{
  "entries": [
    {
      "person_name": "John Doe",
      "date": "10/31/2025",
      "leave_type": "Medical",
      "reason": "Not feeling well...",
      "confidence": "high"
    }
  ],
  "raw_analysis": "Found 1 leave request..."
}
```

#### Check AI Health

```http
GET /api/smart-identify/health
Authorization: Bearer <token>
```

**Response**:
```json
{
  "status": "success",
  "message": "Gemini API is configured and working",
  "configured": true,
  "model": "gemini-1.5-flash"
}
```

### API Documentation

Interactive API docs available at:
- **Swagger UI**: `https://leave-tracker-api-427212681311.us-central1.run.app/docs`
- **ReDoc**: `https://leave-tracker-api-427212681311.us-central1.run.app/redoc`

---

## Google Cloud Deployment

### Architecture Overview

- **Frontend**: Cloud Storage (static website hosting)
- **Backend**: Cloud Run (serverless containers)
- **Database**: Cloud SQL (PostgreSQL, db-f1-micro free tier)
- **Images**: Artifact Registry
- **Build**: Cloud Build (remote Docker builds)

### Prerequisites

1. **Google Cloud Account** with billing enabled
2. **gcloud CLI** installed: https://cloud.google.com/sdk/docs/install
3. **Project ID** chosen (e.g., `leave-tracker-2025`)
4. **Gemini API Key**: https://makersuite.google.com/app/apikey

### Quick Deployment (15 minutes)

#### Step 1: Initial Setup

```powershell
# Login to Google Cloud
gcloud auth login

# Create project
gcloud projects create leave-tracker-2025 --name="Leave Tracker"

# Set as active project
gcloud config set project leave-tracker-2025

# Link billing (required for Cloud SQL)
gcloud billing projects link leave-tracker-2025 `
  --billing-account=YOUR-BILLING-ACCOUNT-ID

# Enable APIs
gcloud services enable run.googleapis.com
gcloud services enable sqladmin.googleapis.com
gcloud services enable artifactregistry.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable storage-api.googleapis.com

# Set region
gcloud config set run/region us-central1
```

#### Step 2: Create Infrastructure

```powershell
# Create Artifact Registry
gcloud artifacts repositories create leave-tracker-repo `
  --repository-format=docker `
  --location=us-central1 `
  --description="Leave Tracker Docker images"

# Create PostgreSQL Database
gcloud sql instances create leave-tracker-db `
  --database-version=POSTGRES_14 `
  --tier=db-f1-micro `
  --region=us-central1 `
  --storage-type=HDD `
  --storage-size=10GB

# Wait for database (takes 5-7 minutes)
gcloud sql instances list

# Set database password
gcloud sql users set-password postgres `
  --instance=leave-tracker-db `
  --password="YOUR-SECURE-PASSWORD"

# Create database
gcloud sql databases create leavetracker `
  --instance=leave-tracker-db
```

#### Step 3: Build and Deploy Backend

```powershell
# Generate JWT secret
$SECRET_KEY = python -c "import secrets; print(secrets.token_hex(32))"

# Build Docker image (Cloud Build - no local Docker needed!)
gcloud builds submit D:\Jobs\workspace\python-projects\Leave-tracker-app\backend `
  --tag us-central1-docker.pkg.dev/leave-tracker-2025/leave-tracker-repo/backend:v1.1.0 `
  --project=leave-tracker-2025 `
  --timeout=20m

# Get SQL connection name
$SQL_CONNECTION = gcloud sql instances describe leave-tracker-db `
  --format='value(connectionName)'

# Build database URL
$DATABASE_URL = "postgresql://postgres:YOUR-PASSWORD@/leavetracker?host=/cloudsql/$SQL_CONNECTION"

# Deploy to Cloud Run
gcloud run deploy leave-tracker-api `
  --image=us-central1-docker.pkg.dev/leave-tracker-2025/leave-tracker-repo/backend:v1.1.0 `
  --region=us-central1 `
  --allow-unauthenticated `
  --memory=512Mi `
  --cpu=1 `
  --timeout=300 `
  --set-env-vars="SECRET_KEY=$SECRET_KEY,DATABASE_URL=$DATABASE_URL,GEMINI_API_KEY=YOUR-GEMINI-KEY,CORS_ORIGINS=https://storage.googleapis.com" `
  --add-cloudsql-instances=$SQL_CONNECTION
```

#### Step 4: Build and Deploy Frontend

```powershell
# Update production environment
cd frontend
@"
VITE_API_URL=https://YOUR-BACKEND-URL.run.app
VITE_ENABLE_REGISTRATION=false
"@ | Out-File -FilePath .env.production -Encoding utf8

# Build frontend
npm run build

# Create Cloud Storage bucket
cd ..
gcloud storage buckets create gs://leave-tracker-2025-frontend `
  --location=us-central1 `
  --no-public-access-prevention

# Grant public access
gcloud storage buckets add-iam-policy-binding gs://leave-tracker-2025-frontend `
  --member=allUsers `
  --role=roles/storage.objectViewer

# Configure static website hosting
gcloud storage buckets update gs://leave-tracker-2025-frontend `
  --web-main-page-suffix=index.html `
  --web-error-page=index.html

# Upload files
gcloud storage cp frontend/dist/index.html gs://leave-tracker-2025-frontend/
gcloud storage cp -r frontend/dist/assets gs://leave-tracker-2025-frontend/
gcloud storage cp -r frontend/dist/public gs://leave-tracker-2025-frontend/

# Set cache control
gcloud storage objects update gs://leave-tracker-2025-frontend/index.html `
  --cache-control="no-cache, no-store, must-revalidate"
```

#### Step 5: Verify Deployment

```powershell
# Test backend
curl https://YOUR-BACKEND-URL.run.app/docs

# Test frontend
Start-Process "https://storage.googleapis.com/leave-tracker-2025-frontend/index.html"
```

### Automated Deployment Script

Use the included `deploy-to-gcp.ps1` for one-command deployment:

```powershell
.\deploy-to-gcp.ps1 `
  -ProjectId "leave-tracker-2025" `
  -SecretKey "$(python -c 'import secrets; print(secrets.token_hex(32))')" `
  -DbPassword "your-secure-password" `
  -GeminiApiKey "your-gemini-api-key"
```

### Cost Breakdown (Free Tier)

| Service | Configuration | Free Tier | Monthly Cost |
|---------|---------------|-----------|--------------|
| Cloud Run | 512Mi RAM, 1 CPU | 2M requests/month | $0 |
| Cloud SQL | db-f1-micro, 10GB | 1 instance | $0 |
| Cloud Storage | 5GB, website hosting | 5GB + 1GB egress | $0 |
| Artifact Registry | Docker images | 0.5GB | $0 |
| Cloud Build | Remote builds | 120 build-minutes/day | $0 |
| Gemini API | 1.5 Flash | 15 req/min, 1M tokens/day | $0 |
| **TOTAL** | Small team usage | **All within free tier** | **$0/month** |

### Monitoring & Maintenance

#### View Logs

```powershell
# Backend logs
gcloud run services logs read leave-tracker-api --region=us-central1 --limit=50

# Real-time logs
gcloud run services logs tail leave-tracker-api --region=us-central1

# Database logs
gcloud sql operations list --instance=leave-tracker-db
```

#### Update Backend

```powershell
# Make code changes
# Rebuild image
gcloud builds submit backend --tag ...repo/backend:v1.1.1

# Deploy new version
gcloud run deploy leave-tracker-api --image=...repo/backend:v1.1.1
```

#### Update Frontend

```powershell
# Make code changes
cd frontend
npm run build

# Deploy
.\deploy-frontend.ps1
```

#### Database Backup

```powershell
# Create manual backup
gcloud sql backups create --instance=leave-tracker-db

# List backups
gcloud sql backups list --instance=leave-tracker-db

# Restore from backup
gcloud sql backups restore BACKUP_ID `
  --backup-instance=leave-tracker-db `
  --backup-project=leave-tracker-2025
```

### Console URLs

- **Project Dashboard**: https://console.cloud.google.com/home/dashboard?project=leave-tracker-2025
- **Cloud Run**: https://console.cloud.google.com/run?project=leave-tracker-2025
- **Cloud SQL**: https://console.cloud.google.com/sql/instances?project=leave-tracker-2025
- **Cloud Storage**: https://console.cloud.google.com/storage/browser?project=leave-tracker-2025
- **Artifact Registry**: https://console.cloud.google.com/artifacts?project=leave-tracker-2025
- **Cloud Build**: https://console.cloud.google.com/cloud-build/builds?project=leave-tracker-2025
- **Billing**: https://console.cloud.google.com/billing?project=leave-tracker-2025

---

## Configuration Management

### Environment Variables

#### Backend (`backend/.env` or Cloud Run)

```bash
# Required
SECRET_KEY=<32-byte-hex-string>
DATABASE_URL=postgresql://user:pass@host/db
CORS_ORIGINS=https://your-frontend-url.com

# Optional
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
GEMINI_API_KEY=<gemini-api-key>
```

#### Frontend (`frontend/.env.development` / `frontend/.env.production`)

```bash
# Required
VITE_API_URL=http://localhost:8000  # or production URL

# Optional
VITE_ENABLE_REGISTRATION=false
```

### Configuration Files

#### Backend Configuration

**`backend/app/database.py`**:
```python
# Conditional database configuration
if DATABASE_URL.startswith("postgresql"):
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
else:
    engine = create_engine(DATABASE_URL, check_same_thread=False)
```

**`backend/app/main.py`**:
```python
# CORS configuration from environment
cors_origins = os.getenv("CORS_ORIGINS", "*").split(",")
```

#### Frontend Configuration

**`frontend/src/config.ts`**:
```typescript
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const config = {
  apiUrl: API_URL,
  features: {
    enableRegistration: import.meta.env.VITE_ENABLE_REGISTRATION === 'true' || false,
  },
  endpoints: {
    auth: {
      register: `${API_URL}/auth/register`,
      login: `${API_URL}/auth/login`,
    },
    // ... other endpoints
  },
};
```

**`frontend/vite.config.ts`**:
```typescript
export default defineConfig({
  base: './',  // Relative paths for Cloud Storage
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      '@services': path.resolve(__dirname, './src/services'),
      '@pages': path.resolve(__dirname, './src/pages'),
    },
  },
});
```

### Path Aliases

Frontend uses path aliases for clean imports:

```typescript
// Instead of: import api from '../../services/api'
import api from '@services/api'

// Instead of: import Login from '../../pages/Login'
import Login from '@pages/Login'

// Instead of: import config from '../config'
import config from '@/config'
```

**Configuration**: `tsconfig.json` + `vite.config.ts`

---

## Troubleshooting

### Common Issues

#### 1. Backend Won't Start

**Symptom**: `uvicorn app.main:app` fails

**Solutions**:
- Check Python version: `python --version` (needs 3.11+)
- Activate virtual environment: `.\venv\Scripts\activate`
- Install dependencies: `pip install -r requirements.txt`
- Check `.env` file exists with `SECRET_KEY`
- Verify database file/connection

#### 2. Frontend Build Fails

**Symptom**: `npm run build` errors

**Solutions**:
- Check Node version: `node --version` (needs 18+)
- Delete `node_modules`: `rm -r node_modules`
- Reinstall: `npm install`
- Clear cache: `npm cache clean --force`
- Check for TypeScript errors: `npm run build` shows errors

#### 3. 401 Unauthorized on API Calls

**Symptom**: All protected endpoints return 401

**Solutions**:
- Check JWT token in localStorage: `localStorage.getItem('access_token')`
- Token might be expired (30 minutes)
- Login again to get new token
- Check backend `SECRET_KEY` hasn't changed
- Verify CORS is configured correctly

#### 4. Login Fails with "Invalid 2FA token"

**Symptom**: Correct password but 2FA fails

**Solutions**:
- Check authenticator app time sync (Settings → Time correction)
- Verify you're using the correct secret key
- Token has 30-second window, try again
- Check `totp_secret` in database is correct
- Try manual time sync on authenticator app

#### 5. Smart Identification Not Working

**Symptom**: "Gemini API key not configured"

**Solutions**:
- Set `GEMINI_API_KEY` in backend `.env`
- Restart backend after adding key
- Verify key is valid: test at https://makersuite.google.com/
- Check API quota hasn't been exceeded
- Check backend logs for detailed error

#### 6. Database Connection Error

**Symptom**: SQLAlchemy connection errors

**Solutions**:
- Local: Check `database.db` file exists in backend folder
- PostgreSQL: Verify connection string format
- Cloud SQL: Check Cloud SQL Proxy is configured
- Check database credentials are correct
- Test connection: `psql -h localhost -U postgres -d leavetracker`

#### 7. Cloud Storage Upload Fails

**Symptom**: `gcloud storage cp` fails with "No objects matched"

**Solutions**:
- Use absolute paths: `gcloud storage cp C:\path\to\file gs://bucket/`
- Upload files individually instead of wildcards
- Check bucket exists: `gcloud storage ls`
- Check permissions: `gcloud storage buckets describe gs://bucket`
- Use the provided `deploy-frontend.ps1` script

#### 8. Frontend Shows Old Version

**Symptom**: Changes not visible after deployment

**Solutions**:
- Clear browser cache (Ctrl + Shift + Delete)
- Use incognito mode
- Add cache-buster: `?v=timestamp`
- Check cache-control headers are set
- Verify correct files are uploaded: `gcloud storage ls gs://bucket/ --recursive`

### Debugging Tips

#### Backend Debugging

```powershell
# Run with verbose logging
uvicorn app.main:app --reload --log-level debug

# Check environment variables
Get-ChildItem Env:

# Test database connection
python -c "from app.database import engine; print(engine)"

# Check API endpoint
curl http://localhost:8000/docs
```

#### Frontend Debugging

```powershell
# Run with source maps
npm run dev

# Check environment variables
npm run dev -- --debug

# Test API connection
curl http://localhost:5173

# Check build output
npm run build -- --debug
```

#### Cloud Debugging

```powershell
# Check Cloud Run logs
gcloud run services logs read leave-tracker-api --limit=100

# Check Cloud Build logs
gcloud builds list --limit=10
gcloud builds log BUILD_ID

# Check SQL operations
gcloud sql operations list --instance=leave-tracker-db

# Test Cloud Run endpoint
curl https://your-service-url.run.app/docs
```

### Error Messages Reference

| Error | Cause | Solution |
|-------|-------|----------|
| `401 Unauthorized` | Invalid/expired JWT | Login again |
| `403 Forbidden` | Missing permissions | Check IAM roles |
| `404 Not Found` | Wrong endpoint/route | Verify URL |
| `422 Unprocessable Entity` | Invalid request data | Check request schema |
| `500 Internal Server Error` | Backend exception | Check backend logs |
| `CORS error` | Missing CORS config | Add frontend URL to CORS_ORIGINS |
| `Database connection failed` | Wrong connection string | Verify DATABASE_URL |
| `Module not found` | Missing dependency | Run pip/npm install |

---

## Maintenance & Updates

### Regular Maintenance Tasks

#### Weekly
- ✅ Check application logs for errors
- ✅ Verify database backups are running
- ✅ Monitor free tier usage

#### Monthly
- ✅ Update dependencies: `pip list --outdated`, `npm outdated`
- ✅ Review and rotate secrets if needed
- ✅ Check for security updates
- ✅ Review user accounts and remove inactive users

#### Quarterly
- ✅ Full dependency updates
- ✅ Security audit
- ✅ Performance review
- ✅ Backup verification (test restore)

### Updating Dependencies

#### Backend Dependencies

```powershell
cd backend

# Check outdated packages
pip list --outdated

# Update specific package
pip install --upgrade package-name

# Update all (with caution)
pip install --upgrade -r requirements.txt

# Test after updates
python -m pytest

# Freeze new versions
pip freeze > requirements.txt
```

#### Frontend Dependencies

```powershell
cd frontend

# Check outdated packages
npm outdated

# Update specific package
npm update package-name

# Update all (with caution)
npm update

# Test after updates
npm run build
npm run dev

# Lock new versions
npm install  # Updates package-lock.json
```

### Version Control Best Practices

#### Branching Strategy

```
main (production)
  ↓
develop (staging)
  ↓
feature/smart-identification
feature/new-feature
```

#### Commit Messages

```
feat: Add Smart Identification feature
fix: Resolve JWT expiration issue
docs: Update deployment guide
chore: Update dependencies
refactor: Improve API client structure
```

#### Before Merging

```powershell
# Run tests
npm test
python -m pytest

# Check linting
npm run lint
flake8 backend/

# Build successfully
npm run build
docker build -t backend .
```

### Backup Strategy

#### Database Backups

**Automatic**:
- Daily at 3:00 AM (configured in Cloud SQL)
- 7-day retention

**Manual**:
```powershell
# Create backup
gcloud sql backups create --instance=leave-tracker-db

# Export to Cloud Storage
gcloud sql export sql leave-tracker-db gs://backup-bucket/backup.sql `
  --database=leavetracker
```

#### Code Backups

- Git repository (remote: GitHub)
- Local development backups
- Tagged releases for stable versions

### Disaster Recovery

#### Scenario 1: Database Corruption

```powershell
# List backups
gcloud sql backups list --instance=leave-tracker-db

# Restore from specific backup
gcloud sql backups restore BACKUP_ID `
  --backup-instance=leave-tracker-db
```

#### Scenario 2: Backend Service Down

```powershell
# Check status
gcloud run services describe leave-tracker-api

# Rollback to previous version
gcloud run services update-traffic leave-tracker-api `
  --to-revisions=PREVIOUS_REVISION=100
```

#### Scenario 3: Complete Project Loss

1. **Restore from Git**: Clone repository
2. **Restore Database**: From Cloud SQL backup
3. **Redeploy**: Run deployment script
4. **Verify**: Test all functionality

### Performance Optimization

#### Backend Optimization

- ✅ Add database indexes for frequently queried fields
- ✅ Implement caching for static data (people, types)
- ✅ Use connection pooling for database
- ✅ Optimize Gemini API calls (batch if possible)
- ✅ Enable gzip compression

#### Frontend Optimization

- ✅ Code splitting: `React.lazy()` for pages
- ✅ Image optimization: Compress assets
- ✅ CDN: Use Cloud CDN for Cloud Storage
- ✅ Lazy loading: Load components on demand
- ✅ Bundle analysis: `npm run build -- --analyze`

#### Database Optimization

```sql
-- Add indexes
CREATE INDEX idx_absences_person_id ON absences(person_id);
CREATE INDEX idx_absences_type_id ON absences(type_id);
CREATE INDEX idx_absences_date ON absences(date);

-- Vacuum database (PostgreSQL)
VACUUM ANALYZE;
```

### Monitoring Setup

#### Cloud Monitoring

```powershell
# Create uptime check
gcloud monitoring uptime-checks create https://your-api.run.app

# Create alert policy
gcloud alpha monitoring policies create --notification-channels=CHANNEL_ID
```

#### Custom Metrics

Add to backend:
```python
from prometheus_client import Counter, Histogram

request_count = Counter('api_requests_total', 'Total API requests')
request_duration = Histogram('api_request_duration_seconds', 'Request duration')
```

### Scaling Considerations

#### When to Scale

- Exceeding free tier limits
- Response time > 1 second
- CPU usage > 80%
- Memory usage > 80%

#### Scaling Options

**Cloud Run**:
```powershell
# Increase resources
gcloud run services update leave-tracker-api `
  --memory=1Gi `
  --cpu=2 `
  --min-instances=1 `
  --max-instances=10
```

**Cloud SQL**:
```powershell
# Upgrade to larger instance
gcloud sql instances patch leave-tracker-db `
  --tier=db-g1-small
```

---

## Appendix

### Quick Reference Commands

```powershell
# Local Development
cd backend; uvicorn app.main:app --reload
cd frontend; npm run dev

# Build
cd frontend; npm run build
docker build -t backend backend/

# Deploy Frontend
.\deploy-frontend.ps1

# Deploy Backend
gcloud builds submit backend --tag ...
gcloud run deploy leave-tracker-api --image ...

# View Logs
gcloud run services logs read leave-tracker-api --limit=50
gcloud run services logs tail leave-tracker-api

# Database
gcloud sql instances describe leave-tracker-db
gcloud sql connect leave-tracker-db --user=postgres

# Storage
gcloud storage ls gs://leave-tracker-2025-frontend/ --recursive
```

### Environment Variables Checklist

#### Backend
- [ ] `SECRET_KEY` - JWT signing key (32-byte hex)
- [ ] `DATABASE_URL` - Database connection string
- [ ] `CORS_ORIGINS` - Allowed frontend URLs
- [ ] `GEMINI_API_KEY` - Google Gemini API key (optional)
- [ ] `ALGORITHM` - JWT algorithm (default: HS256)
- [ ] `ACCESS_TOKEN_EXPIRE_MINUTES` - Token lifetime (default: 30)

#### Frontend
- [ ] `VITE_API_URL` - Backend API URL
- [ ] `VITE_ENABLE_REGISTRATION` - Enable/disable registration (default: false)

### Useful Links

- **Google Gemini API**: https://makersuite.google.com/app/apikey
- **Google Cloud Console**: https://console.cloud.google.com
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **React Docs**: https://react.dev
- **Material-UI**: https://mui.com
- **Vite**: https://vitejs.dev
- **Cloud Run**: https://cloud.google.com/run/docs
- **Cloud SQL**: https://cloud.google.com/sql/docs

### Support & Contribution

For issues, questions, or contributions:
1. Check this guide first
2. Review troubleshooting section
3. Check backend/frontend logs
4. Create GitHub issue with details

---

## Summary

This guide covers everything needed to understand, develop, and deploy the Leave Tracker application:

✅ **Architecture** - System design and data flow  
✅ **Setup** - Local development environment  
✅ **Features** - Detailed implementation docs  
✅ **Security** - Authentication and best practices  
✅ **API** - Complete endpoint reference  
✅ **Deployment** - Google Cloud step-by-step  
✅ **Configuration** - Environment variables and settings  
✅ **Troubleshooting** - Common issues and solutions  
✅ **Maintenance** - Updates, backups, monitoring  

**Current Status**:
- Backend: Deployed to Cloud Run (v1.1.0)
- Frontend: Deployed to Cloud Storage (v1.1.0)
- Database: Cloud SQL PostgreSQL (running)
- Smart Identification: Active (Gemini API configured)
- Registration: Disabled by default
- Cost: $0/month (all within free tier)

**Ready for Production** ✅

---

**Document Version**: 1.1.0  
**Last Updated**: November 2, 2025  
**Maintained By**: Development Team
