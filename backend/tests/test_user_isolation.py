"""
Unit tests for user data isolation feature.
Tests that users can only access their own data across all API endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from datetime import date
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.main import app
from app.core.security import create_access_token, encrypt_username_with_password
from app.db_factory import db

client = TestClient(app)


@pytest.fixture(scope="module")
def test_users():
    """Create two test users for isolation testing"""
    # Create user 1
    user1_username = "test_user_1"
    user1_password = "password123"
    user1_encrypted = encrypt_username_with_password(user1_username, user1_password)
    user1 = db.create_user(user1_username, user1_encrypted, "test_secret_1")
    user1_token = create_access_token(data={"sub": user1_username})
    
    # Create user 2
    user2_username = "test_user_2"
    user2_password = "password456"
    user2_encrypted = encrypt_username_with_password(user2_username, user2_password)
    user2 = db.create_user(user2_username, user2_encrypted, "test_secret_2")
    user2_token = create_access_token(data={"sub": user2_username})
    
    return {
        "user1": {"id": user1["id"], "username": user1_username, "token": user1_token},
        "user2": {"id": user2["id"], "username": user2_username, "token": user2_token}
    }


class TestPeopleIsolation:
    """Test that people are isolated per user"""
    
    def test_create_person_user1(self, test_users):
        """User 1 creates a person"""
        response = client.post(
            "/api/people",
            headers={"Authorization": f"Bearer {test_users['user1']['token']}"},
            json={"name": "Alice (User 1)"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Alice (User 1)"
        assert "id" in data
        return data["id"]
    
    def test_create_person_user2(self, test_users):
        """User 2 creates a person"""
        response = client.post(
            "/api/people",
            headers={"Authorization": f"Bearer {test_users['user2']['token']}"},
            json={"name": "Bob (User 2)"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Bob (User 2)"
        assert "id" in data
    
    def test_user1_sees_only_own_people(self, test_users):
        """User 1 should only see their own people"""
        response = client.get(
            "/api/people",
            headers={"Authorization": f"Bearer {test_users['user1']['token']}"}
        )
        assert response.status_code == 200
        people = response.json()
        # User 1 should only see their own person
        assert all("User 1" in person["name"] or "Alice" in person["name"] for person in people)
        assert not any("User 2" in person["name"] or "Bob" in person["name"] for person in people)
    
    def test_user2_sees_only_own_people(self, test_users):
        """User 2 should only see their own people"""
        response = client.get(
            "/api/people",
            headers={"Authorization": f"Bearer {test_users['user2']['token']}"}
        )
        assert response.status_code == 200
        people = response.json()
        # User 2 should only see their own person
        assert all("User 2" in person["name"] or "Bob" in person["name"] for person in people)
        assert not any("User 1" in person["name"] or "Alice" in person["name"] for person in people)


class TestTypesIsolation:
    """Test that leave types are isolated per user"""
    
    def test_create_type_user1(self, test_users):
        """User 1 creates a leave type"""
        response = client.post(
            "/api/types",
            headers={"Authorization": f"Bearer {test_users['user1']['token']}"},
            json={"name": "Vacation (User 1)"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Vacation (User 1)"
        assert "id" in data
    
    def test_create_type_user2(self, test_users):
        """User 2 creates a leave type"""
        response = client.post(
            "/api/types",
            headers={"Authorization": f"Bearer {test_users['user2']['token']}"},
            json={"name": "Medical (User 2)"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Medical (User 2)"
        assert "id" in data
    
    def test_user1_sees_only_own_types(self, test_users):
        """User 1 should only see their own types"""
        response = client.get(
            "/api/types",
            headers={"Authorization": f"Bearer {test_users['user1']['token']}"}
        )
        assert response.status_code == 200
        types = response.json()
        # User 1 should only see their own types
        assert all("User 1" in t["name"] or "Vacation" in t["name"] for t in types)
        assert not any("User 2" in t["name"] or "Medical" in t["name"] for t in types)
    
    def test_user2_sees_only_own_types(self, test_users):
        """User 2 should only see their own types"""
        response = client.get(
            "/api/types",
            headers={"Authorization": f"Bearer {test_users['user2']['token']}"}
        )
        assert response.status_code == 200
        types = response.json()
        # User 2 should only see their own types
        assert all("User 2" in t["name"] or "Medical" in t["name"] for t in types)
        assert not any("User 1" in t["name"] or "Vacation" in t["name"] for t in types)


class TestAbsencesIsolation:
    """Test that absences are isolated per user"""
    
    def setup_test_data(self, test_users):
        """Helper to create test people and types for both users"""
        # Create person for user 1
        response = client.post(
            "/api/people",
            headers={"Authorization": f"Bearer {test_users['user1']['token']}"},
            json={"name": "Charlie (User 1)"}
        )
        person1_id = response.json()["id"]
        
        # Create type for user 1
        response = client.post(
            "/api/types",
            headers={"Authorization": f"Bearer {test_users['user1']['token']}"},
            json={"name": "Annual (User 1)"}
        )
        type1_id = response.json()["id"]
        
        # Create person for user 2
        response = client.post(
            "/api/people",
            headers={"Authorization": f"Bearer {test_users['user2']['token']}"},
            json={"name": "Diana (User 2)"}
        )
        person2_id = response.json()["id"]
        
        # Create type for user 2
        response = client.post(
            "/api/types",
            headers={"Authorization": f"Bearer {test_users['user2']['token']}"},
            json={"name": "Sick (User 2)"}
        )
        type2_id = response.json()["id"]
        
        return {
            "user1": {"person_id": person1_id, "type_id": type1_id},
            "user2": {"person_id": person2_id, "type_id": type2_id}
        }
    
    def test_create_absence_user1(self, test_users):
        """User 1 creates an absence"""
        test_data = self.setup_test_data(test_users)
        
        response = client.post(
            "/api/absences",
            headers={"Authorization": f"Bearer {test_users['user1']['token']}"},
            json={
                "date": "2025-01-15",
                "duration": "Full Day",
                "reason": "Vacation User 1",
                "type_id": test_data["user1"]["type_id"],
                "person_id": test_data["user1"]["person_id"],
                "applied": 0
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["reason"] == "Vacation User 1"
        assert "id" in data
    
    def test_create_absence_user2(self, test_users):
        """User 2 creates an absence"""
        test_data = self.setup_test_data(test_users)
        
        response = client.post(
            "/api/absences",
            headers={"Authorization": f"Bearer {test_users['user2']['token']}"},
            json={
                "date": "2025-01-16",
                "duration": "Half Day",
                "reason": "Medical User 2",
                "type_id": test_data["user2"]["type_id"],
                "person_id": test_data["user2"]["person_id"],
                "applied": 0
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["reason"] == "Medical User 2"
        assert "id" in data
    
    def test_user1_sees_only_own_absences(self, test_users):
        """User 1 should only see their own absences"""
        response = client.get(
            "/api/absences",
            headers={"Authorization": f"Bearer {test_users['user1']['token']}"}
        )
        assert response.status_code == 200
        absences = response.json()
        # User 1 should only see their own absences
        assert all("User 1" in absence.get("reason", "") for absence in absences if absence.get("reason"))
        assert not any("User 2" in absence.get("reason", "") for absence in absences if absence.get("reason"))
    
    def test_user2_sees_only_own_absences(self, test_users):
        """User 2 should only see their own absences"""
        response = client.get(
            "/api/absences",
            headers={"Authorization": f"Bearer {test_users['user2']['token']}"}
        )
        assert response.status_code == 200
        absences = response.json()
        # User 2 should only see their own absences
        assert all("User 2" in absence.get("reason", "") for absence in absences if absence.get("reason"))
        assert not any("User 1" in absence.get("reason", "") for absence in absences if absence.get("reason"))


class TestAIInstructionsIsolation:
    """Test that AI instructions are isolated per user"""
    
    def test_create_ai_instructions_user1(self, test_users):
        """User 1 creates AI instructions"""
        response = client.put(
            "/api/ai-instructions",
            headers={"Authorization": f"Bearer {test_users['user1']['token']}"},
            json={"instructions": "Custom rules for User 1"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "Custom rules for User 1" in data["instructions"]
    
    def test_create_ai_instructions_user2(self, test_users):
        """User 2 creates AI instructions"""
        response = client.put(
            "/api/ai-instructions",
            headers={"Authorization": f"Bearer {test_users['user2']['token']}"},
            json={"instructions": "Custom rules for User 2"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "Custom rules for User 2" in data["instructions"]
    
    def test_user1_sees_only_own_instructions(self, test_users):
        """User 1 should only see their own AI instructions"""
        response = client.get(
            "/api/ai-instructions",
            headers={"Authorization": f"Bearer {test_users['user1']['token']}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "User 1" in data["instructions"]
        assert "User 2" not in data["instructions"]
    
    def test_user2_sees_only_own_instructions(self, test_users):
        """User 2 should only see their own AI instructions"""
        response = client.get(
            "/api/ai-instructions",
            headers={"Authorization": f"Bearer {test_users['user2']['token']}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "User 2" in data["instructions"]
        assert "User 1" not in data["instructions"]


class TestSecurityViolations:
    """Test that users cannot access other users' data"""
    
    def test_cannot_update_other_user_person(self, test_users):
        """User 2 should not be able to update User 1's person"""
        # Create person as User 1
        response = client.post(
            "/api/people",
            headers={"Authorization": f"Bearer {test_users['user1']['token']}"},
            json={"name": "Secure Person"}
        )
        person_id = response.json()["id"]
        
        # Try to update as User 2
        response = client.put(
            f"/api/people/{person_id}",
            headers={"Authorization": f"Bearer {test_users['user2']['token']}"},
            json={"name": "Hacked Name"}
        )
        # Should fail or return not found
        assert response.status_code in [404, 403]
    
    def test_cannot_delete_other_user_type(self, test_users):
        """User 2 should not be able to delete User 1's type"""
        # Create type as User 1
        response = client.post(
            "/api/types",
            headers={"Authorization": f"Bearer {test_users['user1']['token']}"},
            json={"name": "Secure Type"}
        )
        type_id = response.json()["id"]
        
        # Try to delete as User 2
        response = client.delete(
            f"/api/types/{type_id}",
            headers={"Authorization": f"Bearer {test_users['user2']['token']}"}
        )
        # Should fail or return not found
        assert response.status_code in [404, 403]
    
    def test_cannot_delete_other_user_absence(self, test_users):
        """User 2 should not be able to delete User 1's absence"""
        # Setup test data for User 1
        response = client.post(
            "/api/people",
            headers={"Authorization": f"Bearer {test_users['user1']['token']}"},
            json={"name": "Person For Absence"}
        )
        person_id = response.json()["id"]
        
        response = client.post(
            "/api/types",
            headers={"Authorization": f"Bearer {test_users['user1']['token']}"},
            json={"name": "Type For Absence"}
        )
        type_id = response.json()["id"]
        
        # Create absence as User 1
        response = client.post(
            "/api/absences",
            headers={"Authorization": f"Bearer {test_users['user1']['token']}"},
            json={
                "date": "2025-02-01",
                "duration": "Full Day",
                "reason": "Protected absence",
                "type_id": type_id,
                "person_id": person_id,
                "applied": 0
            }
        )
        absence_id = response.json()["id"]
        
        # Try to delete as User 2
        response = client.delete(
            f"/api/absences/{absence_id}",
            headers={"Authorization": f"Bearer {test_users['user2']['token']}"}
        )
        # Should fail or return not found
        assert response.status_code in [404, 403]


class TestAuthenticationRequired:
    """Test that authentication is required for all endpoints"""
    
    def test_get_people_requires_auth(self):
        """Getting people should require authentication"""
        response = client.get("/api/people")
        assert response.status_code == 403
    
    def test_get_types_requires_auth(self):
        """Getting types should require authentication"""
        response = client.get("/api/types")
        assert response.status_code == 403
    
    def test_get_absences_requires_auth(self):
        """Getting absences should require authentication"""
        response = client.get("/api/absences")
        assert response.status_code == 403
    
    def test_create_person_requires_auth(self):
        """Creating a person should require authentication"""
        response = client.post("/api/people", json={"name": "Unauthorized"})
        assert response.status_code == 403
    
    def test_create_absence_requires_auth(self):
        """Creating an absence should require authentication"""
        response = client.post(
            "/api/absences",
            json={
                "date": "2025-01-01",
                "duration": "Full Day",
                "reason": "Unauthorized",
                "type_id": "fake",
                "person_id": "fake",
                "applied": 0
            }
        )
        assert response.status_code == 403


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
