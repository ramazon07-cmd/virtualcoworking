import requests

# Base URLs
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api"

# Create a session to maintain cookies
session = requests.Session()

# Get CSRF token
print("Getting CSRF token...")
csrf_response = session.get(f"{BASE_URL}/csrf/")
if csrf_response.status_code == 200:
    csrf_token = csrf_response.cookies.get('csrftoken')
    session.headers.update({'X-CSRFToken': csrf_token})
    print(f"CSRF token: {csrf_token}")
else:
    print("Failed to get CSRF token, continuing without it...")

print("\n" + "="*50 + "\n")

# Test registration with a new user
print("Testing user registration...")
reg_data = {
    "username": "testuser3",
    "email": "test3@example.com",
    "password": "testpass123",
    "password_confirm": "testpass123",
    "first_name": "Test3",
    "last_name": "User3"
}

reg_response = session.post(f"{API_BASE}/auth/register/", json=reg_data)
print(f"Registration status: {reg_response.status_code}")
if reg_response.status_code == 201:
    print("Registration successful!")
    user_data = reg_response.json()
    print(f"User created: {user_data}")
else:
    print(f"Registration failed: {reg_response.text}")

print("\n" + "="*50 + "\n")

# Test login
print("Testing user login...")
login_data = {
    "username": "testuser3",
    "password": "testpass123"
}

login_response = session.post(f"{API_BASE}/auth/login/", json=login_data)
print(f"Login status: {login_response.status_code}")
if login_response.status_code == 200:
    print("Login successful!")
    user_data = login_response.json()
    print(f"Logged in user: {user_data}")
    
    # Update CSRF token after login
    if 'csrftoken' in login_response.cookies:
        csrf_token = login_response.cookies.get('csrftoken')
        session.headers.update({'X-CSRFToken': csrf_token})
        print(f"Updated CSRF token: {csrf_token}")
else:
    print(f"Login failed: {login_response.text}")

print("\n" + "="*50 + "\n")

# Test getting current user (should work if logged in)
print("Testing current user endpoint...")
current_user_response = session.get(f"{API_BASE}/auth/current-user/")
print(f"Current user status: {current_user_response.status_code}")
if current_user_response.status_code == 200:
    user_data = current_user_response.json()
    print(f"Current user: {user_data}")
else:
    print(f"Failed to get current user: {current_user_response.text}")

print("\n" + "="*50 + "\n")

# Test getting user profile
print("Testing user profile endpoint...")
profile_response = session.get(f"{API_BASE}/auth/profile/")
print(f"Profile status: {profile_response.status_code}")
if profile_response.status_code == 200:
    profile_data = profile_response.json()
    print(f"User profile: {profile_data}")
else:
    print(f"Failed to get profile: {profile_response.text}")

print("\n" + "="*50 + "\n")

# Test updating user profile
print("Testing profile update...")
update_data = {
    "first_name": "UpdatedTest3",
    "last_name": "UpdatedUser3",
    "bio": "This is a test bio",
    "location": "Test City",
    "role": "freelancer",
    "company_name": "Test Company"
}

update_response = session.put(f"{API_BASE}/auth/profile/update/", json=update_data)
print(f"Profile update status: {update_response.status_code}")
if update_response.status_code == 200:
    updated_profile = update_response.json()
    print(f"Updated profile: {updated_profile}")
else:
    print(f"Failed to update profile: {update_response.text}")

print("\n" + "="*50 + "\n")

# Test logout
print("Testing logout...")
logout_response = session.post(f"{API_BASE}/auth/logout/")
print(f"Logout status: {logout_response.status_code}")
if logout_response.status_code == 200:
    print("Logout successful!")
    logout_data = logout_response.json()
    print(f"Logout response: {logout_data}")
else:
    print(f"Logout failed: {logout_response.text}")