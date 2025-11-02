"""
Run database migration to add 'applied' column
This script can be executed on Cloud Run to update the production database
"""

import os
from sqlalchemy import create_engine, text

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("❌ ERROR: DATABASE_URL not set")
    exit(1)

print(f"🔧 Connecting to database...")
engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as conn:
        # Check if column already exists
        result = conn.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='absences' AND column_name='applied'
        """))
        
        if result.fetchone():
            print("✓ Column 'applied' already exists. No migration needed.")
        else:
            # Add the column
            print("Adding 'applied' column...")
            conn.execute(text("""
                ALTER TABLE absences 
                ADD COLUMN applied INTEGER DEFAULT 0
            """))
            conn.commit()
            print("✅ Migration complete! Column 'applied' added successfully.")
            
except Exception as e:
    print(f"❌ Migration failed: {e}")
    exit(1)
