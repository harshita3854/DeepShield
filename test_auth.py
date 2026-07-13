import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'deepshield_project.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User

client = Client()

# Test Registration
print("Testing Registration...")
response = client.post('/register/', {
    'username': 'testuser123',
    'email': 'test@example.com',
    'password': 'Password123!',
    'password_confirm': 'Password123!'
}, HTTP_HOST='localhost')

print(f"Registration Status Code: {response.status_code}")
if response.status_code == 200:
    print("Registration Failed. Form errors:")
    print(response.context['form'].errors)
elif response.status_code == 302:
    print(f"Registration Redirect URL: {response.url}")

# Test Login
print("\nTesting Login...")
response = client.post('/login/', {
    'username': 'testuser123',
    'password': 'Password123!'
}, HTTP_HOST='localhost')

print(f"Login Status Code: {response.status_code}")
if response.status_code == 200:
    print("Login Failed. Form errors:")
    print(response.context['form'].errors)
elif response.status_code == 302:
    print(f"Login Redirect URL: {response.url}")
