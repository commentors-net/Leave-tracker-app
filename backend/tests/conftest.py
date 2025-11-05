"""
Pytest configuration for user data isolation tests
"""
import pytest
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Set environment to development for testing
os.environ["ENVIRONMENT"] = "development"
os.environ["SECRET_KEY"] = "test-secret-key-for-testing-only"
os.environ["DATABASE_URL"] = "sqlite:///./test_database.db"


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Setup test environment before running tests"""
    # Ensure we're using SQLite for tests
    os.environ["ENVIRONMENT"] = "development"
    
    # Import and create tables
    from app.database import Base, engine
    from app import models
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    yield
    
    # Cleanup after tests (optional)
    # Base.metadata.drop_all(bind=engine)
