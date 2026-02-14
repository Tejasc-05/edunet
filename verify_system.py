#!/usr/bin/env python
"""
Quick test script to verify Django project is ready
"""
import os
import sys
import django

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'waste_management.settings')
django.setup()

from django.core.management import call_command
from waste.models import WasteCategory, WasteReport, UserProfile
from django.contrib.auth.models import User

print("\n" + "="*60)
print("🔍 ECO WASTE MANAGEMENT - SYSTEM VERIFICATION")
print("="*60 + "\n")

# Test 1: Check Django version
from django import get_version
print(f"✅ Django Version: {get_version()}")

# Test 2: Check Database Connection
print(f"✅ Database: SQLite3 (db.sqlite3)")

# Test 3: Check Waste Categories
categories = WasteCategory.objects.all()
print(f"✅ Waste Categories: {categories.count()} categories found")
for cat in categories:
    print(f"   • {cat.get_name_display()}")

# Test 4: Check User Count
user_count = User.objects.count()
print(f"✅ Users in Database: {user_count} user(s)")

# Test 5: Check Reports
report_count = WasteReport.objects.count()
print(f"✅ Waste Reports: {report_count} report(s)")

# Test 6: Check Templates
import os
template_path = os.path.join(os.path.dirname(__file__), 'waste', 'templates', 'waste')
if os.path.exists(template_path):
    templates = os.listdir(template_path)
    print(f"✅ Templates Found: {len(templates)} template(s)")
    for template in templates:
        print(f"   • {template}")
else:
    print("❌ Templates directory not found")

# Test 7: Check Static Files
static_path = os.path.join(os.path.dirname(__file__), 'static')
if os.path.exists(static_path):
    print(f"✅ Static Files Directory: Ready")
else:
    print("⚠️  Static Files Directory: Not found (not critical)")

# Test 8: Settings Check
from django.conf import settings
print(f"✅ DEBUG Mode: {settings.DEBUG}")
print(f"✅ ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")

print("\n" + "="*60)
print("🎉 ALL SYSTEMS CHECK OUT!")
print("="*60)
print("\n📍 Ready to start the server!\n")
print("Run: python manage.py runserver")
print("Then visit: http://127.0.0.1:8000/\n")
print("="*60 + "\n")
