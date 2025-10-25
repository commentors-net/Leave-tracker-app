# Environment Configuration Guide

This document explains how to configure the Leave Tracker application for different environments.

## Overview

The application uses environment variables to configure:
- Backend API settings (JWT tokens, database, CORS)
- Frontend API endpoints
- Security credentials

## Quick Start

### Development Setup

1. **Backend:**
   ```bash
   cd backend
   cp .env.example .env
   # Generate a secure secret key
   python -c "import secrets; print(secrets.token_hex(32))"
   # Update SECRET_KEY in .env with the generated value
   ```

2. **Frontend:**
   - No action needed - `.env.development` is pre-configured

3. **Start the application:**
   - Press F5 in VS Code to launch both backend and frontend

### Production Setup

1. **Backend:**
   ```bash
   cd backend
   cp .env.example .env
   # Update all values for production
   # Use strong SECRET_KEY
   # Set production DATABASE_URL if using PostgreSQL/MySQL
   # Configure CORS_ORIGINS with your frontend domain
   ```

2. **Frontend:**
   ```bash
   cd frontend
   cp .env.production .env.production.local
   # Update VITE_API_URL with your production backend URL
   ```

3. **Build and deploy:**
   ```bash
   # Backend
   cd backend
   docker build -t leave-tracker-backend .
   
   # Frontend
   cd frontend
   npm run build:prod
   ```

## Backend Environment Variables

### JWT Configuration

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `SECRET_KEY` | string | (example value) | **REQUIRED** - Secret key for signing JWT tokens. Must be a strong random value. Generate with: `python -c "import secrets; print(secrets.token_hex(32))"` |
| `ALGORITHM` | string | HS256 | JWT signing algorithm. Supported: HS256, HS384, HS512 |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | integer | 30 | Token expiration time in minutes |

### Database Configuration

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `DATABASE_URL` | string | sqlite:///./database.db | Database connection URL. Examples:<br>- SQLite: `sqlite:///./database.db`<br>- PostgreSQL: `postgresql://user:pass@localhost/dbname`<br>- MySQL: `mysql://user:pass@localhost/dbname` |

### Server Configuration

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `PORT` | integer | 8000 | Port number for the backend server |
| `HOST` | string | 0.0.0.0 | Host address to bind to. Use `0.0.0.0` for all interfaces |

### CORS Configuration

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `CORS_ORIGINS` | string | http://localhost:5173,http://localhost:3000 | Comma-separated list of allowed origins. Examples:<br>- Development: `http://localhost:5173`<br>- Production: `https://yourdomain.com,https://www.yourdomain.com` |

## Frontend Environment Variables

### Development

File: `.env.development`

```env
VITE_API_URL=http://localhost:8000
```

This file is committed to git and used automatically in development mode.

### Production

File: `.env.production`

```env
VITE_API_URL=https://your-production-api.com
```

Update this with your actual production backend URL before building.

### Local Override

File: `.env.local` or `.env.production.local`

These files override the default values and are **not** committed to git (excluded in `.gitignore`).

## Configuration Files Reference

### Backend Files

```
backend/
├── .env.example          # Template file (committed to git)
├── .env                  # Your actual config (NOT committed)
└── app/
    ├── database.py       # Reads DATABASE_URL
    ├── main.py           # Reads CORS_ORIGINS
    └── core/
        └── security.py   # Reads SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
```

### Frontend Files

```
frontend/
├── .env.development      # Development config (committed)
├── .env.production       # Production template (committed)
├── .env.local           # Local override (NOT committed)
├── .env.production.local # Production override (NOT committed)
└── src/
    └── config.ts        # Reads VITE_API_URL and exports config object
```

## Environment Detection

### Backend

Python's `python-dotenv` automatically loads `.env` from the backend directory:

```python
from dotenv import load_dotenv
import os

load_dotenv()  # Loads .env file
SECRET_KEY = os.getenv("SECRET_KEY", "default-value")
```

### Frontend

Vite automatically loads environment files based on mode:

- `npm run dev` → loads `.env.development`
- `npm run build` → loads `.env.production`
- `npm run build:prod` → loads `.env.production` with production optimizations

Access in code:
```typescript
const apiUrl = import.meta.env.VITE_API_URL;
```

## Security Best Practices

### 🔒 Secret Key Management

1. **Generate Strong Keys:**
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

2. **Never Commit Secrets:**
   - Use `.env` files (excluded in `.gitignore`)
   - Use `.env.example` files as templates (committed to git)

