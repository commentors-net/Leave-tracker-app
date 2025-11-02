"""
Export data from PostgreSQL Cloud SQL to JSON format
Run this BEFORE migrating to Firestore
"""
import json
import os
from datetime import date, datetime
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Your Cloud SQL connection
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("ERROR: DATABASE_URL not found in environment variables")
    exit(1)

print(f"Connecting to database...")
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

def export_data():
    """Export all data to JSON"""
    
    export_data = {
        "users": [],
        "ai_instructions": [],
        "people": [],
        "types": [],
        "absences": []
    }
    
    # Export Users
    print("Exporting users...")
    result = db.execute(text("SELECT id, username, password, otp_secret FROM users"))
    for row in result:
        export_data["users"].append({
            "id": row[0],
            "username": row[1],
            "password": row[2],
            "otp_secret": row[3]
        })
    
    # Export AI Instructions
    print("Exporting AI instructions...")
    result = db.execute(text("SELECT id, instructions, created_at, updated_at FROM ai_instructions"))
    for row in result:
        export_data["ai_instructions"].append({
            "id": row[0],
            "instructions": row[1],
            "created_at": row[2],
            "updated_at": row[3]
        })
    
    # Export People
    print("Exporting people...")
    result = db.execute(text("SELECT id, name FROM people"))
    for row in result:
        export_data["people"].append({
            "id": row[0],
            "name": row[1]
        })
    
    # Export Types
    print("Exporting leave types...")
    result = db.execute(text("SELECT id, name FROM types"))
    for row in result:
        export_data["types"].append({
            "id": row[0],
            "name": row[1]
        })
    
    # Export Absences
    print("Exporting absences...")
    result = db.execute(text("SELECT id, date, duration, reason, type_id, person_id, applied FROM absences"))
    for row in result:
        absence_date = row[1]
        export_data["absences"].append({
            "id": row[0],
            "date": absence_date.isoformat() if isinstance(absence_date, date) else str(absence_date),
            "duration": row[2],
            "reason": row[3],
            "type_id": row[4],
            "person_id": row[5],
            "applied": row[6]
        })
    
    # Save to JSON file
    output_file = "data_export.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Export complete!")
    print(f"📁 Data saved to: {output_file}")
    print(f"\n📊 Export Summary:")
    print(f"   Users: {len(export_data['users'])}")
    print(f"   AI Instructions: {len(export_data['ai_instructions'])}")
    print(f"   People: {len(export_data['people'])}")
    print(f"   Leave Types: {len(export_data['types'])}")
    print(f"   Absences: {len(export_data['absences'])}")
    
    db.close()

if __name__ == "__main__":
    try:
        export_data()
    except Exception as e:
        print(f"\n❌ Export failed: {e}")
        import traceback
        traceback.print_exc()
