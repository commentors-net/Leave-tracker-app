# 🚀 Deployment Guide - Leave Tracker Application

This guide will help you deploy the Leave Tracker application to Google Cloud Platform (GCP).

## 📋 Prerequisites

### 1. Google Cloud Account
- Sign up for GCP: https://cloud.google.com/
- Free tier includes: $300 credit for 90 days + Always Free resources

### 2. Install Required Tools
- **Google Cloud SDK**: https://cloud.google.com/sdk/docs/install
- **Docker Desktop**: https://www.docker.com/products/docker-desktop
- **Node.js 18+**: Already installed ✓
- **PowerShell**: Already available on Windows ✓

### 3. GCP Project Setup
```powershell
# Login to Google Cloud
gcloud auth login

# Create a new project (or use existing one)
gcloud projects create leave-tracker-2025 --name="Leave Tracker"

# Set as active project
gcloud config set project leave-tracker-2025

# Enable billing (required even for free tier)
# Go to: https://console.cloud.google.com/billing
# Link your project to a billing account
```

### 4. Required Information
Before running the deployment script, prepare:
- ✅ **Project ID**: Your GCP project ID (e.g., `leave-tracker-2025`)
- ✅ **Secret Key**: A random string for JWT tokens (32+ characters)
- ✅ **Database Password**: Strong password for PostgreSQL (12+ characters)
- ✅ **Gemini API Key**: Your Google Gemini API key from https://aistudio.google.com/apikey
- ✅ **Region**: Default is `us-central1` (or choose closer to you)

## 🔑 Get Your Gemini API Key

1. Visit: https://aistudio.google.com/apikey
2. Click "Create API Key"
3. Select your project or create a new one
4. Copy the API key (starts with `AIza...`)

## 🚀 Deployment Steps

### Option 1: Full Deployment (First Time)

Run the comprehensive deployment script:

```powershell
# Navigate to project root
cd d:\Jobs\workspace\python-projects\Leave-tracker-app

# Run deployment (replace with your values)
.\deploy-to-gcp-complete.ps1 `
    -ProjectId "leave-tracker-2025" `
    -SecretKey "your-super-secret-key-min-32-chars-long" `
    -DbPassword "your-database-password-12-chars" `
    -GeminiApiKey "AIzaSyCvOLSVY8uwDkDKwjBrVROXzwyBo1RfZhk" `
    -Region "us-central1"
```

**This script will:**
1. ✅ Enable required GCP APIs
2. ✅ Create Artifact Registry for Docker images
3. ✅ Build and push backend Docker image
4. ✅ Create Cloud SQL PostgreSQL database
5. ✅ Run database migrations (including new 'applied' column)
6. ✅ Deploy backend to Cloud Run
7. ✅ Build frontend with production config
8. ✅ Deploy frontend to Cloud Storage
9. ✅ Configure CORS settings
10. ✅ Output all URLs and next steps

**Estimated time**: 10-15 minutes (Cloud SQL creation takes ~5 mins)

### Option 2: Update Existing Deployment

If you've already deployed and just need to update:

**Update Backend Only:**
```powershell
.\deploy-backend-only.ps1 -ProjectId "leave-tracker-2025"
```

**Update Frontend Only:**
```powershell
.\deploy-frontend.ps1
```

## 📊 Post-Deployment

### 1. Access Your Application
After deployment completes, you'll see:
```
Frontend:  https://storage.googleapis.com/leave-tracker-2025-frontend/index.html
Backend:   https://leave-tracker-api-xxxxx-uc.a.run.app
API Docs:  https://leave-tracker-api-xxxxx-uc.a.run.app/docs
```

### 2. Register First User
1. Visit the frontend URL
2. Click "Register" (if enabled in config)
3. Scan QR code with Google Authenticator app
4. Login with username, password, and TOTP token

### 3. Setup Initial Data
1. Go to **Settings** → Add people and leave types
2. Go to **Dashboard** → Log some test absences
3. Go to **Smart Identification** → Test AI parsing
4. Go to **Reports** → View and manage all records

## 🔧 Configuration

### Environment Variables (Backend)
Set in Cloud Run:
```
SECRET_KEY=<your-secret-key>
DATABASE_URL=postgresql://postgres:<password>@/leavetracker?host=/cloudsql/<connection>
GEMINI_API_KEY=<your-gemini-key>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
CORS_ORIGINS=https://storage.googleapis.com/<bucket-name>
```

### Frontend Configuration
Edit `frontend/.env.production`:
```
VITE_API_URL=https://leave-tracker-api-xxxxx-uc.a.run.app
VITE_ENABLE_REGISTRATION=true
```

## 💰 Cost Estimate (Free Tier)

### Always Free Resources:
- **Cloud Run**: 2 million requests/month
- **Cloud SQL**: db-f1-micro (shared core, 0.6 GB RAM)
- **Cloud Storage**: 5 GB storage, 1 GB network egress/month
- **Artifact Registry**: 0.5 GB storage

### Expected Monthly Cost:
- **Free Tier Usage**: $0 (within free limits)
- **If exceeding free tier**: ~$10-20/month for small usage

## 📝 Monitoring & Logs

### View Backend Logs:
```powershell
gcloud run services logs tail leave-tracker-api --region=us-central1
```

### View Database:
```powershell
# Connect via Cloud Shell
gcloud sql connect leave-tracker-db --user=postgres

