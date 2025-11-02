"""
Import data from JSON to Firestore
Run this AFTER exporting from PostgreSQL
"""
import json
import os
from datetime import datetime
from google.cloud import firestore

def import_data():
    """Import JSON data to Firestore"""
    
    # Check if export file exists
    if not os.path.exists("data_export.json"):
        print("❌ Error: data_export.json not found!")
        print("   Run export_postgresql_data.py first")
        exit(1)
    
    # Load export data
    print("Loading export data...")
    with open("data_export.json", 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Initialize Firestore
    print("Connecting to Firestore...")
    db = firestore.Client(project="leave-tracker-2025")
    
    # Create ID mapping for relationships
    id_map = {
        "people": {},
        "types": {}
    }
    
    # Import Users
    print(f"\nImporting {len(data['users'])} users...")
    for user in data['users']:
        user_ref = db.collection("users").document()
        user_ref.set({
            "username": user["username"],
            "password": user["password"],
            "otp_secret": user["otp_secret"],
            "created_at": datetime.now().isoformat()
        })
        print(f"  ✓ User: {user['username']}")
    
    # Import AI Instructions
    print(f"\nImporting {len(data['ai_instructions'])} AI instructions...")
    for instruction in data['ai_instructions']:
        instruction_ref = db.collection("ai_instructions").document()
        instruction_ref.set({
            "instructions": instruction["instructions"],
            "created_at": instruction.get("created_at", datetime.now().isoformat()),
            "updated_at": instruction.get("updated_at", datetime.now().isoformat())
        })
        print(f"  ✓ AI instruction created")
    
    # Import People
    print(f"\nImporting {len(data['people'])} people...")
    for person in data['people']:
        person_ref = db.collection("people").document()
        person_ref.set({
            "name": person["name"]
        })
        # Map old ID to new Firestore ID
        id_map["people"][person["id"]] = person_ref.id
        print(f"  ✓ Person: {person['name']}")
    
    # Import Types
    print(f"\nImporting {len(data['types'])} leave types...")
    for leave_type in data['types']:
        type_ref = db.collection("types").document()
        type_ref.set({
            "name": leave_type["name"]
        })
        # Map old ID to new Firestore ID
        id_map["types"][leave_type["id"]] = type_ref.id
        print(f"  ✓ Type: {leave_type['name']}")
    
    # Import Absences
    print(f"\nImporting {len(data['absences'])} absences...")
    for absence in data['absences']:
        # Map old IDs to new Firestore IDs
        person_id = id_map["people"].get(absence["person_id"])
        type_id = id_map["types"].get(absence["type_id"])
        
        if not person_id or not type_id:
            print(f"  ⚠️  Skipping absence (missing person or type mapping)")
            continue
        
        absence_ref = db.collection("absences").document()
        absence_ref.set({
            "date": absence["date"],
            "duration": absence["duration"],
            "reason": absence["reason"],
            "type_id": type_id,
            "person_id": person_id,
            "applied": absence.get("applied", 0),
            "created_at": datetime.now().isoformat()
        })
    
    print(f"\n✅ Import complete!")
    print(f"\n📊 Import Summary:")
    print(f"   Users: {len(data['users'])}")
    print(f"   AI Instructions: {len(data['ai_instructions'])}")
    print(f"   People: {len(data['people'])}")
    print(f"   Leave Types: {len(data['types'])}")
    print(f"   Absences: {len(data['absences'])}")
    
    # Save ID mapping for reference
    with open("id_mapping.json", 'w') as f:
        json.dump(id_map, f, indent=2)
    print(f"\n📝 ID mapping saved to: id_mapping.json")

if __name__ == "__main__":
    try:
        import_data()
    except Exception as e:
        print(f"\n❌ Import failed: {e}")
        import traceback
        traceback.print_exc()
