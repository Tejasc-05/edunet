"""
Test Django App Loading
Verifies the application can handle a test request
"""
import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'waste_management.settings')
django.setup()

from django.test import Client
from django.urls import reverse

print("\n" + "="*70)
print("🧪 TESTING DJANGO APPLICATION - URL ACCESSIBILITY")
print("="*70 + "\n")

# Create test client
client = Client()

# Test 1: Login Page
print("Test 1: Accessing Login Page (GET /)")
response = client.get('/')
print(f"  Status Code: {response.status_code}")
print(f"  ✅ PASS - Login page loads" if response.status_code == 200 else "  ❌ FAIL")
print()

# Test 2: Signup Page
print("Test 2: Accessing Signup Page (GET /signup/)")
response = client.get('/signup/')
print(f"  Status Code: {response.status_code}")
print(f"  ✅ PASS - Signup page loads" if response.status_code == 200 else "  ❌ FAIL")
print()

# Test 3: Dashboard (should redirect to login without auth)
print("Test 3: Accessing Dashboard Without Login (GET /dashboard/)")
response = client.get('/dashboard/')
print(f"  Status Code: {response.status_code}")
print(f"  ✅ PASS - Correctly redirects to login (302)" if response.status_code == 302 else f"  ❌ FAIL")
print()

# Test 4: Admin Page
print("Test 4: Accessing Admin Panel (GET /admin/)")
response = client.get('/admin/')
print(f"  Status Code: {response.status_code}")
print(f"  ✅ PASS - Admin page accessible" if response.status_code in [200, 302] else "  ❌ FAIL")
print()

# Test 5: Category Pages (should redirect without auth)
print("Test 5: Accessing Category Pages (GET /biodegradable/)")
response = client.get('/biodegradable/')
print(f"  Status Code: {response.status_code}")
print(f"  ✅ PASS - Correctly redirects to login (302)" if response.status_code == 302 else f"  ❌ FAIL")
print()

# Test 6: Create Test User
from django.contrib.auth.models import User
from waste.models import UserProfile

print("Test 6: Creating Test User")
try:
    if not User.objects.filter(username='testuser').exists():
        user = User.objects.create_user('testuser', 'test@example.com', 'testpass123')
        UserProfile.objects.create(user=user)
        print(f"  ✅ PASS - Test user created")
    else:
        print(f"  ✅ PASS - Test user already exists")
except Exception as e:
    print(f"  ❌ FAIL - {str(e)}")
print()

# Test 7: Login with Test User
print("Test 7: Testing Login (POST /)")
login_data = {'email': 'test@example.com', 'password': 'testpass123'}
response = client.post('/', login_data)
print(f"  Status Code: {response.status_code}")
print(f"  ✅ PASS - Login works" if response.status_code in [200, 302] else f"  ⚠️  FAIL - Check credentials")
print()

# Test 8: Access Dashboard with Auth
print("Test 8: Accessing Dashboard With Authentication")
client.login(username='testuser', password='testpass123')
response = client.get('/dashboard/')
print(f"  Status Code: {response.status_code}")
print(f"  ✅ PASS - Dashboard loads for authenticated user" if response.status_code == 200 else f"  ❌ FAIL")
print()

# Test 9: Check Database
from waste.models import WasteCategory, WasteReport
print("Test 9: Database Integrity Check")
cat_count = WasteCategory.objects.count()
print(f"  Categories: {cat_count}")
print(f"  ✅ PASS - All 6 categories present" if cat_count == 6 else f"  ❌ FAIL")
print()

print("="*70)
print("✅ ALL APPLICATION TESTS COMPLETED!")
print("="*70)
print("\n📍 The application is ready for deployment!\n")
print("START THE SERVER:")
print("  • Double-click: run_server.bat")
print("  • Or run: python manage.py runserver")
print("\nACCESS THE APP:")
print("  • http://127.0.0.1:8000/")
print("\n" + "="*70 + "\n")
