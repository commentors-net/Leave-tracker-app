"""
Test script to register and login a user
Run this after starting the backend server
"""
import requests
import json

BASE_URL = "http://localhost:8000"

# Test user credentials
username = "testuser123"
password = "TestPass@123"

print("=== Testing User Registration ===")
try:
    response = requests.post(
        f"{BASE_URL}/auth/register",
        json={"username": username, "password": password}
    )
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Registration successful!")
        print(f"   Username: {data['username']}")
        print(f"   User ID: {data['id']}")
        print(f"   2FA Secret: {data['secret']}")
        print(f"\n   Save this secret in your authenticator app!")
        secret = data['secret']
    else:
        print(f"❌ Registration failed: {response.json()}")
        exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)

print("\n=== Testing Login (you'll need to provide 2FA token) ===")
print(f"Use your authenticator app with secret: {secret}")
token_2fa = input("Enter 2FA token from your app: ")

try:
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"username": username, "password": password, "token": token_2fa}
    )
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Login successful!")
        print(f"   Access Token: {data['access_token'][:50]}...")
        print(f"   Token Type: {data['token_type']}")
        print(f"   Username: {data['username']}")
    else:
        print(f"❌ Login failed: {response.json()}")
except Exception as e:
    print(f"❌ Error: {e}")
