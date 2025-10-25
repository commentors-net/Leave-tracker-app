# Security Implementation - JWT Authentication & API Service Layer

## Summary of Changes

This document describes the complete implementation of JWT authentication on the backend and the refactored API service layer on the frontend.

---

## 1. Backend - JWT Authentication Implementation

### ✅ What Was Implemented

All API endpoints (except auth) are now protected with JWT Bearer token authentication.

### Changes Made

#### A. Security Module (`backend/app/core/security.py`)

**Added:**
1. `HTTPBearer` security scheme
2. `get_current_user()` FastAPI dependency

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    FastAPI dependency to validate JWT tokens.
    Raises 401 if token is invalid or expired.
    """
    token = credentials.credentials
    username = verify_token(token)
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return username
```

#### B. Protected Endpoints

**People API** (`backend/app/api/people.py`)
- ✅ GET `/api/people` - Requires JWT
- ✅ POST `/api/people` - Requires JWT
- ✅ PUT `/api/people/{id}` - Requires JWT
- ✅ DELETE `/api/people/{id}` - Requires JWT

**Types API** (`backend/app/api/types.py`)
- ✅ GET `/api/types` - Requires JWT
- ✅ POST `/api/types` - Requires JWT
- ✅ PUT `/api/types/{id}` - Requires JWT
- ✅ DELETE `/api/types/{id}` - Requires JWT

**Absences API** (`backend/app/api/absences.py`)
- ✅ GET `/api/absences` - Requires JWT
- ✅ POST `/api/absences` - Requires JWT

All endpoints now include:
```python
current_user: str = Depends(get_current_user)
```

### How It Works

1. **Client makes request** with `Authorization: Bearer <token>` header
2. **FastAPI calls** `get_current_user()` dependency before endpoint handler
3. **Dependency extracts** token from Authorization header
4. **Token is verified** using `verify_token()` (checks signature and expiration)
5. **If valid**: Username returned, endpoint executes
6. **If invalid**: 401 Unauthorized response immediately

---

## 2. Frontend - API Service Layer Refactoring

### ✅ What Was Implemented

Created centralized API service with automatic JWT token management.

### Changes Made

#### A. New API Service (`frontend/src/services/api.ts`)

**Features:**
1. **Centralized axios instance** with automatic JWT injection
2. **Request interceptor** - Adds `Authorization: Bearer <token>` to all requests
3. **Response interceptor** - Handles 401 errors (token expired)
4. **Type-safe API functions** for all endpoints

**Structure:**
```typescript
frontend/src/services/
└── api.ts
    ├── apiClient (configured axios instance)
    ├── authApi (register, login, changePassword)
    ├── peopleApi (getAll, create, update, delete)
    ├── typesApi (getAll, create, update, delete)
    └── absencesApi (getAll, create)
```

**Request Interceptor:**
```typescript
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access_token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  }
);
```

**Response Interceptor:**
```typescript
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired - clear and redirect
      localStorage.removeItem("access_token");
      localStorage.removeItem("username");
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);
```

#### B. Updated Components

**Login** (`frontend/src/pages/Login.tsx`)
- ❌ Before: `axios.post(config.endpoints.auth.login, ...)`
- ✅ After: `authApi.login({ username, password, token })`

**Register** (`frontend/src/pages/Register.tsx`)
- ❌ Before: `axios.post(config.endpoints.auth.register, ...)`
- ✅ After: `authApi.register({ username, password })`

**Dashboard** (`frontend/src/pages/Dashboard.tsx`)
- ❌ Before: Direct axios calls with config URLs
- ✅ After: `peopleApi.getAll()`, `typesApi.getAll()`, `absencesApi.create()`
- ✅ Added proper TypeScript types
- ✅ JWT automatically included in all requests

**Settings** (`frontend/src/pages/Settings.tsx`)
- ❌ Before: Direct axios calls with config URLs
- ✅ After: `peopleApi` and `typesApi` methods
- ✅ Cleaner code: `await peopleApi.create({ name })` vs `await axios.post(url, { name })`
- ✅ JWT automatically included

### Benefits

1. **No manual JWT handling** - Interceptor handles everything
2. **Type safety** - All API calls are typed
3. **DRY principle** - No repeated axios calls in components
4. **Centralized error handling** - 401 handled in one place
5. **Easy to extend** - Add new endpoints in one file
6. **Testable** - Mock `api.ts` instead of mocking axios everywhere

---

## 3. Authentication Flow

### Registration Flow
```
User enters credentials
    ↓
authApi.register({ username, password })
    ↓
POST /auth/register (no JWT needed)
    ↓
Backend creates user + JWT token
    ↓
← { access_token, qr, secret, username }
    ↓
Frontend stores access_token in localStorage
    ↓
User scans QR and continues to login
```

### Login Flow
```
User enters credentials + 2FA token
    ↓
authApi.login({ username, password, token })
    ↓
POST /auth/login (no JWT needed)
    ↓
Backend validates password + 2FA token
    ↓
← { access_token, token_type, username }
    ↓
Frontend stores access_token in localStorage
    ↓
Navigate to /dashboard
```

### Protected API Call Flow
```
Component calls peopleApi.getAll()
    ↓
Request interceptor adds: Authorization: Bearer <token>
    ↓
GET /api/people with JWT header
    ↓
Backend: get_current_user() validates token
    ↓
If valid: Return data
If invalid (401): Response interceptor catches it
    ↓
Clear localStorage + redirect to /login
```

---

## 4. File Changes Summary

### Backend Files Modified
- ✅ `backend/app/core/security.py` - Added `get_current_user()` dependency
- ✅ `backend/app/api/people.py` - Added JWT protection
- ✅ `backend/app/api/types.py` - Added JWT protection
- ✅ `backend/app/api/absences.py` - Added JWT protection

### Frontend Files Created
- ✅ `frontend/src/services/api.ts` - NEW centralized API service

### Frontend Files Modified
- ✅ `frontend/src/pages/Login.tsx` - Uses `authApi.login()`
- ✅ `frontend/src/pages/Register.tsx` - Uses `authApi.register()`
- ✅ `frontend/src/pages/Dashboard.tsx` - Uses `peopleApi`, `typesApi`, `absencesApi`
- ✅ `frontend/src/pages/Settings.tsx` - Uses `peopleApi`, `typesApi`

---

## 5. Testing

### Backend JWT Protection Test

```bash
# 1. Try accessing protected endpoint without token (should fail)
curl http://localhost:8000/api/people
# Response: {"detail":"Not authenticated"}

# 2. Login to get token
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser123","password":"TestPass@123","token":"123456"}'
# Response: {"access_token":"eyJ...","token_type":"bearer","username":"testuser123"}

# 3. Use token to access protected endpoint (should work)
curl http://localhost:8000/api/people \
  -H "Authorization: Bearer eyJ..."
# Response: [{"id":1,"name":"John Doe"}]
```

### Frontend API Service Test

1. Open browser DevTools → Application → Local Storage
2. Clear localStorage
3. Try accessing Dashboard → Should redirect to login
4. Login successfully → Check localStorage for `access_token`
5. Navigate to Dashboard → Check Network tab for `Authorization: Bearer ...` header
6. Manually delete `access_token` from localStorage
7. Refresh page → Should redirect to login

---

## 6. Security Benefits

### Before Implementation
- ❌ All API endpoints publicly accessible
- ❌ No authentication required
- ❌ Anyone could modify data

### After Implementation
- ✅ All API endpoints protected with JWT
- ✅ Token required for every request
- ✅ Token expires after 30 minutes
- ✅ Automatic logout on token expiration
- ✅ Secure token validation on server
- ✅ Stateless authentication (no session storage)

---

## 7. Code Quality Improvements

### Before Refactoring
```typescript
// Repeated in every component
const response = await axios.post("http://localhost:8000/api/people", data);
// No types
// No centralized error handling
// No automatic JWT inclusion
```

### After Refactoring
```typescript
// Clean and simple
const person = await peopleApi.create(data);
// Fully typed
// Centralized error handling
// JWT automatically included
```

---

## 8. Next Steps (Optional Enhancements)

### Refresh Tokens
- Implement long-lived refresh tokens
- Auto-refresh access tokens before expiration

### Role-Based Access Control (RBAC)
- Add roles to JWT claims (admin, user, etc.)
- Restrict endpoints based on roles

### Token Blacklist
- Add ability to revoke tokens before expiration
- Track logged-out users

### API Rate Limiting
- Limit requests per user
- Prevent abuse

---

## Conclusion

✅ **Backend**: All protected endpoints now require JWT authentication via `Depends(get_current_user)`

✅ **Frontend**: Centralized API service with automatic JWT management via axios interceptors

✅ **Security**: Complete authentication flow from login → token storage → automatic inclusion → validation → expiration handling

✅ **Code Quality**: Clean, maintainable, type-safe API layer that follows best practices

The application now has production-ready JWT authentication with proper separation of concerns!