# Inside PostgreSQL:
\c leavetracker
\dt
SELECT * FROM absences;
```

### Check Service Status:
```powershell
gcloud run services describe leave-tracker-api --region=us-central1
```

## 🔄 Update Application

### Update Backend Code:
1. Make changes to backend code
2. Run: `.\deploy-backend-only.ps1 -ProjectId "leave-tracker-2025"`
3. Wait ~2-3 minutes for deployment

### Update Frontend Code:
1. Make changes to frontend code
2. Run: `.\deploy-frontend.ps1`
3. Clear browser cache or use incognito to see changes

### Run New Migrations:
```powershell
# SSH into Cloud Run (not recommended for production)
# Better: Run migrations during deployment

# Or connect to Cloud SQL and run manually:
gcloud sql connect leave-tracker-db --user=postgres
\c leavetracker
ALTER TABLE absences ADD COLUMN new_column_name TYPE;
```

## 🛡️ Security Best Practices

1. **Never commit secrets** to git
   - Use environment variables
   - Add `.env` to `.gitignore` ✓

2. **Use strong passwords**
   - Database: 16+ characters
   - Secret Key: 32+ characters
   - User passwords: 8+ characters

3. **Enable 2FA** (already implemented via TOTP)

4. **Keep dependencies updated**
   ```powershell
   cd backend
   pip list --outdated
   ```

5. **Monitor API usage**
   - Check Gemini API quota: https://aistudio.google.com/
   - Check Cloud Run usage: GCP Console

## 🐛 Troubleshooting

### Backend Won't Deploy
```powershell
# Check Docker build locally
cd backend
docker build -t test-backend .
docker run -p 8080:8080 test-backend

# Check logs
gcloud run services logs tail leave-tracker-api --region=us-central1
```

### Frontend Not Loading
```powershell
# Verify bucket contents
gsutil ls gs://leave-tracker-2025-frontend/

# Make bucket public
gsutil iam ch allUsers:objectViewer gs://leave-tracker-2025-frontend
```

### Database Connection Issues
```powershell
# Test connection
gcloud sql connect leave-tracker-db --user=postgres

# Check Cloud SQL instances
gcloud sql instances list
```

### CORS Errors
```powershell
# Update CORS settings
gcloud run services update leave-tracker-api \
  --region=us-central1 \
  --update-env-vars="CORS_ORIGINS=https://storage.googleapis.com/leave-tracker-2025-frontend"
```

### Gemini API Not Working
1. Check API key is set: `gcloud run services describe leave-tracker-api --region=us-central1 --format="value(spec.template.spec.containers[0].env)"`
2. Verify quota: https://aistudio.google.com/
3. Check logs for errors

## 📱 Custom Domain (Optional)

To use your own domain:

1. **Register domain** (e.g., via Google Domains)

2. **Map Cloud Run service:**
   ```powershell
   gcloud run domain-mappings create \
     --service=leave-tracker-api \
     --domain=api.yourdomain.com \
     --region=us-central1
   ```

3. **Configure frontend bucket with Load Balancer**
   - Follow: https://cloud.google.com/storage/docs/hosting-static-website

4. **Update CORS** with new domain

## 🔄 Backup & Recovery

### Backup Database:
```powershell
gcloud sql export sql leave-tracker-db \
  gs://leave-tracker-2025-backups/backup-$(Get-Date -Format yyyy-MM-dd).sql \
  --database=leavetracker
```

### Restore Database:
```powershell
gcloud sql import sql leave-tracker-db \
  gs://leave-tracker-2025-backups/backup-2025-11-02.sql \
  --database=leavetracker
```

## 📞 Support

- **GCP Documentation**: https://cloud.google.com/docs
- **Cloud Run Docs**: https://cloud.google.com/run/docs
- **Gemini API Docs**: https://ai.google.dev/docs

## ✅ Deployment Checklist

Before deployment:
- [ ] GCP account created and billing enabled
- [ ] gcloud CLI installed and authenticated
- [ ] Docker Desktop running
- [ ] Project ID chosen
- [ ] Secret key generated (32+ chars)
- [ ] Database password generated (12+ chars)
- [ ] Gemini API key obtained
- [ ] Region selected

After deployment:
- [ ] Frontend URL accessible
- [ ] Backend health check passes (`/docs`)
- [ ] First user registered
- [ ] 2FA configured
- [ ] Test data added
- [ ] Smart Identification working
- [ ] Reports page functional

## 🎉 Success!

Your Leave Tracker application is now live in the cloud!

**Next Steps:**
1. Share the frontend URL with your team
2. Have each person register and setup 2FA
3. Start tracking leaves!

---

**Need help?** Check troubleshooting section or GCP documentation.
