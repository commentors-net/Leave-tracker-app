# Google Cloud Deployment Scripts

## Quick Deploy Script (PowerShell)

Save this as `deploy-to-gcp.ps1` in your project root.

```powershell
# deploy-to-gcp.ps1
# Automated deployment script for Google Cloud Platform

param(
    [Parameter(Mandatory=$true)]
    [string]$ProjectId,
    
    [Parameter(Mandatory=$true)]
    [string]$SecretKey,
    
    [Parameter(Mandatory=$true)]
    [string]$DbPassword,
    
    [string]$Region = "us-central1",
    [string]$Version = "v1.0.0"
)

Write-Host "🚀 Starting Google Cloud Deployment..." -ForegroundColor Green

# Set project
Write-Host "`n📋 Setting project: $ProjectId" -ForegroundColor Yellow
gcloud config set project $ProjectId

# Enable required APIs
Write-Host "`n🔧 Enabling required APIs..." -ForegroundColor Yellow
gcloud services enable run.googleapis.com
gcloud services enable sqladmin.googleapis.com
gcloud services enable artifactregistry.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable storage-api.googleapis.com

# Set region
gcloud config set run/region $Region

# Create Artifact Registry (if not exists)
Write-Host "`n📦 Setting up Artifact Registry..." -ForegroundColor Yellow
gcloud artifacts repositories create leave-tracker-repo `
    --repository-format=docker `
    --location=$Region `
    --description="Leave Tracker Docker images" `
    2>$null

# Configure Docker authentication
gcloud auth configure-docker "$Region-docker.pkg.dev"

# Build and push backend
Write-Host "`n🐳 Building backend Docker image..." -ForegroundColor Yellow
Set-Location backend
docker build -t "$Region-docker.pkg.dev/$ProjectId/leave-tracker-repo/backend:$Version" .

Write-Host "`n📤 Pushing to Artifact Registry..." -ForegroundColor Yellow
docker push "$Region-docker.pkg.dev/$ProjectId/leave-tracker-repo/backend:$Version"
Set-Location ..

# Get Cloud SQL connection name
Write-Host "`n🗄️  Getting Cloud SQL connection..." -ForegroundColor Yellow
$SqlConnection = gcloud sql instances describe leave-tracker-db --format='value(connectionName)' 2>$null

