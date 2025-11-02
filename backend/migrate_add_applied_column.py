"""
Migration script to add 'applied' column to absences table
"""

from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./leave_tracker.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

def migrate():
    print("Adding 'applied' column to absences table...")
    
    with engine.connect() as conn:
        try:
            # Check if column already exists
            result = conn.execute(text("PRAGMA table_info(absences)"))
            columns = [row[1] for row in result]
            
            if 'applied' in columns:
                print("✓ Column 'applied' already exists. Skipping migration.")
                return
            
            # Add the column
            conn.execute(text("ALTER TABLE absences ADD COLUMN applied INTEGER DEFAULT 0"))
            conn.commit()
            print("✓ Migration complete! Column 'applied' added successfully.")
            
        except Exception as e:
            print(f"✗ Migration failed: {e}")
            conn.rollback()

if __name__ == "__main__":
    migrate()
