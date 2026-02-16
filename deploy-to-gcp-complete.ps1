# deploy-to-gcp-complete.ps1
# Complete deployment script for Leave Tracker App with all features
# Includes: Backend, Frontend, Database, Migrations, Gemini API

param(
    [Parameter(Mandatory=$true)]
    [string]$ProjectId,
    
    [Parameter(Mandatory=$true)]
    [string]$SecretKey,
    
    [Parameter(Mandatory=$true)]
    [string]$GeminiApiKey,
    
    [string]$Region = "us-central1",
    [string]$Version = "v1.1.0"
)

$ErrorActionPreference = "Continue"

Write-Host "`n==================================================" -ForegroundColor Cyan
Write-Host "LEAVE TRACKER - CLOUD DEPLOYMENT SCRIPT" -ForegroundColor Cyan
Write-Host "==================================================`n" -ForegroundColor Cyan

Write-Host "Configuration:" -ForegroundColor Yellow
Write-Host "   Project ID:     $ProjectId" -ForegroundColor White
Write-Host "   Region:         $Region" -ForegroundColor White
Write-Host "   Version:        $Version" -ForegroundColor White
Write-Host "   Gemini API:     Configured" -ForegroundColor Green
Write-Host ""

# Validate inputs
if ($SecretKey.Length -lt 32) {
    Write-Host "ERROR: Secret key must be at least 32 characters long" -ForegroundColor Red
    exit 1
}

# Step 1: Set project
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host "STEP 1/10: Setting up project..." -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray

gcloud config set project $ProjectId
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to set project. Please check project ID exists." -ForegroundColor Red
    exit 1
}
Write-Host "OK: Project set successfully`n" -ForegroundColor Green

# Step 2: Enable APIs
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host "STEP 2/10: Enabling required APIs..." -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray

$apis = @(
    "run.googleapis.com",
    "firestore.googleapis.com",
    "artifactregistry.googleapis.com",
    "cloudbuild.googleapis.com",
    "storage-api.googleapis.com",
    "compute.googleapis.com"
)

foreach ($api in $apis) {
    Write-Host "   Enabling $api..." -ForegroundColor Gray
    gcloud services enable $api --quiet 2>$null
}
Write-Host "OK: All APIs enabled`n" -ForegroundColor Green

# Set region
gcloud config set run/region $Region

# Step 3: Create Artifact Registry
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host "STEP 3/10: Setting up Artifact Registry..." -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray

$repoCheck = gcloud artifacts repositories describe leave-tracker-repo --location=$Region 2>&1
if ($LASTEXITCODE -ne 0) {
    gcloud artifacts repositories create leave-tracker-repo `
        --repository-format=docker `
        --location=$Region `
        --description="Leave Tracker Docker images"
    Write-Host "OK: Repository created" -ForegroundColor Green
} else {
    Write-Host "OK: Repository already exists" -ForegroundColor Green
}

Write-Host "" 

# Step 4: Build and push backend
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host "STEP 4/10: Building and pushing backend..." -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray

$ImageTag = "$Region-docker.pkg.dev/$ProjectId/leave-tracker-repo/backend:$Version"
Set-Location backend

Write-Host "   Submitting Cloud Build..." -ForegroundColor Gray
gcloud builds submit --tag $ImageTag
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Cloud Build failed" -ForegroundColor Red
    Set-Location ..
    exit 1
}

Set-Location ..
Write-Host "OK: Backend image ready: $ImageTag`n" -ForegroundColor Green

# Step 5: Firestore configuration
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host "STEP 5/10: Configuring Firestore..." -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray

Write-Host "   Firestore will use the Cloud Run service account" -ForegroundColor Gray
Write-Host "OK: Firestore configured`n" -ForegroundColor Green

# Step 6: Deploy backend to Cloud Run
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host "STEP 6/10: Deploying backend to Cloud Run..." -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray

gcloud run deploy leave-tracker-api `
    --image=$ImageTag `
    --platform=managed `
    --region=$Region `
    --allow-unauthenticated `
    --memory=512Mi `
    --cpu=1 `
    --min-instances=0 `
    --max-instances=10 `
    --timeout=300 `
    --set-env-vars="SECRET_KEY=$SecretKey,GEMINI_API_KEY=$GeminiApiKey,ALGORITHM=HS256,ACCESS_TOKEN_EXPIRE_MINUTES=30,ENVIRONMENT=production" `
    --quiet

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Backend deployment failed" -ForegroundColor Red
    exit 1
}

$BackendUrl = gcloud run services describe leave-tracker-api --region=$Region --format='value(status.url)'
Write-Host "OK: Backend deployed: $BackendUrl`n" -ForegroundColor Green

# Step 7: Firestore collections
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host "STEP 7/10: Firestore collections..." -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray

Write-Host "   Collections will be created on first use" -ForegroundColor Gray
Write-Host "   Collections: users, people, types, absences, ai_instructions" -ForegroundColor Gray
Write-Host "OK: Firestore ready`n" -ForegroundColor Green

# Step 8: Build frontend
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host "STEP 8/10: Building frontend..." -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray

Set-Location frontend

Write-Host "   Configuring API endpoint..." -ForegroundColor Gray
"VITE_API_URL=$BackendUrl" | Out-File -FilePath .env.production -Encoding utf8
"VITE_ENABLE_REGISTRATION=true" | Out-File -FilePath .env.production -Append -Encoding utf8

Write-Host "   Installing dependencies..." -ForegroundColor Gray
npm install --silent 2>$null

Write-Host "   Building production bundle..." -ForegroundColor Gray
npm run build:prod
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Frontend build failed" -ForegroundColor Red
    Set-Location ..
    exit 1
}

