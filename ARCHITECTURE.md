# 🏗️ Project Architecture & Structure

## Overall Architecture

```
┌─────────────────────────────────────────────────────┐
│                   Browser / Client                  │
└──────────────────────┬────────────────────────────────┘
                       │ HTTP Requests
                       ▼
┌─────────────────────────────────────────────────────┐
│              Django Web Server                      │
│  (manage.py runserver / Gunicorn / uWSGI)           │
└──────────────────────┬────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
    ┌─────────┐   ┌─────────┐   ┌──────────┐
    │ Views   │   │ Models  │   │ Templates│
    │ (Logic) │   │ (Data)  │   │ (HTML)   │
    └────┬────┘   └────┬────┘   └──────────┘
         │             │
         └─────────┬───┘
                   │
         ┌─────────▼──────────┐
         │  SQLite Database   │
         │  (db.sqlite3)      │
         └────────────────────┘
```

---

## Project Directory Structure

```
waste_management/ (Project Root)
│
├── 📁 waste/                              # Main Django App
│   ├── 📁 migrations/
│   │   ├── __init__.py
│   │   └── 0001_initial.py               # Initial database migration
│   │
│   ├── 📁 management/
│   │   └── 📁 commands/
│   │       ├── __init__.py
│   │       └── populate_categories.py    # Custom command to seed data
│   │
│   ├── 📁 templates/
│   │   └── 📁 waste/
│   │       ├── base.html                 # Base template
│   │       ├── login.html                # Login page
│   │       ├── signup.html               # Signup page
│   │       ├── dashboard.html            # Main dashboard
│   │       └── category_detail.html      # Category details
│   │
│   ├── admin.py                          # Admin interface configuration
│   ├── apps.py                           # App configuration
│   ├── forms.py                          # Django forms (login, signup, reports)
│   ├── models.py                         # Database models
│   ├── tests.py                          # Test cases
│   ├── urls.py                           # URL routing for app
│   └── views.py                          # View functions (logic)
│
├── 📁 waste_management/                  # Project Configuration
│   ├── __init__.py
│   ├── asgi.py                           # ASGI configuration
│   ├── settings.py                       # Main settings file
│   ├── urls.py                           # Project URL routing
│   └── wsgi.py                           # WSGI configuration
│
├── 📁 static/                            # Static files (CSS, JS)
│   ├── 📁 css/
│   │   └── style.css                     # Project styles
│   └── 📁 js/
│       └── script.js                     # Project scripts
│
├── 📁 media/                             # User uploaded files
│
├── db.sqlite3                            # SQLite database file
├── manage.py                             # Django management script
├── requirements.txt                      # Python dependencies
├── .gitignore                            # Git ignore file
├── README.md                             # Project documentation
├── QUICKSTART.md                         # Quick start guide
├── USER_GUIDE.md                         # User guide
├── SETTINGS.md                           # Settings documentation
├── ARCHITECTURE.md                       # This file
├── run_server.bat                        # Batch file to run server
└── create_superuser.bat                  # Batch file to create admin
```

---

## Data Model Architecture

```
┌─────────────────────────┐
│    Django User          │
│  (from auth.models)     │
│  - username             │
│  - email                │
│  - password             │
│  - first_name           │
│  - last_name            │
└────────────┬────────────┘
             │ OneToOne
             │
┌────────────▼────────────────┐
│    UserProfile              │
│  - user (OneToOne)          │
│  - location                 │
│  - total_waste_recorded     │
└─────────────────────────────┘

┌─────────────────────────────┐
│   WasteCategory             │
│  - name (choices)           │
│  - icon                     │
│  - description              │
│  - color                    │
│  - treatment_method         │
│  - environmental_impact     │
└────────────┬────────────────┘
             │ ForeignKey
             │
┌────────────▼────────────────────┐
│    WasteReport                   │
│  - user (ForeignKey)             │
│  - category (ForeignKey)         │
│  - quantity                      │
│  - date                          │
│  - location                      │
│  - notes                         │
└──────────────────────────────────┘
```

---

## URL Routing Structure

```
http://localhost:8000/
│
├─ /                          → login_view (GET)
├─ /signup/                   → signup_view (GET, POST)
├─ /logout/                   → logout_view (POST)
├─ /dashboard/                → index_view (GET)
│
├─ /biodegradable/            → category_detail (GET)
├─ /plastic/                  → category_detail (GET)
├─ /ewaste/                   → category_detail (GET)
├─ /metal/                    → category_detail (GET)
├─ /glass/                    → category_detail (GET)
├─ /hazardous/                → category_detail (GET)
│
├─ /add-report/               → add_waste_report (POST)
├─ /reports/                  → user_reports (GET)
├─ /statistics/               → get_statistics (GET) → JSON
│
└─ /admin/                    → Django Admin Panel
   ├─ /waste/wastecategory/
   ├─ /waste/wastereport/
   └─ /waste/userprofile/
```

---

## Request Response Flow

### User Login Flow

```
┌──────────────┐
│ User enters  │
│ credentials  │
└──────┬───────┘
       │
       ▼
┌──────────────────────────────────┐
│ POST / login.html                │
│ (LoginForm with email & password)│
└──────┬───────────────────────────┘
       │
       ▼
┌──────────────────────────────────┐
│ login_view (views.py)            │
│ - Authenticate user              │
│ - Get from database              │
└──────┬───────────────────────────┘
       │
    ┌──┴──┐
    │     │
    ▼     ▼
 Success Failure
    │     │
    ▼     ▼
 Redirect Show Error
 Dashboard
```

### Waste Recording Flow

