#!/usr/bin/env python3
"""
Simple test runner for user isolation tests (without pytest dependency).
This script can be run directly to verify the tests pass.
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Set test environment
os.environ["ENVIRONMENT"] = "development"
os.environ["SECRET_KEY"] = "test-secret-key-for-testing-only"

from fastapi.testclient import TestClient
from app.main import app
from app.core.security import create_access_token, encrypt_username_with_password
from app.db_factory import db
from app.database import Base, engine
from app import models

# Initialize database
Base.metadata.create_all(bind=engine)

client = TestClient(app)

print("=" * 70)
print("USER DATA ISOLATION TESTS")
print("=" * 70)

# Create test users
print("\n[Setup] Creating test users...")
user1_username = "test_iso_user_1"
user1_password = "password123"
user1_encrypted = encrypt_username_with_password(user1_username, user1_password)

try:
    user1 = db.create_user(user1_username, user1_encrypted, "test_secret_1")
    user1_token = create_access_token(data={"sub": user1_username})
    print(f"✓ Created User 1: {user1_username}")
except Exception as e:
    # User might already exist
    user1 = db.get_user_by_username(user1_username)
    user1_token = create_access_token(data={"sub": user1_username})
    print(f"✓ Using existing User 1: {user1_username}")

user2_username = "test_iso_user_2"
user2_password = "password456"
user2_encrypted = encrypt_username_with_password(user2_username, user2_password)

try:
    user2 = db.create_user(user2_username, user2_encrypted, "test_secret_2")
    user2_token = create_access_token(data={"sub": user2_username})
    print(f"✓ Created User 2: {user2_username}")
except Exception as e:
    # User might already exist
    user2 = db.get_user_by_username(user2_username)
    user2_token = create_access_token(data={"sub": user2_username})
    print(f"✓ Using existing User 2: {user2_username}")

test_results = []

def test(name, condition, message=""):
    """Helper function to track test results"""
    result = "✓ PASS" if condition else "✗ FAIL"
    test_results.append((name, condition))
    status_msg = f"{result}: {name}"
    if message:
        status_msg += f" - {message}"
    print(status_msg)
    return condition

# Test 1: Create people for each user
print("\n[Test 1] Creating people for each user...")
response1 = client.post(
    "/api/people",
    headers={"Authorization": f"Bearer {user1_token}"},
    json={"name": "Test Person User 1"}
)
test("User 1 can create person", response1.status_code == 200)

response2 = client.post(
    "/api/people",
    headers={"Authorization": f"Bearer {user2_token}"},
    json={"name": "Test Person User 2"}
)
test("User 2 can create person", response2.status_code == 200)

# Test 2: Verify data isolation - People
print("\n[Test 2] Verifying people data isolation...")
people1 = client.get("/api/people", headers={"Authorization": f"Bearer {user1_token}"}).json()
people2 = client.get("/api/people", headers={"Authorization": f"Bearer {user2_token}"}).json()

user1_only = all("User 1" in p["name"] for p in people1 if "Test Person" in p["name"])
user2_only = all("User 2" in p["name"] for p in people2 if "Test Person" in p["name"])

test("User 1 sees only their people", user1_only)
test("User 2 sees only their people", user2_only)
test("User 1 doesn't see User 2's people", not any("User 2" in p["name"] for p in people1))
test("User 2 doesn't see User 1's people", not any("User 1" in p["name"] for p in people2))

# Test 3: Create types for each user
print("\n[Test 3] Creating types for each user...")
response1 = client.post(
    "/api/types",
    headers={"Authorization": f"Bearer {user1_token}"},
    json={"name": "Test Type User 1"}
)
test("User 1 can create type", response1.status_code == 200)

response2 = client.post(
    "/api/types",
    headers={"Authorization": f"Bearer {user2_token}"},
    json={"name": "Test Type User 2"}
)
test("User 2 can create type", response2.status_code == 200)

# Test 4: Verify data isolation - Types
print("\n[Test 4] Verifying types data isolation...")
types1 = client.get("/api/types", headers={"Authorization": f"Bearer {user1_token}"}).json()
types2 = client.get("/api/types", headers={"Authorization": f"Bearer {user2_token}"}).json()

user1_types_only = all("User 1" in t["name"] for t in types1 if "Test Type" in t["name"])
user2_types_only = all("User 2" in t["name"] for t in types2 if "Test Type" in t["name"])

test("User 1 sees only their types", user1_types_only)
test("User 2 sees only their types", user2_types_only)
test("User 1 doesn't see User 2's types", not any("User 2" in t["name"] for t in types1))
test("User 2 doesn't see User 1's types", not any("User 1" in t["name"] for t in types2))

# Test 5: Authentication is required
print("\n[Test 5] Verifying authentication is required...")
response = client.get("/api/people")
test("Get people requires auth", response.status_code == 403)

response = client.get("/api/types")
test("Get types requires auth", response.status_code == 403)

response = client.get("/api/absences")
test("Get absences requires auth", response.status_code == 403)

# Test 6: Try to access another user's data
print("\n[Test 6] Verifying cross-user security...")
# Get user 1's person ID
people1 = client.get("/api/people", headers={"Authorization": f"Bearer {user1_token}"}).json()
if people1:
    person1_id = people1[0]["id"]
    
    # Try to update as user 2
    response = client.put(
        f"/api/people/{person1_id}",
        headers={"Authorization": f"Bearer {user2_token}"},
        json={"name": "Hacked"}
    )
    test("User 2 cannot update User 1's person", response.status_code in [404, 403])

# Summary
print("\n" + "=" * 70)
print("TEST SUMMARY")
print("=" * 70)
passed = sum(1 for _, result in test_results if result)
failed = sum(1 for _, result in test_results if not result)
total = len(test_results)

print(f"Total Tests: {total}")
print(f"Passed: {passed} ✓")
print(f"Failed: {failed} ✗")
print(f"Success Rate: {(passed/total*100):.1f}%")

if failed == 0:
    print("\n🎉 ALL TESTS PASSED! User data isolation is working correctly.")
    sys.exit(0)
else:
    print("\n⚠️  SOME TESTS FAILED. Please review the failures above.")
    sys.exit(1)
