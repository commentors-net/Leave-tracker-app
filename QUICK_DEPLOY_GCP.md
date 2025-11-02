# Quick Deploy to Google Cloud (Free Tier)

## 🚀 One-Command Deployment

### Prerequisites (5 minutes)
1. **Install gcloud CLI**: https://cloud.google.com/sdk/docs/install
2. **Install Docker Desktop**: https://www.docker.com/products/docker-desktop
3. **Create Google Cloud Account**: https://console.cloud.google.com

### Step 1: Login to Google Cloud
```powershell
gcloud auth login
```

### Step 2: Generate Secrets
```powershell
# Generate JWT secret key
python -c "import secrets; print(secrets.token_hex(32))"
# Save this output!

# Create a strong database password
# Example: "MySecureDb2025!@#"
```

### Step 3: Deploy!
```powershell
# Replace with your values
.\deploy-to-gcp.ps1 `
    -ProjectId "leave-tracker-2025" `
    -SecretKey "paste-generated-secret-here" `
    -DbPassword "your-database-password-here"
```

**That's it!** The script will:
- ✅ Create Google Cloud project
- ✅ Enable required APIs
- ✅ Create PostgreSQL database (free tier)
- ✅ Build and deploy backend to Cloud Run
- ✅ Build and deploy frontend to Cloud Storage
- ✅ Configure CORS and networking

**Time to deploy**: ~10 minutes

---

## 📱 After Deployment

### Your URLs will be displayed:
```
Frontend:  https://storage.googleapis.com/leave-tracker-2025-frontend/index.html
Backend:   https://leave-tracker-api-xxxxx-uc.a.run.app
API Docs:  https://leave-tracker-api-xxxxx-uc.a.run.app/docs
```

### Test Your Application:
1. Visit the Frontend URL
2. Click "Register"
3. Create account with Google Authenticator
4. Login and start using!

---

## 💰 Cost: $0/month (Free Tier)

Your application uses:
- **Cloud Run**: 2M requests/month FREE
- **Cloud SQL**: db-f1-micro FREE
- **Cloud Storage**: 5GB FREE
- **Egress**: 1GB/month FREE

**Perfect for teams up to 50 users!**

---

## 🔄 Update Your App

```powershell
# After making code changes, redeploy:
.\deploy-to-gcp.ps1 `
    -ProjectId "leave-tracker-2025" `
    -SecretKey "same-secret-as-before" `
    -DbPassword "same-password-as-before" `
    -Version "v1.0.1"
```

---

## 📊 Monitor Your App

### View Logs
```powershell
gcloud run services logs tail leave-tracker-api --region=us-central1
```

### Check Status
```powershell
gcloud run services list
```

### View Costs (should be $0!)
Visit: https://console.cloud.google.com/billing

---

## 🆘 Troubleshooting

### Docker not running?
```powershell
# Start Docker Desktop, then retry
```

### "Project already exists"?
```powershell
# Use a different ProjectId:
.\deploy-to-gcp.ps1 -ProjectId "leave-tracker-2025-v2" ...
```

### Frontend can't reach backend?
```powershell
# Check CORS settings
gcloud run services describe leave-tracker-api --format='value(spec.template.spec.containers[0].env)'
```

### Need to start over?
```powershell
# Delete everything and redeploy
gcloud run services delete leave-tracker-api --region=us-central1
gcloud sql instances delete leave-tracker-db
gsutil rm -r gs://leave-tracker-2025-frontend
```

---

## 📚 Detailed Guides

- **Full Deployment Guide**: [GOOGLE_CLOUD_DEPLOYMENT.md](./GOOGLE_CLOUD_DEPLOYMENT.md)
- **Manual Steps**: [DEPLOY_SCRIPTS.md](./DEPLOY_SCRIPTS.md)
- **Application Setup**: [SETUP.md](./SETUP.md)

---

## ✅ Quick Checklist

Before deploying:
- [ ] gcloud CLI installed
- [ ] Docker Desktop installed and running
- [ ] Google Cloud account created
- [ ] Billing enabled (won't charge for free tier)
- [ ] SECRET_KEY generated
- [ ] Database password created

After deploying:
- [ ] Frontend URL accessible
- [ ] Backend API docs working
- [ ] Registration flow tested
- [ ] Login with 2FA tested
- [ ] Dashboard loads data

---

## 🎉 Success!

Your Leave Tracker is now live on Google Cloud Platform!

**Share the frontend URL with your team and start tracking leave!** 🚀

For questions or issues, check:
- [Full deployment guide](./GOOGLE_CLOUD_DEPLOYMENT.md)
- [Version 1.0 release notes](./VERSION_1.0_RELEASE.md)
- Google Cloud logs: `gcloud run services logs tail leave-tracker-api`
