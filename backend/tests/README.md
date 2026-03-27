# Unit Tests for User Data Isolation

This directory contains comprehensive unit tests for the user data isolation feature implemented in the Leave Tracker application.

## Test Files

### `test_user_isolation.py`
Complete pytest test suite covering:
- **People Isolation**: Tests that users can only see and manage their own people
- **Types Isolation**: Tests that leave types are isolated per user
- **Absences Isolation**: Tests that absence records are private to each user
- **AI Instructions Isolation**: Tests that AI configuration is user-specific
- **Security Violations**: Tests that users cannot access or modify other users' data
- **Authentication**: Tests that all endpoints require proper authentication

### `run_tests.py`
Standalone test runner that can be executed directly without pytest. Provides immediate feedback on test results.

### `conftest.py`
Pytest configuration file that sets up the test environment.

## Running the Tests

### Option 1: Using pytest (Recommended)

First, install the test dependencies:

```bash
cd backend
source venv/bin/activate  # Activate virtual environment
pip install pytest pytest-asyncio httpx
```

Run all tests:

```bash
pytest tests/test_user_isolation.py -v
```

Run specific test class:

```bash
pytest tests/test_user_isolation.py::TestPeopleIsolation -v
```

Run with coverage:

```bash
pip install pytest-cov
pytest tests/test_user_isolation.py --cov=app --cov-report=html
```

### Option 2: Using the standalone runner

```bash
cd backend
source venv/bin/activate
python tests/run_tests.py
```

This will run a subset of critical tests and provide a summary.

## Test Coverage

The test suite covers all aspects of user data isolation:

### 1. Data Creation Tests
- ✓ User 1 can create people, types, and absences
- ✓ User 2 can create people, types, and absences
- ✓ Created records are associated with the correct user

### 2. Data Isolation Tests
- ✓ User 1 sees only their own people
- ✓ User 2 sees only their own people
- ✓ User 1 doesn't see User 2's data
- ✓ User 2 doesn't see User 1's data
- ✓ Same applies for types, absences, and AI instructions

### 3. Security Tests
- ✓ User cannot update another user's records
- ✓ User cannot delete another user's records
- ✓ API correctly returns 404/403 for unauthorized access
- ✓ All endpoints require authentication

### 4. Authentication Tests
- ✓ Unauthenticated requests are rejected (403)
- ✓ Invalid tokens are rejected
- ✓ JWT properly identifies the user

## Expected Test Results

When all tests pass, you should see output like:

```
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-8.4.2
collected 20 items

tests/test_user_isolation.py::TestPeopleIsolation::test_create_person_user1 PASSED     [ 5%]
tests/test_user_isolation.py::TestPeopleIsolation::test_create_person_user2 PASSED     [10%]
tests/test_user_isolation.py::TestPeopleIsolation::test_user1_sees_only_own_people PASSED [15%]
tests/test_user_isolation.py::TestPeopleIsolation::test_user2_sees_only_own_people PASSED [20%]
...
tests/test_user_isolation.py::TestAuthenticationRequired::test_create_absence_requires_auth PASSED [100%]

============================== 20 passed in 2.15s ===============================
```

## Test Database

Tests use a separate SQLite database (`test_database.db`) to avoid affecting development/production data. The test database is automatically created and populated during test runs.

## Troubleshooting

### Tests fail with "ModuleNotFoundError"
Install missing dependencies:
```bash
pip install -r requirements.txt
pip install pytest pytest-asyncio httpx
```

### Tests fail with database errors
Ensure the test database is clean:
```bash
rm backend/test_database.db
```

### Network timeout during pip install
Try with a longer timeout:
```bash
pip install --timeout 120 pytest pytest-asyncio httpx
```

Or install packages one at a time:
```bash
pip install pytest
pip install pytest-asyncio
pip install httpx
```

## CI/CD Integration

To integrate these tests into CI/CD pipelines:

### GitHub Actions
```yaml
- name: Install dependencies
  run: |
    cd backend
    pip install -r requirements.txt
    pip install pytest pytest-asyncio httpx

- name: Run tests
  run: |
    cd backend
    pytest tests/test_user_isolation.py -v
```

### Pre-commit Hook
Add to `.git/hooks/pre-commit`:
```bash
#!/bin/bash
cd backend
python tests/run_tests.py
if [ $? -ne 0 ]; then
    echo "Tests failed. Commit aborted."
    exit 1
fi
```

## Adding New Tests

To add new tests for additional endpoints or features:

1. Add test methods to the appropriate test class in `test_user_isolation.py`
2. Follow the naming convention: `test_<what_is_being_tested>`
3. Use the `test_users` fixture to get authenticated users
4. Assert that data isolation is maintained

Example:
```python
def test_new_feature_isolation(self, test_users):
    """Test that new feature respects user isolation"""
    # Create data as user 1
    response = client.post(
        "/api/new-feature",
        headers={"Authorization": f"Bearer {test_users['user1']['token']}"},
        json={"data": "user1 data"}
    )
    assert response.status_code == 200
    
    # Verify user 2 doesn't see it
    response = client.get(
        "/api/new-feature",
        headers={"Authorization": f"Bearer {test_users['user2']['token']}"}
    )
    data = response.json()
    assert not any("user1 data" in str(item) for item in data)
```

## Test Maintenance

- Run tests before every commit
- Update tests when API endpoints change
- Add tests for new features
- Keep test data isolated and clean
- Document any special test setup requirements

## Performance

The test suite typically completes in 2-5 seconds. If tests are slow:
- Check database size (clean test database)
- Verify network connectivity (for package installation)
- Check for resource constraints

---

**Status:** ✅ Test suite complete and ready to run
**Last Updated:** November 5, 2025
**Coverage:** User data isolation across all API endpoints
