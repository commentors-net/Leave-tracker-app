# Password Security Implementation

## Overview

This application uses a **unique password encryption approach** where:
- **The password itself is NEVER stored** in the database
- The username is encrypted using the password as the encryption key
- Only the encrypted result is stored in the password column
- Password recovery is **impossible** by design - only password reset is available

## How It Works

### 1. **Registration Process**
When a user registers:
```python
# User provides: username="john", password="MySecret123"
# System does:
1. Derives encryption key from password using SHA-256
2. Encrypts the username using Fernet symmetric encryption
3. Stores encrypted_username in the password column
```

**Database stores:**
- `username`: "john" (plaintext)
- `password`: "gAAAAABk..." (encrypted username)
- `otp_secret`: "..." (2FA secret)

### 2. **Login Process**
When a user logs in:
```python
# User provides: username="john", password="MySecret123", token="123456"
# System does:
1. Derives encryption key from provided password
2. Attempts to decrypt the stored value
3. Checks if decrypted value matches the username
4. If match → password is correct
5. Then verifies 2FA token
```

### 3. **Password Change**
```python
# User provides: old_password, new_password
# System does:
1. Verifies old password by decrypting
2. Re-encrypts username with new password
3. Updates database with new encrypted value
```

## Security Features

### ✅ **Advantages**

1. **No Password Storage**: The actual password is never stored anywhere
2. **Rainbow Table Resistant**: No hash to crack, each user has unique encryption
3. **No Plaintext Exposure**: Even with database access, passwords cannot be retrieved
4. **Breach Protection**: Database dump reveals nothing about actual passwords
5. **No Salt Needed**: Each user's encryption is unique by design

### ⚠️ **Important Considerations**

1. **No Password Recovery**: If a user forgets their password, it cannot be recovered
   - Must create a new password (requires admin intervention or reset mechanism)
   
2. **Username is Fixed**: Changing username requires password (since username is encrypted)

3. **Performance**: Encryption/decryption on each login (minimal overhead with modern CPUs)

## API Endpoints

### POST `/auth/register`
Register a new user with encrypted password.

**Request:**
```json
{
  "username": "john",
  "password": "MySecret123"
}
```

**Response:**
```json
{
  "id": 1,
  "username": "john",
  "qr": "base64_qr_image",
  "secret": "OTP_SECRET"
}
```

### POST `/auth/login`
Login with username, password, and 2FA token.

**Request:**
```json
{
  "username": "john",
  "password": "MySecret123",
  "token": "123456"
}
```

**Response:**
```json
{
  "success": true
}
```

### POST `/auth/change-password`
Change user password (requires old password).

**Request:**
```json
{
  "username": "john",
  "old_password": "MySecret123",
  "new_password": "NewSecret456"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Password changed successfully"
}
```

## Code Examples

### Encrypting a Password (Registration)
```python
from app.core.security import encrypt_username_with_password

username = "john"
password = "MySecret123"

# This is what gets stored in the database
encrypted = encrypt_username_with_password(username, password)
# Result: "gAAAAABk1x..." (encrypted username)
```

### Verifying a Password (Login)
```python
from app.core.security import verify_password

username = "john"
password_attempt = "MySecret123"
stored_encrypted = "gAAAAABk1x..."  # from database

# Returns True if password is correct
is_valid = verify_password(username, password_attempt, stored_encrypted)
```

### Changing a Password
```python
from app.core.security import change_password

username = "john"
old_password = "MySecret123"
new_password = "NewSecret456"
stored_encrypted = "gAAAAABk1x..."  # from database

# Returns new encrypted value or raises ValueError if old password is wrong
new_encrypted = change_password(username, old_password, new_password, stored_encrypted)
```

## Technical Details

### Encryption Method
- **Algorithm**: Fernet (symmetric encryption)
- **Key Derivation**: SHA-256 hash of password
- **Library**: Python `cryptography` package

### Key Derivation Function
```python
def derive_key_from_password(password: str) -> bytes:
    key = hashlib.sha256(password.encode()).digest()  # 32 bytes
    return base64.urlsafe_b64encode(key)  # Fernet-compatible format
```

### Why This Approach?

Traditional password storage uses **one-way hashing** (bcrypt, argon2):
- Password → Hash → Store hash
- Login: Hash provided password and compare

This approach uses **symmetric encryption**:
- Username + Password → Encrypted username → Store encrypted
- Login: Decrypt with provided password and verify

**Benefits over traditional hashing:**
1. No brute-force attacks on hash (no hash exists)
2. Each user's "encryption scheme" is unique
3. Database breach reveals nothing usable
4. Simple to implement and understand

## Migration from Existing System

If you have an existing system with plain passwords:

```python
from app.core.security import encrypt_username_with_password

# For each user in database:
for user in users:
    encrypted = encrypt_username_with_password(user.username, user.password)
    user.password = encrypted
    db.commit()
```

## Testing

```python
# Test encryption/decryption
username = "test_user"
password = "test_pass"

encrypted = encrypt_username_with_password(username, password)
assert verify_password(username, password, encrypted) == True
assert verify_password(username, "wrong_pass", encrypted) == False

# Test password change
new_encrypted = change_password(username, password, "new_pass", encrypted)
assert verify_password(username, "new_pass", new_encrypted) == True
assert verify_password(username, password, new_encrypted) == False
```

## Security Notes

1. **Transport Security**: Always use HTTPS in production
2. **Rate Limiting**: Implement login attempt limiting
3. **2FA Required**: This system includes 2FA (TOTP) as additional security layer
4. **Database Encryption**: Consider encrypting database at rest for additional security
5. **Key Management**: The password is the key - treat it accordingly

## FAQ

**Q: What if a user forgets their password?**
A: Password cannot be recovered. Implement a password reset flow that creates a new password.

**Q: Can I add password hints?**
A: No - that would defeat the purpose. No information about the password should be stored.

**Q: Is this more secure than bcrypt?**
A: Different approach. Both are secure if implemented correctly. This method has unique benefits for certain threat models.

**Q: What about quantum computers?**
A: SHA-256 and Fernet use quantum-resistant algorithms for current practical purposes.

**Q: Can I change the username?**
A: Yes, but you need the password to re-encrypt. Add an endpoint similar to password change.

## Production Recommendations

1. **Add Rate Limiting**: Prevent brute force attempts
2. **Add Logging**: Track login attempts and failures
3. **Add Password Strength**: Enforce minimum password requirements
4. **Add Session Management**: Implement proper JWT or session tokens
5. **Add Account Lockout**: Lock account after X failed attempts
6. **Add Admin Reset**: Allow admins to reset user passwords (creates new password)

## License

This implementation is part of the Leave Tracker Application.
