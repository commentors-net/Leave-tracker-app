# Security Considerations

This application is a demonstration/starter project based on the README.md specification. Before deploying to production, consider the following security improvements:

## Critical Issues

### 1. Password Storage
**Current:** Passwords are stored in plain text in the database.

**Fix:** Use proper password hashing:
```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# When registering
hashed_password = pwd_context.hash(data.password)
user = User(username=data.username, password=hashed_password, otp_secret=secret)

# When verifying (add to login flow before 2FA check)
if not pwd_context.verify(plain_password, user.password):
    raise HTTPException(status_code=401, detail="Invalid credentials")
```

Add to requirements.txt:
```
passlib[bcrypt]
```

### 2. CORS Configuration
**Current:** Allows all origins (`allow_origins=["*"]`)

**Fix:** Restrict to specific frontend domains:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 3. Authentication & Authorization
**Current:** No session management or protected routes.

**Fix:** Implement JWT tokens:
```python
# After successful 2FA login, return a JWT
from jose import jwt
from datetime import datetime, timedelta

token = jwt.encode(
    {"sub": user.username, "exp": datetime.utcnow() + timedelta(hours=24)},
    SECRET_KEY,
    algorithm="HS256"
)
return {"access_token": token, "token_type": "bearer"}
```

Then protect routes with authentication dependency.

## Medium Priority Issues

### 4. Rate Limiting
Add rate limiting to prevent brute force attacks on login:
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@router.post("/login")
@limiter.limit("5/minute")
def login(request: Request, data: schemas.TokenData, db: Session = Depends(get_db)):
    # ... existing code
```

### 5. Input Validation
Add proper validation for:
- Username format (alphanumeric, length limits)
- Password strength requirements
- SQL injection prevention (SQLAlchemy handles this, but validate inputs)

### 6. HTTPS Only
Ensure the application only runs over HTTPS in production:
```python
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware

if not DEBUG:
    app.add_middleware(HTTPSRedirectMiddleware)
```

### 7. Environment Variables
Move sensitive configuration to environment variables:
```python
import os

SECRET_KEY = os.getenv("SECRET_KEY")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./database.db")
```

### 8. OTP Secret Protection
Consider encrypting OTP secrets in the database rather than storing them in plain text.

## Low Priority Issues

### 9. Error Messages
Don't reveal system details in error messages:
```python
# Bad
raise HTTPException(status_code=404, detail="User not found")

# Better
raise HTTPException(status_code=401, detail="Invalid credentials")
```

### 10. Database Backups
Implement regular database backups, especially if using SQLite in production.

### 11. Logging
Add proper logging for security events (failed logins, etc.)

### 12. Content Security Policy
Add CSP headers to prevent XSS attacks.

## Recommendations

For production deployment:
1. Use PostgreSQL instead of SQLite
2. Implement all security fixes above
3. Add automated security scanning (Dependabot, Snyk)
4. Regular security audits
5. Keep dependencies updated
6. Use secrets management (Google Secret Manager, AWS Secrets Manager)

## Note

This application was built following the examples in README.md as a demonstration project. The security issues listed above exist in the original specification and should be addressed before production use.
