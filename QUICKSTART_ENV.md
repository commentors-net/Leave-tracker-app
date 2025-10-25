# 🚀 Quick Start - Environment Configuration

## ⚡ TL;DR - Get Started in 3 Minutes

### 1️⃣ Backend Setup (Required)
```bash
cd backend
cp .env.example .env
python -c "import secrets; print(secrets.token_hex(32))"
# Copy the output and paste it as SECRET_KEY value in .env
```

### 2️⃣ Frontend Setup (Optional - Already Configured for Dev)
```bash
# For development: No action needed!
# The .env.development file is already configured

# For production: Update the API URL
cd frontend
# Edit .env.production and change VITE_API_URL to your production backend URL
```

### 3️⃣ Launch (VS Code F5 or Manual)
```bash
# Option A: Press F5 in VS Code
# OR Option B: Manual launch
cd backend
uvicorn app.main:app --reload

# In another terminal
cd frontend
npm run dev
```

---

## 📋 Environment Files Checklist

### Backend Files:
- ✅ `backend/.env.example` - Template (already exists)
- ⚠️ `backend/.env` - **YOU NEED TO CREATE THIS**

### Frontend Files:
- ✅ `frontend/.env.development` - Dev config (already exists)
- ✅ `frontend/.env.production` - Prod template (already exists)
- ℹ️ `frontend/.env.production.local` - Optional prod override (create if needed)

---

## 🔑 Required Environment Variables

### Backend `.env` (REQUIRED)
```env
SECRET_KEY=<generate-with-python-command-above>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=sqlite:///./database.db
PORT=8000
HOST=0.0.0.0
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

### Frontend `.env.development` (Already configured)
```env
VITE_API_URL=http://localhost:8000
```

### Frontend `.env.production` (Update before deploying)
```env
VITE_API_URL=https://your-production-api.com
```

---

## 🔐 Security Checklist

Before deploying to production:

- [ ] Generated strong SECRET_KEY using Python secrets module
- [ ] Updated CORS_ORIGINS to only allow your production domain
- [ ] Changed DATABASE_URL if using PostgreSQL/MySQL
- [ ] Updated frontend .env.production with production API URL
- [ ] Verified .env files are NOT committed to git (check .gitignore)
- [ ] Backed up your database

---

## 🧪 Quick Test

Test if everything is configured correctly:

```bash
# Test backend environment loading
cd backend
python -c "from app.core.security import SECRET_KEY; print('✅ Backend config loaded' if len(SECRET_KEY) > 20 else '❌ SECRET_KEY not set')"

# Test frontend can connect to backend
cd frontend
npm run dev
# Open http://localhost:5173 and try to register/login
```

---

## 🆘 Common Issues

### ❌ Backend won't start
```bash
cd backend
pip install python-dotenv
# Make sure .env file exists
ls .env
```

### ❌ Frontend can't connect to backend
```bash
# Check backend is running
curl http://localhost:8000/docs

# Check frontend env file
cd frontend
cat .env.development
# Should show: VITE_API_URL=http://localhost:8000
```

### ❌ JWT authentication not working
```bash
# Verify SECRET_KEY is set
cd backend
grep SECRET_KEY .env
# Should show a long random string, not the placeholder
```

---

## 📚 Full Documentation

For detailed documentation, see:
- **[SETUP.md](./SETUP.md)** - Complete setup guide
- **[ENVIRONMENT_CONFIG.md](./ENVIRONMENT_CONFIG.md)** - In-depth configuration guide
- **[CONFIGURATION_SUMMARY.md](./CONFIGURATION_SUMMARY.md)** - Implementation details

---

## 🎯 Production Deployment Quick Guide

```bash
# 1. Generate production SECRET_KEY
python -c "import secrets; print(secrets.token_hex(32))"

# 2. Update backend .env with production values
cd backend
nano .env  # Update SECRET_KEY, DATABASE_URL, CORS_ORIGINS

# 3. Update frontend production URL
cd frontend
nano .env.production  # Set VITE_API_URL to production backend

# 4. Build for production
npm run build:prod

# 5. Deploy
# Backend: docker build -t leave-tracker-backend .
# Frontend: Copy dist/ folder to your hosting (Vercel, Netlify, etc.)
```

---

## ✅ You're All Set!

Once you've completed step 1 (backend .env setup), you can launch the app with **F5** in VS Code or manually start both services. Happy coding! 🎉

For questions or issues, refer to the troubleshooting section in **ENVIRONMENT_CONFIG.md**.
