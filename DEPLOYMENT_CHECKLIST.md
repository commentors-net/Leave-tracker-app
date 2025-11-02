# 🚀 Google Cloud Deployment Checklist

## Pre-Deployment Checklist

### ✅ System Requirements
- [ ] **Windows PowerShell** (or equivalent terminal)
- [ ] **gcloud CLI installed** - [Install](https://cloud.google.com/sdk/docs/install)
  ```powershell
  gcloud version
  # Should show: Google Cloud SDK 400+
  ```
- [ ] **Docker Desktop installed and running** - [Install](https://www.docker.com/products/docker-desktop)
  ```powershell
  docker version
  # Should show: Docker version 20+
  ```
- [ ] **Python 3.11+** installed
  ```powershell
  python --version
  # Should show: Python 3.11.x
  ```
- [ ] **Node.js 22+ and npm 11+** installed
  ```powershell
  node --version  # Should show: v22.x
  npm --version   # Should show: 11.x
  ```

### ✅ Google Cloud Account Setup
- [ ] **Google Cloud account created** - [Sign Up](https://console.cloud.google.com)
- [ ] **Billing enabled** (required even for free tier)
  - Navigate to: [Billing](https://console.cloud.google.com/billing)
  - Add payment method (won't charge if staying in free tier)
- [ ] **Budget alert configured** (recommended)
  - Set budget: $5/month
  - Set alerts at: 50%, 90%, 100%

### ✅ Authentication
- [ ] **Login to gcloud**
  ```powershell
  gcloud auth login
  # Opens browser for authentication
  ```
- [ ] **Verify login**
  ```powershell
  gcloud auth list
  # Should show your email with * (active)
  ```

### ✅ Generate Secrets
- [ ] **Generate JWT SECRET_KEY**
  ```powershell
  python -c "import secrets; print(secrets.token_hex(32))"
  # Save this output! Example: 965be4012f77a327c290d96c6c9a7b87624728af7b381893c306ce5bb4ce0e57
  ```
- [ ] **Create database password**
  - Use strong password with: letters, numbers, symbols
  - Example: `MySecureDb2025!@#$`
  - **Save this password securely!**

### ✅ Code Ready
- [ ] All code changes committed to git
- [ ] Backend `.env.example` exists
- [ ] Frontend `.env.development` and `.env.production` templates exist
- [ ] `deploy-to-gcp.ps1` script exists in project root
- [ ] `backend/Dockerfile` exists

---

## 🚀 Deployment Steps

### Step 1: Navigate to Project Root
```powershell
cd d:\Jobs\workspace\python-projects\Leave-tracker-app
```

### Step 2: Choose Project ID
- [ ] **Decide on a unique project ID**
  - Must be globally unique across all Google Cloud
  - 6-30 characters, lowercase letters, numbers, hyphens
  - Example: `leave-tracker-2025`
  - Cannot be changed later!

### Step 3: Run Deployment Script
```powershell
.\deploy-to-gcp.ps1 `
    -ProjectId "leave-tracker-2025" `
    -SecretKey "your-generated-secret-key-from-above" `
    -DbPassword "your-secure-database-password"
```

**What the script does**:
1. ⏱️ **1 min**: Creates project and enables APIs
2. ⏱️ **1 min**: Sets up Artifact Registry
3. ⏱️ **2 min**: Builds and pushes backend Docker image
4. ⏱️ **5 min**: Creates Cloud SQL database
5. ⏱️ **2 min**: Deploys backend to Cloud Run
6. ⏱️ **2 min**: Builds and deploys frontend
7. ⏱️ **1 min**: Configures CORS and networking

**Total time**: ~10-15 minutes

### Step 4: Save URLs
After deployment completes, save these URLs:

- [ ] **Frontend URL**: `https://storage.googleapis.com/<project-id>-frontend/index.html`
- [ ] **Backend URL**: `https://leave-tracker-api-xxxxx-uc.a.run.app`
- [ ] **API Docs**: `https://leave-tracker-api-xxxxx-uc.a.run.app/docs`

---

## 🧪 Post-Deployment Testing

### Test 1: Backend Health Check
```powershell
# Test backend is accessible
curl https://leave-tracker-api-xxxxx-uc.a.run.app/docs
# Should return HTML for FastAPI Swagger UI
```
- [ ] Backend API docs load successfully

### Test 2: Frontend Access
- [ ] Open frontend URL in browser
- [ ] Page loads without errors
- [ ] Login and Register buttons visible

### Test 3: Registration Flow
- [ ] Click "Register" button
- [ ] Enter username and password
- [ ] QR code displays
- [ ] Scan QR code with Google Authenticator app
- [ ] "Continue to Login" redirects to login page

### Test 4: Login Flow
- [ ] Enter registered username and password
- [ ] Enter 6-digit 2FA code from authenticator
- [ ] Login successful
- [ ] Redirected to Dashboard
- [ ] Navigation shows "Welcome, [username]"

### Test 5: JWT Token Verification
- [ ] Open browser DevTools (F12)
- [ ] Go to Application → Local Storage
- [ ] Verify `access_token` exists
- [ ] Go to Network tab
- [ ] Load Dashboard
- [ ] Check request headers
- [ ] Verify `Authorization: Bearer <token>` header present

### Test 6: Dashboard Functionality
- [ ] People dropdown loads data
- [ ] Leave Types dropdown loads data
- [ ] Select person, date, duration, type
- [ ] Enter reason
- [ ] Click Submit
- [ ] Success message appears
- [ ] Form clears after submission

### Test 7: Settings - People Management
- [ ] Navigate to Settings
- [ ] Click "People" tab
- [ ] Add new person
- [ ] Person appears in list
- [ ] Edit person name
- [ ] Delete person
- [ ] Verify changes in Dashboard dropdown

### Test 8: Settings - Leave Types Management
- [ ] Click "Leave Types" tab
- [ ] Add new type (e.g., "Sick Leave")
- [ ] Type appears in list
- [ ] Edit type name
- [ ] Delete type
- [ ] Verify changes in Dashboard dropdown

### Test 9: Logout
- [ ] Click Logout button
- [ ] Redirected to Login page
- [ ] Navigation updated (shows Login/Register)
- [ ] Check localStorage - `access_token` removed

### Test 10: JWT Expiration (Optional)
- [ ] Login successfully
- [ ] Wait 30 minutes (token expiration)
- [ ] Try to load Dashboard
- [ ] Should redirect to Login or show error
- [ ] Re-login works successfully

---

## 📊 Monitoring Setup

### Configure Logging
```powershell
# View real-time logs
gcloud run services logs tail leave-tracker-api --region=us-central1

# View recent logs
gcloud run services logs read leave-tracker-api --region=us-central1 --limit=50
```

- [ ] Logs accessible and readable
- [ ] No error messages in logs

### Setup Alerts (Recommended)
1. [ ] Navigate to [Cloud Console - Alerting](https://console.cloud.google.com/monitoring/alerting)
2. [ ] Create alert for Cloud Run errors
3. [ ] Create alert for Cloud SQL connection failures
4. [ ] Create alert for high latency (>1s)
5. [ ] Add email notification

### Monitor Costs
1. [ ] Navigate to [Billing Reports](https://console.cloud.google.com/billing/reports)
2. [ ] Verify current charges are $0
3. [ ] Check daily usage
4. [ ] Confirm staying within free tier

---

## 🔐 Security Hardening

### Post-Deployment Security Checklist
- [ ] **CORS configured** with exact frontend URL (not wildcard)
  ```powershell
  gcloud run services describe leave-tracker-api --format='value(spec.template.spec.containers[0].env)'
  # Check CORS_ORIGINS is set correctly
  ```
- [ ] **SECRET_KEY is unique** (not example value)
- [ ] **Database password is strong** (12+ characters, mixed case, numbers, symbols)
- [ ] **Environment variables not in git** (check `.gitignore`)
- [ ] **Budget alerts configured** ($5/month limit)
- [ ] **Cloud SQL private** (only Cloud Run can connect)

### Optional: Enable Additional Security
```powershell
# Enable Cloud Armor (DDoS protection)
gcloud compute security-policies create leave-tracker-policy

# Add rule to block SQL injection
gcloud compute security-policies rules create 1000 \
  --security-policy=leave-tracker-policy \
  --expression="evaluatePreconfiguredExpr('sqli-stable')" \
  --action=deny-403

# Add rule to block XSS
gcloud compute security-policies rules create 1001 \
  --security-policy=leave-tracker-policy \
  --expression="evaluatePreconfiguredExpr('xss-stable')" \
  --action=deny-403
```

---

## 🔄 Updating Your Deployment

### Deploy Code Updates
```powershell
# Make code changes
git add .
git commit -m "Updated feature X"

# Redeploy with new version
.\deploy-to-gcp.ps1 `
    -ProjectId "leave-tracker-2025" `
    -SecretKey "same-secret-as-before" `
    -DbPassword "same-password-as-before" `
    -Version "v1.0.1"
```

- [ ] New version deployed successfully
- [ ] Frontend shows updated changes
- [ ] Backend API updated
- [ ] No breaking changes

### Update Environment Variables
```powershell
# Update a single environment variable
gcloud run services update leave-tracker-api \
  --region=us-central1 \
  --update-env-vars="VARIABLE_NAME=new_value"
```

### Rollback to Previous Version
```powershell
# List revisions
gcloud run revisions list --service=leave-tracker-api --region=us-central1

# Rollback to previous revision
gcloud run services update-traffic leave-tracker-api \
  --to-revisions=leave-tracker-api-00002-abc=100 \
  --region=us-central1
```

---

## 🐛 Troubleshooting Guide

### Issue: Script Fails at API Enablement
**Solution**:
```powershell
# Manually enable APIs
gcloud services enable run.googleapis.com
gcloud services enable sqladmin.googleapis.com
gcloud services enable artifactregistry.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable storage-api.googleapis.com

# Retry deployment
```

### Issue: Docker Build Fails
**Solution**:
```powershell
# Check Docker is running
docker ps
# If error, start Docker Desktop

# Re-authenticate Docker
gcloud auth configure-docker us-central1-docker.pkg.dev

# Retry deployment
```

### Issue: Cloud SQL Creation Times Out
**Solution**:
```powershell
# Check if instance exists
gcloud sql instances list

# If partially created, delete and retry
gcloud sql instances delete leave-tracker-db
# Then run deployment script again
```

### Issue: Frontend Shows 404
**Solution**:
```powershell
# Check bucket exists
gsutil ls gs://leave-tracker-2025-frontend

# Re-upload frontend
cd frontend
npm run build:prod
gsutil -m rsync -r dist/ gs://leave-tracker-2025-frontend/
gsutil web set -m index.html -e index.html gs://leave-tracker-2025-frontend
```

### Issue: CORS Errors in Browser
**Solution**:
```powershell
# Get exact frontend URL
echo "https://storage.googleapis.com/leave-tracker-2025-frontend"

# Update CORS with exact URL (no trailing slash, no /index.html)
gcloud run services update leave-tracker-api \
  --region=us-central1 \
  --update-env-vars="CORS_ORIGINS=https://storage.googleapis.com/leave-tracker-2025-frontend"
```

### Issue: Database Connection Fails
**Solution**:
```powershell
# Check Cloud SQL connection name
gcloud sql instances describe leave-tracker-db --format='value(connectionName)'

# Verify Cloud Run has Cloud SQL connection
gcloud run services describe leave-tracker-api --format='value(spec.template.metadata.annotations."run.googleapis.com/cloudsql-instances")'

# If missing, update service
gcloud run services update leave-tracker-api \
  --region=us-central1 \
  --set-cloudsql-instances=<connection-name>
```

---

## 🧹 Cleanup (Delete Everything)

### If You Want to Start Over or Delete Project

```powershell
# Delete Cloud Run service
gcloud run services delete leave-tracker-api --region=us-central1 --quiet

# Delete Cloud SQL instance
gcloud sql instances delete leave-tracker-db --quiet

# Delete Cloud Storage bucket
gsutil rm -r gs://leave-tracker-2025-frontend

# Delete Artifact Registry repository
gcloud artifacts repositories delete leave-tracker-repo --location=us-central1 --quiet

# Delete entire project (nuclear option)
gcloud projects delete leave-tracker-2025 --quiet
```

---

## ✅ Final Checklist

### Deployment Complete When:
- [ ] ✅ Frontend URL loads in browser
- [ ] ✅ Backend API docs accessible
- [ ] ✅ User registration works with QR code
- [ ] ✅ Login works with 2FA
- [ ] ✅ JWT token in localStorage
- [ ] ✅ Dashboard loads people and types
- [ ] ✅ Can log absences
- [ ] ✅ Settings CRUD operations work
- [ ] ✅ Logout clears token
- [ ] ✅ Logs accessible via gcloud
- [ ] ✅ Budget alerts configured
- [ ] ✅ Costs at $0/month
- [ ] ✅ URLs saved and shared with team

---

## 🎉 Success!

**Congratulations!** Your Leave Tracker application is now live on Google Cloud Platform!

### Share with Your Team:
```
🎊 Our Leave Tracker is live!

Frontend: https://storage.googleapis.com/<your-project>-frontend/index.html

Instructions:
1. Click "Register"
2. Create account with username/password
3. Scan QR code with Google Authenticator app
4. Login with your 2FA code
5. Start tracking leave!

Questions? Check the docs or contact admin.
```

### Next Steps:
1. Share frontend URL with team
2. Monitor usage and costs daily for first week
3. Review logs regularly
4. Plan for Version 2.0 features
5. Consider custom domain setup

**Estimated cost for 10-50 users: $0/month** 🎉

---

## 📞 Support Resources

- **This Project's Docs**: All `.md` files in root directory
- **Google Cloud Docs**: https://cloud.google.com/docs
- **Cloud Run Docs**: https://cloud.google.com/run/docs
- **Cloud SQL Docs**: https://cloud.google.com/sql/docs
- **Free Tier Info**: https://cloud.google.com/free

**Deployment checklist completed!** ✅