3. **Rotate Keys Regularly:**
   - Change `SECRET_KEY` periodically in production
   - Update all active sessions will be invalidated

### 🔒 Database Security

1. **Development:** SQLite is fine
2. **Production:** Use PostgreSQL or MySQL with:
   - Strong passwords
   - SSL/TLS connections
   - Regular backups
   - Restricted network access

### 🔒 CORS Configuration

1. **Development:** Allow `localhost:5173`
2. **Production:** 
   - Only allow your specific domains
   - Never use `*` (allow all)
   - Include both `https://example.com` and `https://www.example.com` if needed

## Deployment Scenarios

### Local Development

```bash
# Backend: .env
SECRET_KEY=abc123...
DATABASE_URL=sqlite:///./database.db
CORS_ORIGINS=http://localhost:5173

# Frontend: .env.development (default)
VITE_API_URL=http://localhost:8000
```

### Docker Compose

```yaml
version: '3.8'
services:
  backend:
    build: ./backend
    environment:
      - SECRET_KEY=${SECRET_KEY}
      - DATABASE_URL=${DATABASE_URL}
      - CORS_ORIGINS=${CORS_ORIGINS}
    env_file:
      - ./backend/.env
      
  frontend:
    build: ./frontend
    environment:
      - VITE_API_URL=http://backend:8000
```

### Google Cloud Run

1. **Backend:**
   ```bash
   gcloud run deploy leave-tracker-api \
     --image gcr.io/PROJECT_ID/leave-tracker-backend \
     --set-env-vars="SECRET_KEY=...,DATABASE_URL=..." \
     --set-secrets="SECRET_KEY=leave-tracker-secret:latest"
   ```

2. **Frontend:**
   ```bash
   # Build with production config
   VITE_API_URL=https://api.example.com npm run build:prod
   # Deploy to Cloud Storage + Cloud CDN
   ```

### Kubernetes

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: leave-tracker-secrets
type: Opaque
stringData:
  SECRET_KEY: "your-secret-key"
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: leave-tracker-backend
spec:
  template:
    spec:
      containers:
      - name: backend
        image: leave-tracker-backend:latest
        env:
        - name: SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: leave-tracker-secrets
              key: SECRET_KEY
```

## Troubleshooting

### Issue: Frontend can't connect to backend

**Check:**
1. Frontend `.env` file has correct `VITE_API_URL`
2. Backend CORS allows the frontend origin
3. Backend is actually running and accessible
4. Network/firewall allows the connection

**Solution:**
```bash
# Test backend directly
curl http://localhost:8000/docs

# Check frontend config
cd frontend
cat .env.development

# Check backend CORS
cd backend
grep CORS_ORIGINS .env
```

### Issue: JWT tokens not working

**Check:**
1. `SECRET_KEY` is set in backend `.env`
2. `SECRET_KEY` hasn't changed (invalidates all tokens)
3. Token hasn't expired (check `ACCESS_TOKEN_EXPIRE_MINUTES`)

**Solution:**
```bash
# Verify backend is using the .env file
cd backend
cat .env | grep SECRET_KEY

# Check if python-dotenv is installed
pip list | grep python-dotenv
```

### Issue: Database not found

**Check:**
1. `DATABASE_URL` in backend `.env`
2. Database file exists (for SQLite)
3. Database permissions (for PostgreSQL/MySQL)

**Solution:**
```bash
# Check database config
cd backend
cat .env | grep DATABASE_URL

# For SQLite, check if file exists
ls -la database.db

# Recreate database
rm database.db
python -c "from app.database import engine; from app.models import Base; Base.metadata.create_all(bind=engine)"
```

## Migration Guide

### From Hardcoded Values to Environment Variables

If you're updating from an older version:

1. **Install python-dotenv:**
   ```bash
   cd backend
   pip install python-dotenv
   ```

2. **Create .env files:**
   ```bash
   cd backend
   cp .env.example .env
   # Update values
   
   cd ../frontend
   # .env.development already exists
   ```

3. **Test the changes:**
   ```bash
   # Stop all running services
   # Press F5 in VS Code to restart with new config
   ```

4. **Verify:**
   - Backend starts successfully
   - Frontend can connect to backend
   - Login/registration works
   - API calls succeed

## Additional Resources

- [python-dotenv documentation](https://pypi.org/project/python-dotenv/)
- [Vite environment variables](https://vitejs.dev/guide/env-and-mode.html)
- [FastAPI settings management](https://fastapi.tiangolo.com/advanced/settings/)
- [JWT best practices](https://tools.ietf.org/html/rfc8725)
