# Migrate to Firestore - FREE Google Cloud Database
# Step-by-step guide to migrate from Cloud SQL to Firestore

Write-Host "`nFIRESTORE MIGRATION GUIDE" -ForegroundColor Cyan
Write-Host "=============================================`n" -ForegroundColor Gray

Write-Host "COST COMPARISON:" -ForegroundColor Yellow
Write-Host "  Current Cloud SQL: RM 12-15/month" -ForegroundColor Red
Write-Host "  After Firestore:   RM 0.00/month" -ForegroundColor Green
Write-Host "  Free tier limit:   1 GB storage" -ForegroundColor Gray

Write-Host "`n=============================================" -ForegroundColor Gray
Write-Host "`nSTEP 1: ENABLE FIRESTORE" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Gray
Write-Host "`n1. Go to Firestore console:" -ForegroundColor White
Write-Host "   https://console.cloud.google.com/firestore?project=leave-tracker-2025`n" -ForegroundColor Cyan
Write-Host "2. Click 'Select Native Mode'" -ForegroundColor White
Write-Host "3. Choose location: us-central1" -ForegroundColor White
Write-Host "4. Click 'Create Database'" -ForegroundColor White
Write-Host "   Takes 1-2 minutes...`n" -ForegroundColor Gray

Write-Host "=============================================" -ForegroundColor Gray
Write-Host "STEP 2: EXPORT DATA FROM CLOUD SQL" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Gray
Write-Host "`nRun the export script:" -ForegroundColor White
Write-Host "  cd backend" -ForegroundColor Cyan
Write-Host "  python export_postgresql_data.py`n" -ForegroundColor Cyan
Write-Host "This creates data_export.json`n" -ForegroundColor Green

Write-Host "=============================================" -ForegroundColor Gray
Write-Host "STEP 3: SETUP FIRESTORE AUTH" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Gray
Write-Host "`nCreate service account:" -ForegroundColor White
Write-Host '  gcloud iam service-accounts create firestore-app --display-name="Firestore App" --project=leave-tracker-2025' -ForegroundColor Cyan

Write-Host "`nGrant permissions:" -ForegroundColor White  
Write-Host '  gcloud projects add-iam-policy-binding leave-tracker-2025 --member="serviceAccount:firestore-app@leave-tracker-2025.iam.gserviceaccount.com" --role="roles/datastore.user"' -ForegroundColor Cyan

Write-Host "`nCreate key file:" -ForegroundColor White
Write-Host '  gcloud iam service-accounts keys create firestore-key.json --iam-account=firestore-app@leave-tracker-2025.iam.gserviceaccount.com' -ForegroundColor Cyan

Write-Host "`n=============================================" -ForegroundColor Gray
Write-Host "STEP 4: IMPORT DATA TO FIRESTORE" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Gray
Write-Host "`nSet environment variable:" -ForegroundColor White
Write-Host '  $env:GOOGLE_APPLICATION_CREDENTIALS = "$PWD\firestore-key.json"' -ForegroundColor Cyan

Write-Host "`nInstall library:" -ForegroundColor White
Write-Host "  pip install google-cloud-firestore" -ForegroundColor Cyan

Write-Host "`nRun import:" -ForegroundColor White
Write-Host "  python import_to_firestore.py`n" -ForegroundColor Cyan

Write-Host "=============================================" -ForegroundColor Gray
Write-Host "STEP 5: UPDATE BACKEND CODE" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Gray
Write-Host "`nFirestore helper created:" -ForegroundColor White
Write-Host "  backend/app/firestore_db.py`n" -ForegroundColor Green

Write-Host "Files to update:" -ForegroundColor Yellow
Write-Host "  - backend/app/api/auth.py" -ForegroundColor White
Write-Host "  - backend/app/api/people.py" -ForegroundColor White
Write-Host "  - backend/app/api/types.py" -ForegroundColor White
Write-Host "  - backend/app/api/absences.py" -ForegroundColor White
Write-Host "  - backend/app/api/ai_instructions.py`n" -ForegroundColor White

Write-Host "I'll help you update these files next!`n" -ForegroundColor Yellow

Write-Host "=============================================" -ForegroundColor Gray
Write-Host "STEP 6: DEPLOY TO CLOUD RUN" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Gray
Write-Host "`nAfter code updates:" -ForegroundColor White
Write-Host "  cd backend" -ForegroundColor Cyan
Write-Host '  gcloud run deploy leave-tracker-api --source . --region=us-central1 --service-account=firestore-app@leave-tracker-2025.iam.gserviceaccount.com' -ForegroundColor Cyan

Write-Host "`n=============================================" -ForegroundColor Gray
Write-Host "STEP 7: DELETE CLOUD SQL" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Gray
Write-Host "`nAfter confirming app works:" -ForegroundColor Yellow
Write-Host "  gcloud sql instances delete leave-tracker-db --project=leave-tracker-2025`n" -ForegroundColor Cyan

Write-Host "=============================================" -ForegroundColor Gray
Write-Host "FINAL RESULT:" -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Gray
Write-Host "  Firestore:      RM 0.00" -ForegroundColor Green
Write-Host "  Cloud Run:      RM 0.00" -ForegroundColor Green
Write-Host "  Cloud Storage:  RM 0.00" -ForegroundColor Green
Write-Host "  -------------------------" -ForegroundColor Gray
Write-Host "  TOTAL:          RM 0.00/month`n" -ForegroundColor Green

Write-Host "Your app will be 100% FREE!`n" -ForegroundColor Green
