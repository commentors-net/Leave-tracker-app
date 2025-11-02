# Frontend Deployment Script for Google Cloud Storage
# Use this script to deploy the frontend after making changes

# Colors for output
$Green = "Green"
$Cyan = "Cyan"
$Yellow = "Yellow"

Write-Host "`n========================================" -ForegroundColor $Green
Write-Host "  FRONTEND DEPLOYMENT" -ForegroundColor $Green
Write-Host "========================================`n" -ForegroundColor $Green

# Step 1: Build frontend
Write-Host "Step 1: Building frontend..." -ForegroundColor $Cyan
cd frontend
npm run build
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Build failed!" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Build successful`n" -ForegroundColor $Green

# Step 2: Delete old files (optional - comment out if you want to keep old versions)
Write-Host "Step 2: Cleaning old files..." -ForegroundColor $Cyan
gcloud storage rm -r gs://leave-tracker-2025-frontend/* --project=leave-tracker-2025 2>$null
Write-Host "✓ Cleaned (or already empty)`n" -ForegroundColor $Green

# Step 3: Upload new files
Write-Host "Step 3: Uploading files..." -ForegroundColor $Cyan
gcloud storage cp dist/index.html gs://leave-tracker-2025-frontend/ --project=leave-tracker-2025
gcloud storage cp -r dist/assets gs://leave-tracker-2025-frontend/ --project=leave-tracker-2025
gcloud storage cp -r dist/public gs://leave-tracker-2025-frontend/ --project=leave-tracker-2025

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Upload failed!" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Upload successful`n" -ForegroundColor $Green

# Step 4: Set cache control
Write-Host "Step 4: Setting cache control..." -ForegroundColor $Cyan
gcloud storage objects update gs://leave-tracker-2025-frontend/index.html `
    --cache-control="no-cache, no-store, must-revalidate" `
    --project=leave-tracker-2025
Write-Host "✓ Cache control set`n" -ForegroundColor $Green

# Step 5: Verify
Write-Host "Step 5: Verifying deployment..." -ForegroundColor $Cyan
gcloud storage ls gs://leave-tracker-2025-frontend/ --recursive --project=leave-tracker-2025

Write-Host "`n========================================" -ForegroundColor $Green
Write-Host "  DEPLOYMENT COMPLETE!" -ForegroundColor $Green
Write-Host "========================================`n" -ForegroundColor $Green
Write-Host "Frontend URL: https://storage.googleapis.com/leave-tracker-2025-frontend/index.html" -ForegroundColor $Cyan
Write-Host "`nNote: Clear browser cache or use incognito mode to see changes immediately`n" -ForegroundColor $Yellow

cd ..