if (-not $SqlConnection) {
    Write-Host "⚠️  Cloud SQL instance not found. Creating..." -ForegroundColor Yellow
    gcloud sql instances create leave-tracker-db `
        --database-version=POSTGRES_14 `
        --tier=db-f1-micro `
        --region=$Region `
        --storage-type=HDD `
        --storage-size=10GB `
        --storage-auto-increase `
        --backup-start-time=03:00
    
    Write-Host "Setting database password..." -ForegroundColor Yellow
    gcloud sql users set-password postgres `
        --instance=leave-tracker-db `
        --password=$DbPassword
    
    Write-Host "Creating database..." -ForegroundColor Yellow
    gcloud sql databases create leavetracker --instance=leave-tracker-db
    
    $SqlConnection = gcloud sql instances describe leave-tracker-db --format='value(connectionName)'
}

$DatabaseUrl = "postgresql://postgres:$DbPassword@/leavetracker?host=/cloudsql/$SqlConnection"

# Deploy backend to Cloud Run
Write-Host "`n🚢 Deploying backend to Cloud Run..." -ForegroundColor Yellow
gcloud run deploy leave-tracker-api `
    --image="$Region-docker.pkg.dev/$ProjectId/leave-tracker-repo/backend:$Version" `
    --platform=managed `
    --region=$Region `
    --allow-unauthenticated `
    --memory=512Mi `
    --cpu=1 `
    --min-instances=0 `
    --max-instances=10 `
    --timeout=300 `
    --set-env-vars="SECRET_KEY=$SecretKey" `
    --set-env-vars="ALGORITHM=HS256" `
    --set-env-vars="ACCESS_TOKEN_EXPIRE_MINUTES=30" `
    --set-env-vars="PORT=8080" `
    --set-cloudsql-instances=$SqlConnection `
    --set-env-vars="DATABASE_URL=$DatabaseUrl"

# Get backend URL
$BackendUrl = gcloud run services describe leave-tracker-api `
    --region=$Region `
    --format='value(status.url)'

Write-Host "`n✅ Backend deployed: $BackendUrl" -ForegroundColor Green

# Build frontend
Write-Host "`n🎨 Building frontend..." -ForegroundColor Yellow
Set-Location frontend

# Update .env.production
"VITE_API_URL=$BackendUrl" | Out-File -FilePath .env.production -Encoding utf8

npm install
npm run build:prod

# Create/update storage bucket
$BucketName = "$ProjectId-frontend"
Write-Host "`n☁️  Deploying frontend to Cloud Storage..." -ForegroundColor Yellow

gsutil mb -l $Region gs://$BucketName 2>$null
gsutil iam ch allUsers:objectViewer gs://$BucketName
gsutil -m rsync -r -d dist/ gs://$BucketName/
gsutil web set -m index.html -e index.html gs://$BucketName

# Set cache headers
gsutil -m setmeta -h "Cache-Control:public, max-age=31536000" "gs://$BucketName/**/*.js" 2>$null
gsutil -m setmeta -h "Cache-Control:public, max-age=31536000" "gs://$BucketName/**/*.css" 2>$null

$FrontendUrl = "https://storage.googleapis.com/$BucketName/index.html"

Set-Location ..

# Update CORS
Write-Host "`n🔐 Updating CORS settings..." -ForegroundColor Yellow
gcloud run services update leave-tracker-api `
    --region=$Region `
    --update-env-vars="CORS_ORIGINS=https://storage.googleapis.com/$BucketName"

Write-Host "`n✅ Frontend deployed: $FrontendUrl" -ForegroundColor Green

# Summary
Write-Host "`n" -NoNewline
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "🎉 Deployment Complete!" -ForegroundColor Green
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "`nBackend API:  " -NoNewline -ForegroundColor White
Write-Host $BackendUrl -ForegroundColor Cyan
Write-Host "Frontend App: " -NoNewline -ForegroundColor White
Write-Host $FrontendUrl -ForegroundColor Cyan
Write-Host "`nAPI Docs:     " -NoNewline -ForegroundColor White
Write-Host "$BackendUrl/docs" -ForegroundColor Cyan
Write-Host "`n" -NoNewline
Write-Host "💡 Next steps:" -ForegroundColor Yellow
Write-Host "   1. Visit frontend URL to test registration" -ForegroundColor White
Write-Host "   2. Check API docs at /docs endpoint" -ForegroundColor White
Write-Host "   3. Monitor logs: gcloud run services logs tail leave-tracker-api" -ForegroundColor White
Write-Host "`n"
```

---

## Usage

### First Time Deployment

```powershell
# Generate a secure secret key first
python -c "import secrets; print(secrets.token_hex(32))"

# Run deployment
.\deploy-to-gcp.ps1 `
    -ProjectId "leave-tracker-app-2025" `
    -SecretKey "your-generated-secret-key-here" `
    -DbPassword "your-secure-db-password-here" `
    -Region "us-central1" `
    -Version "v1.0.0"
```

### Update Deployment (New Version)

```powershell
# Increment version
.\deploy-to-gcp.ps1 `
    -ProjectId "leave-tracker-app-2025" `
    -SecretKey "your-existing-secret-key" `
    -DbPassword "your-existing-db-password" `
    -Region "us-central1" `
    -Version "v1.0.1"
```

---

## Manual Step-by-Step (If Script Fails)

### 1. Initial Setup
```powershell
# Login and create project
gcloud auth login
gcloud projects create leave-tracker-app-2025
gcloud config set project leave-tracker-app-2025

# Enable APIs
gcloud services enable run.googleapis.com sqladmin.googleapis.com artifactregistry.googleapis.com cloudbuild.googleapis.com storage-api.googleapis.com
```

### 2. Create Database
```powershell
# Create Cloud SQL instance
gcloud sql instances create leave-tracker-db `
    --database-version=POSTGRES_14 `
    --tier=db-f1-micro `
    --region=us-central1 `
    --storage-type=HDD `
    --storage-size=10GB

# Set password
gcloud sql users set-password postgres `
    --instance=leave-tracker-db `
    --password=YOUR_PASSWORD

# Create database
gcloud sql databases create leavetracker --instance=leave-tracker-db
```

### 3. Build and Deploy Backend
```powershell
# Create repository
gcloud artifacts repositories create leave-tracker-repo `
    --repository-format=docker `
    --location=us-central1

# Configure Docker
gcloud auth configure-docker us-central1-docker.pkg.dev

# Build and push
cd backend
docker build -t us-central1-docker.pkg.dev/leave-tracker-app-2025/leave-tracker-repo/backend:v1.0.0 .
docker push us-central1-docker.pkg.dev/leave-tracker-app-2025/leave-tracker-repo/backend:v1.0.0

# Deploy to Cloud Run
gcloud run deploy leave-tracker-api `
    --image=us-central1-docker.pkg.dev/leave-tracker-app-2025/leave-tracker-repo/backend:v1.0.0 `
    --platform=managed `
    --region=us-central1 `
    --allow-unauthenticated `
    --memory=512Mi `
    --set-env-vars="SECRET_KEY=your-secret-key" `
    --set-cloudsql-instances=leave-tracker-app-2025:us-central1:leave-tracker-db `
    --set-env-vars="DATABASE_URL=postgresql://postgres:password@/leavetracker?host=/cloudsql/leave-tracker-app-2025:us-central1:leave-tracker-db"
```

### 4. Deploy Frontend
```powershell
cd ..\frontend

# Update API URL
"VITE_API_URL=https://your-backend-url.run.app" | Out-File .env.production

# Build
npm install
npm run build:prod

# Deploy to Cloud Storage
gsutil mb gs://leave-tracker-app-2025-frontend
gsutil iam ch allUsers:objectViewer gs://leave-tracker-app-2025-frontend
gsutil -m rsync -r dist/ gs://leave-tracker-app-2025-frontend/
gsutil web set -m index.html -e index.html gs://leave-tracker-app-2025-frontend
```

---

## Environment Variables Reference

### Required for Deployment
- `ProjectId` - Google Cloud project ID
- `SecretKey` - JWT secret key (generate with `python -c "import secrets; print(secrets.token_hex(32))"`)
- `DbPassword` - PostgreSQL database password

### Optional
- `Region` - GCP region (default: us-central1)
- `Version` - Docker image version tag (default: v1.0.0)

---

## Troubleshooting

### Docker Build Fails
```powershell
# Check Docker is running
docker version

# Login to gcloud again
gcloud auth login
gcloud auth configure-docker us-central1-docker.pkg.dev
```

### Cloud SQL Connection Error
```powershell
# Verify instance exists
gcloud sql instances list

# Get connection name
gcloud sql instances describe leave-tracker-db --format='value(connectionName)'

# Test connection
gcloud sql connect leave-tracker-db --user=postgres
```

### Frontend Build Fails
```powershell
# Clear npm cache
cd frontend
Remove-Item -Recurse -Force node_modules
Remove-Item -Force package-lock.json
npm install
npm run build:prod
```

### CORS Issues
```powershell
# Update CORS with exact URL
gcloud run services update leave-tracker-api `
    --region=us-central1 `
    --update-env-vars="CORS_ORIGINS=https://storage.googleapis.com/your-bucket-name"
```

---

## Monitoring Commands

```powershell
# View backend logs
gcloud run services logs tail leave-tracker-api --region=us-central1

# Check Cloud Run status
gcloud run services list

# Check Cloud SQL status
gcloud sql instances list

# View database size
gcloud sql instances describe leave-tracker-db --format='value(settings.dataDiskSizeGb)'

# Check costs (requires billing API)
gcloud billing accounts list
```

---

## Cleanup (Delete Everything)

```powershell
# Delete Cloud Run service
gcloud run services delete leave-tracker-api --region=us-central1 --quiet

# Delete Cloud SQL instance
gcloud sql instances delete leave-tracker-db --quiet

# Delete Cloud Storage bucket
gsutil rm -r gs://leave-tracker-app-2025-frontend

# Delete Artifact Registry repository
gcloud artifacts repositories delete leave-tracker-repo --location=us-central1 --quiet

# Delete project (optional - deletes everything)
gcloud projects delete leave-tracker-app-2025 --quiet
```

---

## Cost Monitoring

Set up budget alerts to avoid unexpected charges:

```powershell
# View current project costs
gcloud billing accounts list

# Create budget (do this in Cloud Console for easier setup)
# Navigate to: Billing → Budgets & alerts → Create Budget
# Set alert at $5/month with email notifications
```

---

## Security Checklist

- [ ] SECRET_KEY is unique and secure (32+ characters)
- [ ] Database password is strong
- [ ] CORS origins limited to your frontend URL only
- [ ] Cloud SQL accepts connections only from Cloud Run
- [ ] Budget alerts configured
- [ ] Environment variables not in source code
- [ ] .env files in .gitignore
- [ ] Regular backups enabled for Cloud SQL

---

## Support

If you encounter issues:

1. Check logs: `gcloud run services logs tail leave-tracker-api`
2. Verify environment variables: `gcloud run services describe leave-tracker-api`
3. Test Cloud SQL: `gcloud sql connect leave-tracker-db --user=postgres`
4. Review [GOOGLE_CLOUD_DEPLOYMENT.md](./GOOGLE_CLOUD_DEPLOYMENT.md) for detailed steps