```
┌─────────────────────┐
│ Fill form on        │
│ dashboard           │
└──────┬──────────────┘
       │
       ▼
┌────────────────────────────────┐
│ POST /add-report/              │
│ WasteReportForm with:          │
│ - category                     │
│ - quantity                     │
│ - location                     │
│ - notes                        │
└──────┬─────────────────────────┘
       │
       ▼
┌────────────────────────────────┐
│ add_waste_report (views.py)    │
│ - Validate form                │
│ - Create WasteReport object    │
│ - Save to database             │
└──────┬─────────────────────────┘
       │
       ▼
┌────────────────────────────────┐
│ Database (SQLite)              │
│ INSERT WasteReport             │
└──────┬─────────────────────────┘
       │
       ▼
┌────────────────────────────────┐
│ Show success message           │
│ Redirect to dashboard          │
└────────────────────────────────┘
```

---

## Technology Stack

### Backend
- **Framework**: Django 6.0.2
- **Language**: Python 3.8+
- **Database**: SQLite3 (development), PostgreSQL (production)
- **ORM**: Django ORM

### Frontend
- **HTML5**: Template markup
- **CSS3**: Styling and layout
- **JavaScript**: Client-side interactions
- **Font Awesome**: Icon library

### Utilities
- **Authentication**: Django Auth System
- **Forms**: Django Forms
- **Admin**: Django Admin Interface
- **Server**: Django Development Server (runserver)

### Development Tools
- **Version Control**: Git
- **Package Manager**: pip
- **Database**: SQLite3
- **Editor**: VS Code

---

## Database Schema

### Tables (Models)

#### waste_wastecategory
```sql
CREATE TABLE waste_wastecategory (
    id INTEGER PRIMARY KEY,
    name VARCHAR(50) UNIQUE,
    icon VARCHAR(50),
    description TEXT,
    color VARCHAR(7),
    treatment_method TEXT,
    environmental_impact TEXT
);
```

#### waste_wastereport
```sql
CREATE TABLE waste_wastereport (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES auth_user(id),
    category_id INTEGER REFERENCES waste_wastecategory(id),
    quantity FLOAT,
    date DATE,
    location VARCHAR(255),
    notes TEXT
);
```

#### waste_userprofile
```sql
CREATE TABLE waste_userprofile (
    id INTEGER PRIMARY KEY,
    user_id INTEGER UNIQUE REFERENCES auth_user(id),
    location VARCHAR(255),
    total_waste_recorded FLOAT
);
```

---

## Authentication & Authorization

### Login System
- Email-based authentication
- Password hashing with Django's authentication system
- Session management

### User Roles
1. **Anonymous User**: Can only access login/signup
2. **Authenticated User**: Can access dashboard and features
3. **Superuser/Admin**: Full access including admin panel

### Permissions
- `login_required` decorator for protected views
- Redirect to login for unauthenticated access

---

## Performance Considerations

### Database Optimization
- Indexes on frequently queried fields
- Select_related for foreign keys
- Aggregate functions for statistics

### Caching (Future)
- Page caching for dashboard
- Query result caching
- Session-based caching

### Frontend Optimization
- Minimal CSS/JS
- Inline styles for quick loading
- Lazy loading for images (future)

---

## Deployment Architecture

### Development
```
Developer Machine
└── Django Dev Server (runserver)
    └── SQLite Database
```

### Production
```
Nginx/Apache (Web Server)
└── Gunicorn/uWSGI (App Server)
    └── Django Application
        └── PostgreSQL Database
```

---

## Security Architecture

### Input Validation
- Form validation in forms.py
- Model validation in models.py
- CSRF protection on forms

### Authentication
- Django's password hashing
- Session-based authentication
- Email-based login

### Data Protection
- SQL injection prevention (ORM)
- XSS protection (template auto-escaping)
- CSRF tokens on forms

---

## Error Handling

### View Level
- Try-catch for database errors
- Get_object_or_404 for missing records
- Form validation errors

### Template Level
- Error message display
- Form error highlighting
- User-friendly messages

### Logging
- Django logging system
- Error log files
- Debug information

---

## Testing Architecture

### Unit Tests
- Model tests
- Form tests
- View tests

### Integration Tests
- User registration
- Login/logout flow
- Waste recording

### Fixtures
- Sample data for testing
- Predefined categories
- Test users

---

## Scalability Considerations

### Current Limitations
- SQLite suitable for single-user
- No distributed caching
- Single server deployment

### Future Improvements
- PostgreSQL for multi-user
- Redis for caching
- Load balancing
- Database replication
- CDN for static files

---

## File Upload Architecture

### Media Files
```
media/
├── user_uploads/
│   ├── user_1/
│   ├── user_2/
│   └── ...
```

### Path: `/media/` → Served by Django in development

---

## API Architecture (Future)

```
REST Endpoints (DRF):

GET    /api/v1/waste-categories/
POST   /api/v1/waste-reports/
GET    /api/v1/waste-reports/
GET    /api/v1/statistics/
GET    /api/v1/user/profile/
PATCH  /api/v1/user/profile/
```

---

## CI/CD Architecture (Future)

```
GitHub
  │
  ├─ Push Code
  │
  ▼
GitHub Actions
  │
  ├─ Run Tests
  ├─ Check Code Quality
  ├─ Build Docker Image
  │
  ▼
Docker Registry
  │
  ▼
Production Server
  │
  ├─ Pull Image
  ├─ Run Container
  └─ Deploy
```

---

## Monitoring Architecture (Future)

```
Application
  │
  ├─ Error Logs → ELK Stack
  ├─ Performance Metrics → Prometheus
  ├─ Uptime Monitoring → Pingdom
  └─ User Analytics → Google Analytics
```

---

**This architecture provides a solid foundation for the Eco Waste Management System with room for growth and scalability!** 🚀
