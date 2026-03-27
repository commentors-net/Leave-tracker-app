#!/usr/bin/env python3
"""
Database Migration Script: Add user_id to tables
================================================

This script adds user_id column to absences, people, types, and ai_instructions tables.
It handles both SQLite and Firestore databases.

Safety:
- No data is deleted
- Existing records are assigned to the first user (or a default user)
- Creates backup before migration for SQLite

Usage:
    python migrate_add_user_id.py

Environment:
    Set ENVIRONMENT=development for SQLite
    Set ENVIRONMENT=production for Firestore
"""

import os
import sys
import sqlite3
import shutil
from datetime import datetime
from pathlib import Path

# Add parent directory to path to import app modules
sys.path.insert(0, str(Path(__file__).parent))

def migrate_sqlite(db_path: str):
    """Migrate SQLite database to add user_id columns"""
    print(f"Migrating SQLite database: {db_path}")
    
    # Create backup
    backup_path = f"{db_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    shutil.copy2(db_path, backup_path)
    print(f"✓ Backup created: {backup_path}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get the first user ID (or None if no users exist)
    cursor.execute("SELECT id FROM users ORDER BY id LIMIT 1")
    first_user_row = cursor.fetchone()
    first_user_id = first_user_row[0] if first_user_row else None
    
    if not first_user_id:
        print("⚠️  Warning: No users found in database. Please create a user first.")
        conn.close()
        return False
    
    print(f"✓ Found first user ID: {first_user_id}")
    print(f"  Existing records will be assigned to this user.")
    
    try:
        # Check if migrations are already applied
        cursor.execute("PRAGMA table_info(absences)")
        absences_columns = [col[1] for col in cursor.fetchall()]
        
        if 'user_id' in absences_columns:
            print("✓ Migration already applied (user_id column exists)")
            conn.close()
            return True
        
        print("\nApplying migrations...")
        
        # 1. Add user_id to ai_instructions
        print("  - Adding user_id to ai_instructions table...")
        cursor.execute("PRAGMA table_info(ai_instructions)")
        ai_columns = [col[1] for col in cursor.fetchall()]
        if 'user_id' not in ai_columns:
            cursor.execute(f"ALTER TABLE ai_instructions ADD COLUMN user_id TEXT NOT NULL DEFAULT '{first_user_id}'")
            cursor.execute(f"UPDATE ai_instructions SET user_id = '{first_user_id}' WHERE user_id IS NULL OR user_id = ''")
            print("    ✓ ai_instructions migrated")
        
        # 2. Add user_id to people
        print("  - Adding user_id to people table...")
        cursor.execute("PRAGMA table_info(people)")
        people_columns = [col[1] for col in cursor.fetchall()]
        if 'user_id' not in people_columns:
            cursor.execute(f"ALTER TABLE people ADD COLUMN user_id TEXT NOT NULL DEFAULT '{first_user_id}'")
            cursor.execute(f"UPDATE people SET user_id = '{first_user_id}' WHERE user_id IS NULL OR user_id = ''")
            # Remove unique constraint on name (now unique per user)
            # SQLite doesn't support dropping constraints, so we'll handle uniqueness in application
            print("    ✓ people migrated")
        
        # 3. Add user_id to types
        print("  - Adding user_id to types table...")
        cursor.execute("PRAGMA table_info(types)")
        types_columns = [col[1] for col in cursor.fetchall()]
        if 'user_id' not in types_columns:
            cursor.execute(f"ALTER TABLE types ADD COLUMN user_id TEXT NOT NULL DEFAULT '{first_user_id}'")
            cursor.execute(f"UPDATE types SET user_id = '{first_user_id}' WHERE user_id IS NULL OR user_id = ''")
            # Remove unique constraint on name (now unique per user)
            print("    ✓ types migrated")
        
        # 4. Add user_id to absences
        print("  - Adding user_id to absences table...")
        cursor.execute("PRAGMA table_info(absences)")
        absences_columns = [col[1] for col in cursor.fetchall()]
        if 'user_id' not in absences_columns:
            cursor.execute(f"ALTER TABLE absences ADD COLUMN user_id TEXT NOT NULL DEFAULT '{first_user_id}'")
            cursor.execute(f"UPDATE absences SET user_id = '{first_user_id}' WHERE user_id IS NULL OR user_id = ''")
            print("    ✓ absences migrated")
        
        conn.commit()
        
        # Verify migrations
        print("\nVerifying migrations...")
        for table in ['ai_instructions', 'people', 'types', 'absences']:
            cursor.execute(f"PRAGMA table_info({table})")
            columns = [col[1] for col in cursor.fetchall()]
            if 'user_id' in columns:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"  ✓ {table}: user_id column added ({count} records)")
            else:
                print(f"  ✗ {table}: user_id column NOT found")
        
        print("\n✅ SQLite migration completed successfully!")
        print(f"   Backup saved at: {backup_path}")
        
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        conn.rollback()
        print(f"   Restoring from backup: {backup_path}")
        conn.close()
        shutil.copy2(backup_path, db_path)
        return False
    
    finally:
        conn.close()
    
    return True


def migrate_firestore():
    """Migrate Firestore database to add user_id field"""
    print("Migrating Firestore database...")
    
    try:
        from google.cloud import firestore
        
        db = firestore.Client()
        
        # Get first user
        users_ref = db.collection('users')
        users = list(users_ref.limit(1).stream())
        
        if not users:
            print("⚠️  Warning: No users found in Firestore. Please create a user first.")
            return False
        
        first_user_id = users[0].id
        print(f"✓ Found first user ID: {first_user_id}")
        print(f"  Existing records will be assigned to this user.")
        
        # Migrate each collection
        collections = ['ai_instructions', 'people', 'types', 'absences']
        
        print("\nApplying migrations...")
        for collection_name in collections:
            print(f"  - Migrating {collection_name} collection...")
            collection_ref = db.collection(collection_name)
            docs = collection_ref.stream()
            
            count = 0
            for doc in docs:
                data = doc.to_dict()
                if 'user_id' not in data or not data.get('user_id'):
                    doc.reference.update({'user_id': first_user_id})
                    count += 1
            
            print(f"    ✓ {collection_name}: updated {count} documents")
        
        print("\n✅ Firestore migration completed successfully!")
        return True
        
    except ImportError:
        print("❌ Error: google-cloud-firestore not installed")
        print("   Run: pip install google-cloud-firestore")
        return False
    except Exception as e:
        print(f"❌ Firestore migration failed: {e}")
        return False


def main():
    """Main migration function"""
    print("="* 60)
    print("Database Migration: Add user_id to tables")
    print("="* 60)
    print()
    
    environment = os.getenv("ENVIRONMENT", "production").lower()
    print(f"Environment: {environment}")
    print()
    
    if environment == "development":
        # SQLite migration
        # Find database.db in backend directory
        backend_dir = Path(__file__).parent
        db_path = backend_dir / "database.db"
        
        if not db_path.exists():
            print(f"❌ Error: Database not found at {db_path}")
            print("   Please run the application first to create the database.")
            return False
        
        success = migrate_sqlite(str(db_path))
    else:
        # Firestore migration
        success = migrate_firestore()
    
    if success:
        print()
        print("="* 60)
        print("✅ Migration completed successfully!")
        print("="* 60)
        print()
        print("Next steps:")
        print("  1. Restart your application")
        print("  2. Test data isolation by logging in as different users")
        print("  3. Verify that users can only see their own data")
    else:
        print()
        print("="* 60)
        print("❌ Migration failed")
        print("="* 60)
        sys.exit(1)


if __name__ == "__main__":
    main()
