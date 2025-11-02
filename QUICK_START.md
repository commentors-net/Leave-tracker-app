# 🚀 QUICK START - Deploy to Cloud in 5 Minutes

## Prerequisites Check ✅

Before starting, make sure you have:

1. **Google Cloud Account** 
   - Sign up: https://cloud.google.com/ (Free $300 credit)

2. **Install Google Cloud SDK**
   ```powershell
   # Download and install from: https://cloud.google.com/sdk/docs/install
   # After install, restart PowerShell and verify:
   gcloud --version
   ```

3. **Install Docker Desktop**
   ```powershell
   # Download from: https://www.docker.com/products/docker-desktop
   # Start Docker Desktop before deployment
   ```

4. **Login to Google Cloud**
   ```powershell
   gcloud auth login
   # This will open a browser for authentication
   ```

## Step 1: Generate Secure Keys 🔐

```powershell
cd d:\Jobs\workspace\python-projects\Leave-tracker-app
.\generate-keys.ps1
```

This will generate:
- ✅ Secret Key (32 characters) - for JWT tokens
- ✅ Database Password (16 characters) - for PostgreSQL

**IMPORTANT:** Copy and save these keys securely!

## Step 2: Get Gemini API Key 🤖

1. Visit: https://aistudio.google.com/apikey
2. Click "Create API Key"
3. Select your project (or create new one)
4. Copy the API key (starts with `AIza...`)

## Step 3: Create GCP Project 📋

```powershell
# Option 1: Create via command line
gcloud projects create leave-tracker-2025 --name="Leave Tracker"

# Option 2: Create via web console
# Visit: https://console.cloud.google.com/projectcreate
```

**IMPORTANT:** Enable billing for your project
- Visit: https://console.cloud.google.com/billing
- Link your project to a billing account (required even for free tier)

## Step 4: Deploy Everything 🚀

```powershell
cd d:\Jobs\workspace\python-projects\Leave-tracker-app

.\deploy-to-gcp-complete.ps1 `
    -ProjectId "leave-tracker-2025" `
    -SecretKey "YOUR_SECRET_KEY_FROM_STEP_1" `
    -DbPassword "YOUR_DB_PASSWORD_FROM_STEP_1" `
    -GeminiApiKey "YOUR_GEMINI_API_KEY_FROM_STEP_2"
```

**What this does:**
1. ✅ Enables required GCP APIs
2. ✅ Creates Docker container registry
3. ✅ Builds and uploads backend image
4. ✅ Creates PostgreSQL database (~5 minutes)
5. ✅ Deploys backend to Cloud Run
6. ✅ Builds frontend with production config
7. ✅ Deploys frontend to Cloud Storage
8. ✅ Configures CORS and permissions

**Total time:** ~10-15 minutes (mostly waiting for database creation)

## Step 5: Access Your App 🌐

After deployment completes, you'll see:

```
Frontend:  https://storage.googleapis.com/leave-tracker-2025-frontend/index.html
Backend:   https://leave-tracker-api-xxxxx-uc.a.run.app
```

### First Time Setup:

1. **Visit the frontend URL**
   - Click "Register" to create your account
   
2. **Setup 2FA**
   - Scan the QR code with Google Authenticator app
   - Save your backup code securely
   
3. **Login**
   - Enter username, password, and 6-digit TOTP code
   
4. **Configure Settings**
   - Go to Settings → People tab
   - Add team members (e.g., John, Sarah, Mike)
   - Go to Types tab
   - Add leave types (e.g., Annual, Sick, WFH)
   
5. **Test Features**
   - Dashboard: Log a test absence
   - Reports: View and manage records
   - Smart Identification: Try AI conversation parsing
   - Settings: Customize AI instructions

## Quick Commands 📝

### View Backend Logs:
```powershell
gcloud run services logs tail leave-tracker-api --region=us-central1
```

### Update Backend Only:
```powershell
.\deploy-backend-only.ps1 -ProjectId "leave-tracker-2025"
```

### Update Frontend Only:
```powershell
.\deploy-frontend.ps1
```

### Check Service Status:
```powershell
gcloud run services describe leave-tracker-api --region=us-central1
```

### Connect to Database:
```powershell
gcloud sql connect leave-tracker-db --user=postgres
# Enter your database password when prompted
```

## Cost Estimate 💰

**Free Tier Includes:**
- Cloud Run: 2M requests/month
- Cloud SQL: db-f1-micro instance
- Cloud Storage: 5 GB storage
- Artifact Registry: 0.5 GB

**Expected Cost:**
- Within free tier limits: **$0/month**
- Small team usage (10-50 users): **$5-15/month**

## Troubleshooting 🔧

### Docker Build Fails:
```powershell
# Make sure Docker Desktop is running
# Check Docker:
docker --version
docker ps
```

### Project Not Found:
```powershell
# List your projects:
gcloud projects list

# Set correct project:
gcloud config set project YOUR_PROJECT_ID
```

### Permission Denied:
```powershell
# Re-authenticate:
gcloud auth login
gcloud auth application-default login
```

### Frontend Not Loading:
```powershell
# Make bucket public:
gsutil iam ch allUsers:objectViewer gs://leave-tracker-2025-frontend

# Verify files:
gsutil ls gs://leave-tracker-2025-frontend/
```

### Gemini API Not Working:
- Verify API key in Cloud Run: Check environment variables
- Check quota: Visit https://aistudio.google.com/
- View errors in logs: `gcloud run services logs tail leave-tracker-api`

## Update Your App 🔄

### After Code Changes:

**Backend:**
```powershell
.\deploy-backend-only.ps1 -ProjectId "leave-tracker-2025"
```

**Frontend:**
```powershell
.\deploy-frontend.ps1
```

**Both:**
```powershell
.\deploy-to-gcp-complete.ps1 -ProjectId "..." -SecretKey "..." -DbPassword "..." -GeminiApiKey "..."
```

## Need Help? 📚

- **Full Documentation:** See `DEPLOYMENT_GUIDE.md`
- **GCP Console:** https://console.cloud.google.com/
- **Cloud Run Docs:** https://cloud.google.com/run/docs
- **Support:** Check GCP documentation or Stack Overflow

## Success! 🎉

Your Leave Tracker is now running in the cloud!

**Share with your team:**
- Send them the frontend URL
- They can register and setup their own 2FA
- Start tracking leaves together!

**Remember:**
- ✅ Data is stored in Cloud SQL (backed up automatically)
- ✅ Application scales automatically with usage
- ✅ 2FA keeps accounts secure
- ✅ Free tier covers most small team usage

Happy tracking! 🚀
