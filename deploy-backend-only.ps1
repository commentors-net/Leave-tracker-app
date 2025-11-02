# deploy-backend-only.ps1
# Quick backend update deployment script

param(
    [Parameter(Mandatory=$true)]
    [string]$ProjectId,
    
    [string]$Region = "us-central1",
    [string]$Version = "v1.1.0"
)

Write-Host "`n🚀 BACKEND UPDATE DEPLOYMENT" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor Gray

# Set project
Write-Host "Setting project..." -ForegroundColor Yellow
gcloud config set project $ProjectId
gcloud config set run/region $Region

# Configure Docker
Write-Host "Configuring Docker..." -ForegroundColor Yellow
gcloud auth configure-docker "$Region-docker.pkg.dev" --quiet

# Build and push
Write-Host "`nBuilding backend image..." -ForegroundColor Yellow
$ImageTag = "$Region-docker.pkg.dev/$ProjectId/leave-tracker-repo/backend:$Version"

Set-Location backend
docker build -t $ImageTag . --quiet

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Build failed!" -ForegroundColor Red
    Set-Location ..
    exit 1
}

Write-Host "Pushing to registry..." -ForegroundColor Yellow
docker push $ImageTag

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Push failed!" -ForegroundColor Red
    Set-Location ..
    exit 1
}

Set-Location ..

# Deploy
Write-Host "`nDeploying to Cloud Run..." -ForegroundColor Yellow
gcloud run deploy leave-tracker-api `
    --image=$ImageTag `
    --region=$Region `
    --quiet

if ($LASTEXITCODE -eq 0) {
    $BackendUrl = gcloud run services describe leave-tracker-api --region=$Region --format='value(status.url)'
    Write-Host "`n✅ Backend updated successfully!" -ForegroundColor Green
    Write-Host "URL: $BackendUrl" -ForegroundColor Cyan
} else {
    Write-Host "`n❌ Deployment failed!" -ForegroundColor Red
    exit 1
}
