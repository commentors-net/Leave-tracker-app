# JWT Authentication & Navigation Implementation

## Changes Summary

### Backend Changes

#### 1. **JWT Implementation** (`backend/app/core/security.py`)
- Added JWT token generation with `create_access_token()`
- Added JWT token verification with `verify_token()`
- Token expires after 30 minutes (configurable)
- Uses HS256 algorithm with secret key

#### 2. **Updated Login Endpoint** (`backend/app/api/auth.py`)
- Now returns JWT token on successful login
- Response includes:
  - `access_token`: JWT token for authenticated requests
  - `token_type`: "bearer"
  - `username`: logged in username
  - `success`: true

#### 3. **Dependencies** (`requirements.txt`)
- Added `python-multipart` for form data
- Added `passlib[bcrypt]` for password hashing utilities
- `python-jose[cryptography]` already included for JWT

### Frontend Changes

#### 1. **Register Page** (`frontend/src/pages/Register.tsx`)
- ✅ Shows QR code and secret after registration
- ✅ Added "Continue to Login" button
- ✅ Redirects to login page after registration complete
- Better UI with instructions

#### 2. **Login Page** (`frontend/src/pages/Login.tsx`)
- ✅ Stores JWT token in localStorage on successful login
- ✅ Stores username in localStorage
- ✅ Redirects to dashboard after successful login
- Better error messages

#### 3. **App Component** (`frontend/src/App.tsx`)
- ✅ Checks localStorage for existing login on mount
- ✅ Shows different navigation based on login status
- ✅ Displays "Welcome, {username}" when logged in
- ✅ Added Logout button that:
  - Clears localStorage
  - Redirects to login page
  - Updates UI state

## Test User Credentials

For testing, use:
- **Username**: `testuser123`
- **Password**: `TestPass@123`

## How to Test

### 1. Start Both Servers

Press **F5** in VS Code to start both backend and frontend

Or manually:
```powershell
# Terminal 1 - Backend
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2 - Frontend
cd frontend
npm run dev
```

### 2. Register a New User

1. Go to http://localhost:5173/register
2. Enter username and password
3. Click "Register"
4. **IMPORTANT**: Scan the QR code with Google Authenticator or similar app
5. Save the secret key (shown below QR code)
6. Click "Continue to Login"

### 3. Login

1. You'll be redirected to http://localhost:5173/login
2. Enter your username
3. Enter your password
4. Open your authenticator app and get the 6-digit code
5. Enter the 2FA token
6. Click "Login"
7. **You'll be automatically redirected to Dashboard**

### 4. Verify Login State

- Check the navigation bar shows "Welcome, {username}"
- Check Dashboard and Settings links are visible
- Logout button is available
- Login/Register buttons are hidden

### 5. Test Logout

1. Click "Logout" button
2. You'll be redirected to login page
3. Navigation changes back to Login/Register buttons

## API Testing (PowerShell)

### Register a User
```powershell
$body = @{username='testuser123';password='TestPass@123'} | ConvertTo-Json
Invoke-RestMethod -Uri 'http://localhost:8000/auth/register' -Method POST -Body $body -ContentType 'application/json'
```

### Login (with 2FA token)
```powershell
$body = @{username='testuser123';password='TestPass@123';token='123456'} | ConvertTo-Json
Invoke-RestMethod -Uri 'http://localhost:8000/auth/login' -Method POST -Body $body -ContentType 'application/json'
```

## Python Test Script

Run the test script to test registration and login:
```powershell
cd backend
python test_auth.py
```

This script will:
1. Register the test user
2. Display the 2FA secret
3. Prompt you for a 2FA token
4. Test login with JWT

## JWT Token Usage

The JWT token is stored in localStorage and can be used for authenticated API calls:

```javascript
// In frontend
const token = localStorage.getItem('access_token');

axios.get('http://localhost:8000/api/protected-endpoint', {
  headers: {
    'Authorization': `Bearer ${token}`
  }
});
```

## Security Notes

1. **JWT Secret Key**: Change the secret key in `backend/app/core/security.py` for production
2. **Token Expiration**: Tokens expire after 30 minutes
3. **HTTPS**: Always use HTTPS in production
4. **LocalStorage**: Consider using httpOnly cookies for more security in production

## Next Steps

To protect routes that require authentication:

1. **Backend**: Add authentication dependency
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthCredentials = Depends(security)):
    token = credentials.credentials
    username = verify_token(token)
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    return username

# Use in routes
@router.get("/protected")
async def protected_route(username: str = Depends(get_current_user)):
    return {"message": f"Hello {username}"}
```

2. **Frontend**: Create a ProtectedRoute component
```tsx
function ProtectedRoute({ children }) {
  const token = localStorage.getItem('access_token');
  if (!token) {
    return <Navigate to="/login" />;
  }
  return children;
}

// Use in App.tsx
<Route path="/dashboard" element={
  <ProtectedRoute>
    <Dashboard />
  </ProtectedRoute>
} />
```

## File Changes Summary

### Modified:
- `backend/requirements.txt` - Added JWT dependencies
- `backend/app/core/security.py` - Added JWT functions
- `backend/app/api/auth.py` - Updated login to return JWT
- `frontend/src/App.tsx` - Added login state management
- `frontend/src/pages/Login.tsx` - Added navigation after login
- `frontend/src/pages/Register.tsx` - Added navigation after registration

### Created:
- `backend/test_auth.py` - Test script for authentication
- This README file

## Common Issues

### Backend won't start
- Check if port 8000 is in use
- Verify all dependencies are installed: `pip install -r requirements.txt`

### Frontend navigation not working
- Clear browser localStorage
- Refresh the page
- Check browser console for errors

### 2FA token invalid
- Make sure time on your device is synchronized
- Check you're using the correct secret
- Try generating a new token

## Database

User data is stored in SQLite database at `backend/database.db`. The password field contains the encrypted username (not the actual password).

To reset and start fresh:
```powershell
Remove-Item backend\database.db
```

Then restart the backend server.
