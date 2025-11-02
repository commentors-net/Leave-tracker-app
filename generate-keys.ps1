# Generate Secure Keys for Deployment
# Run this script to generate random secure keys

Write-Host "`n🔐 SECURE KEY GENERATOR" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor Gray

# Generate Secret Key (32 characters)
$SecretKey = -join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | ForEach-Object {[char]$_})

# Generate Database Password (16 characters with special chars)
$DbPassword = -join ((48..57) + (65..90) + (97..122) + (33,35,36,37,38,42,43,45,61,63,64) | Get-Random -Count 16 | ForEach-Object {[char]$_})

Write-Host "✅ Keys Generated Successfully!`n" -ForegroundColor Green

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host "📋 COPY THESE VALUES FOR DEPLOYMENT:" -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor Gray

Write-Host "Secret Key (for JWT tokens):" -ForegroundColor Cyan
Write-Host $SecretKey -ForegroundColor White
Write-Host ""

Write-Host "Database Password (for PostgreSQL):" -ForegroundColor Cyan
Write-Host $DbPassword -ForegroundColor White
Write-Host ""

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host "⚠️  IMPORTANT SECURITY NOTES:" -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor Gray

Write-Host "• NEVER commit these keys to git" -ForegroundColor Red
Write-Host "• Store them securely (password manager recommended)" -ForegroundColor Yellow
Write-Host "• You'll need them for deployment" -ForegroundColor Yellow
Write-Host "• Keep them private and confidential" -ForegroundColor Yellow
Write-Host ""

Write-Host "🔑 For Gemini API Key:" -ForegroundColor Cyan
Write-Host "   Visit: https://aistudio.google.com/apikey" -ForegroundColor White
Write-Host "   Click Create API Key and copy it" -ForegroundColor White
Write-Host ""

Write-Host "📝 Ready to deploy? Use these in your deployment command:" -ForegroundColor Green
Write-Host ""
Write-Host ".\deploy-to-gcp-complete.ps1 ``" -ForegroundColor Gray
Write-Host "    -ProjectId `"your-project-id`" ``" -ForegroundColor Gray
Write-Host "    -SecretKey `"$SecretKey`" ``" -ForegroundColor Gray
Write-Host "    -DbPassword `"$DbPassword`" ``" -ForegroundColor Gray
Write-Host "    -GeminiApiKey `"your-gemini-api-key`"" -ForegroundColor Gray
Write-Host ""
