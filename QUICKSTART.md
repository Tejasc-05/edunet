# 🌱 Quick Start Guide - Eco Waste Management Django

## Fast Setup (5 minutes)

### Option 1: Using Batch Files (Easiest for Windows)

#### Step 1: Create Superuser
Double-click: `create_superuser.bat`
- Username: `admin`
- Email: `admin@example.com`
- Password: `admin123` (or your choice)

#### Step 2: Run the Server
Double-click: `run_server.bat`
- Server will start at `http://127.0.0.1:8000/`

#### Step 3: Access the App
- **Home**: `http://127.0.0.1:8000/`
- **Admin**: `http://127.0.0.1:8000/admin/`

---

### Option 2: Using Command Line

```bash
# 1. Navigate to project directory
cd c:\Users\Lenovo\Downloads\smart

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run migrations
python manage.py migrate

# 4. Populate categories
python manage.py populate_categories

# 5. Create superuser
python manage.py createsuperuser

# 6. Start server
python manage.py runserver
```

---

## User Flows

### New User Registration
1. Go to `http://127.0.0.1:8000/`
2. Click "Sign up here!"
3. Enter:
   - Full Name
   - Email
   - Password (min 6 characters)
   - Confirm Password
4. Click "CREATE ACCOUNT"
5. You're logged in! 🎉

### Login
1. Enter your email
2. Enter your password
3. Click "LOGIN"

### Record Waste
1. Go to Dashboard
2. Scroll to "Record New Waste"
3. Select Category (Biodegradable, Plastic, etc.)
4. Enter Quantity (in kg)
5. Add Location (optional)
6. Add Notes (optional)
7. Click "Record Waste"

### View Category Details
1. Click on any waste category card
2. See:
   - Treatment method
   - Environmental impact
   - Your reports for this category
   - Statistics

---

## Key Pages

| URL | Purpose | Access |
|-----|---------|--------|
| `/` | Login | Not logged in |
| `/signup/` | Create account | Not logged in |
| `/dashboard/` | Main dashboard | Logged in |
| `/biodegradable/` | Biodegradable waste | Logged in |
| `/plastic/` | Plastic waste | Logged in |
| `/ewaste/` | E-waste | Logged in |
| `/metal/` | Metal waste | Logged in |
| `/glass/` | Glass waste | Logged in |
| `/hazardous/` | Hazardous waste | Logged in |
| `/reports/` | Your reports | Logged in |
| `/admin/` | Admin panel | Superuser |
| `/logout/` | Logout | Logged in |

---

## Test Accounts

### Admin Account (Create your own via `create_superuser.bat`)
- Access: `http://127.0.0.1:8000/admin/`
- Can manage all data

### Regular User Account
- Create via signup form
- Can record and view waste data

---

## Admin Panel Guide

Access: `http://127.0.0.1:8000/admin/`

### Manage Waste Categories
- View all categories
- Edit category details
- Change colors and icons

### View User Reports
- See all waste reports
- Filter by category or date
- Delete reports if needed

### Manage Users
- View all registered users
- Reset passwords
- Delete users

---

## Troubleshooting

### "Port 8000 already in use"
```bash
python manage.py runserver 8001
```

### "No module named django"
```bash
pip install django==6.0.2
```

### Database errors
```bash
python manage.py migrate --run-syncdb
```

### Forgot admin password
```bash
python manage.py changepassword admin
```

### Clear all data and start fresh
```bash
# Delete db.sqlite3
# Run migrations again
python manage.py migrate
python manage.py populate_categories
python manage.py createsuperuser
```

---

## Development Tips

### Create Test Data
```bash
# Create user
python manage.py shell
>>> from django.contrib.auth.models import User
>>> user = User.objects.create_user('testuser', 'test@example.com', 'password')

# Create waste report
>>> from waste.models import WasteCategory, WasteReport
>>> cat = WasteCategory.objects.get(name='biodegradable')
>>> WasteReport.objects.create(user=user, category=cat, quantity=10.5)
```

### Access Django Shell
```bash
python manage.py shell
```

### Export Data
```bash
python manage.py dumpdata > data.json
```

### Import Data
```bash
python manage.py loaddata data.json
```

---

## Features Overview

✅ **User Management**
- Registration with email validation
- Secure login system
- Profile management

✅ **Waste Tracking**
- 6 waste categories
- Quantity tracking (in kg)
- Location based records
- Custom notes

✅ **Statistics**
- Total waste recorded
- Category-wise breakdown
- Report count
- Historical data

✅ **Admin Dashboard**
- Full user management
- Category configuration
- Report management
- Statistics overview

---

## Next Steps

1. **Customize Colors**: Edit `color` field in waste categories admin
2. **Add Categories**: Use Django admin or edit `populate_categories.py`
3. **Advanced Analytics**: Integrate Chart.js or D3.js
4. **Mobile App**: Build a React Native app
5. **API**: Create REST API with Django REST Framework
6. **Deployment**: Deploy to Heroku, AWS, or Azure

---

## Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django Models](https://docs.djangoproject.com/en/6.0/topics/db/models/)
- [Django Views](https://docs.djangoproject.com/en/6.0/topics/http/views/)
- [Django Templates](https://docs.djangoproject.com/en/6.0/topics/templates/)
- [Django Forms](https://docs.djangoproject.com/en/6.0/topics/forms/)

---

**Happy waste tracking! Together we can make India cleaner! 🌍♻️**
