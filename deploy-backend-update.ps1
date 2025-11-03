# Quick backend deployment script
Write-Host "`n🚀 Deploying Backend Updates to Production" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor Gray

$ProjectId = "leave-tracker-2025"
$Region = "us-central1"
$ImageTag = "$Region-docker.pkg.dev/$ProjectId/leave-tracker-repo/backend:latest"

# Step 1: Configure project
Write-Host "Step 1/3: Configuring project..." -ForegroundColor Yellow
gcloud config set project $ProjectId --quiet
gcloud config set run/region $Region --quiet
Write-Host "✓ Project configured`n" -ForegroundColor Green

# Step 2: Build with Cloud Build
Write-Host "Step 2/3: Building image with Cloud Build - this may take 2-3 minutes..." -ForegroundColor Yellow
Set-Location backend
gcloud builds submit --tag $ImageTag

if ($LASTEXITCODE -ne 0) {
    Write-Host "`n❌ Build failed!" -ForegroundColor Red
    Set-Location ..
    exit 1
}
Set-Location ..
Write-Host "✓ Image built successfully`n" -ForegroundColor Green

# Step 3: Deploy to Cloud Run
Write-Host "Step 3/3: Deploying to Cloud Run..." -ForegroundColor Yellow
gcloud run deploy leave-tracker-api `
    --image=$ImageTag `
    --region=$Region `
    --platform=managed `
    --quiet

if ($LASTEXITCODE -eq 0) {
    $BackendUrl = gcloud run services describe leave-tracker-api --region=$Region --format='value(status.url)'
    Write-Host "" -ForegroundColor Green
    Write-Host "========================================================" -ForegroundColor Green
    Write-Host "         DEPLOYMENT SUCCESSFUL!              " -ForegroundColor Green
    Write-Host "========================================================" -ForegroundColor Green
    Write-Host "" -ForegroundColor Green
    Write-Host "Backend URL: $BackendUrl" -ForegroundColor Cyan
    Write-Host "API Docs:    $BackendUrl/docs" -ForegroundColor Cyan
    Write-Host "" -ForegroundColor Yellow
    Write-Host "Your production backend is now updated with all fixes!" -ForegroundColor Yellow
} else {
    Write-Host ""
    Write-Host "Deployment failed!" -ForegroundColor Red
    exit 1
}
