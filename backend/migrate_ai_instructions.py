"""
Migration script to add AIInstructions table
Run this after updating models.py
"""
from app.database import engine, Base
from app.models import AIInstructions

def migrate():
    print("Creating AIInstructions table...")
    Base.metadata.create_all(bind=engine)
    print("✓ Migration complete!")

if __name__ == "__main__":
    migrate()