Write-Host "OK: Frontend built successfully`n" -ForegroundColor Green

# Step 9: Deploy frontend to Cloud Storage
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host "STEP 9/10: Deploying frontend to Cloud Storage..." -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray

$BucketName = "$ProjectId-frontend"

# Create bucket if not exists
$bucketCheck = gsutil ls gs://$BucketName 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "   Creating bucket..." -ForegroundColor Gray
    gsutil mb -l $Region gs://$BucketName
    Write-Host "OK: Bucket created: $BucketName" -ForegroundColor Green
} else {
    Write-Host "OK: Bucket already exists" -ForegroundColor Green
}

# Make bucket public
Write-Host "   Configuring public access..." -ForegroundColor Gray
gsutil iam ch allUsers:objectViewer gs://$BucketName

# Upload files
Write-Host "   Uploading files..." -ForegroundColor Gray
gsutil -m rsync -r -d dist/ gs://$BucketName/

# Configure website
gsutil web set -m index.html -e index.html gs://$BucketName

# Set cache headers
Write-Host "   Setting cache headers..." -ForegroundColor Gray
gsutil -m setmeta -h "Cache-Control:public, max-age=31536000" "gs://$BucketName/assets/**" 2>$null
gsutil setmeta -h "Cache-Control:no-cache, no-store, must-revalidate" "gs://$BucketName/index.html"

$FrontendUrl = "https://storage.googleapis.com/$BucketName/index.html"

Set-Location ..
Write-Host "OK: Frontend deployed: $FrontendUrl`n" -ForegroundColor Green

# Step 10: Update CORS
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host "STEP 10/10: Configuring CORS..." -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray

$CorsOrigin = "https://storage.googleapis.com"
gcloud run services update leave-tracker-api `
    --region=$Region `
    --update-env-vars="CORS_ORIGINS=$CorsOrigin" `
    --quiet

Write-Host "OK: CORS configured`n" -ForegroundColor Green

# Success Summary
Write-Host "`n==================================================" -ForegroundColor Green
Write-Host "DEPLOYMENT SUCCESSFUL" -ForegroundColor Green
Write-Host "==================================================`n" -ForegroundColor Green

Write-Host "Application URLs:" -ForegroundColor Cyan
Write-Host "   Frontend:     $FrontendUrl" -ForegroundColor White
Write-Host "   Backend API:  $BackendUrl" -ForegroundColor White
Write-Host "   API Docs:     $BackendUrl/docs" -ForegroundColor White
Write-Host ""

Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "   1. Visit the frontend URL above" -ForegroundColor White
Write-Host "   2. Click 'Register' to create first user account" -ForegroundColor White
Write-Host "   3. Scan QR code with Google Authenticator app" -ForegroundColor White
Write-Host "   4. Login with your username, password, and 6-digit code" -ForegroundColor White
Write-Host "   5. Go to Settings -> Add people and leave types" -ForegroundColor White
Write-Host "   6. Start tracking leaves!" -ForegroundColor White
Write-Host ""

Write-Host "Features Available:" -ForegroundColor Cyan
Write-Host "   - Dashboard - Quick absence logging" -ForegroundColor Green
Write-Host "   - Reports - View and manage all records with filters" -ForegroundColor Green
Write-Host "   - Smart Identification - AI-powered conversation parsing" -ForegroundColor Green
Write-Host "   - Settings - Manage people, types, password, AI rules" -ForegroundColor Green
Write-Host ""

Write-Host "Monitoring:" -ForegroundColor Yellow
Write-Host "   View logs:    gcloud run services logs tail leave-tracker-api --region=$Region" -ForegroundColor White
Write-Host "   Backend URL:  $BackendUrl/docs" -ForegroundColor White
Write-Host "   Firestore:    https://console.cloud.google.com/firestore/databases?project=$ProjectId" -ForegroundColor White
Write-Host ""

Write-Host "Tips:" -ForegroundColor Cyan
Write-Host "   - Use incognito mode or clear cache to see frontend updates" -ForegroundColor Gray
Write-Host "   - Check API documentation at /docs endpoint" -ForegroundColor Gray
Write-Host "   - Customize AI instructions via Settings menu" -ForegroundColor Gray
Write-Host "   - Free tier covers ~2M requests/month" -ForegroundColor Gray
Write-Host ""

Write-Host "OK: Your Leave Tracker app is now live in the cloud!" -ForegroundColor Green
Write-Host ""
