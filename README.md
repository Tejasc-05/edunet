# Eco Waste Management - Django Application

A complete Django-based web application for tracking and managing waste generation in India. This application helps users record, categorize, and analyze waste data across multiple waste types.

## Features

✅ **User Authentication**
- User registration (Sign Up)
- Secure login system
- User profile management

✅ **Waste Categories**
- Biodegradable waste
- Plastic waste
- E-waste
- Metal waste
- Glass waste
- Hazardous waste

✅ **Waste Tracking**
- Record waste reports
- Track waste by category
- View detailed statistics
- Filter and search reports

✅ **Dashboard**
- User-friendly interface
- Real-time statistics
- Category overview cards
- Quick waste recording

## Project Structure

```
waste_management/
├── waste_management/          # Django project settings
│   ├── settings.py           # Project configuration
│   ├── urls.py               # URL routing
│   ├── wsgi.py              # WSGI configuration
│   └── asgi.py              # ASGI configuration
├── waste/                     # Main Django app
│   ├── models.py            # Database models
│   ├── views.py             # View logic
│   ├── urls.py              # App URL patterns
│   ├── forms.py             # Django forms
│   ├── admin.py             # Admin configuration
│   ├── templates/waste/     # HTML templates
│   ├── static/              # CSS, JS, images
│   ├── migrations/          # Database migrations
│   └── management/commands/ # Custom commands
├── static/                    # Project static files
│   ├── css/                 # Stylesheets
│   └── js/                  # JavaScript files
├── db.sqlite3               # SQLite database
├── manage.py                # Django management script
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Apply Migrations

```bash
python manage.py migrate
```

### Step 3: Populate Waste Categories

```bash
python manage.py populate_categories
```

### Step 4: Create Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

Follow the prompts to create your admin account:
- Username: (choose your username)
- Email: (enter your email)
- Password: (enter a secure password)

### Step 5: Run the Development Server

```bash
python manage.py runserver
```

The application will be available at: `http://127.0.0.1:8000/`

## OpenAI Integration (optional)

To enable improved classification via OpenAI vision/text models:

1. Create and activate a virtual environment and install requirements (includes `openai`):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

2. Set your OpenAI API key (macOS / Linux):

```bash
export OPENAI_API_KEY="sk-..."
```

3. Run the verification script (this will call OpenAI and may incur usage):

```bash
python scripts/verify_openai.py path/to/photo.jpg
```

Notes:
- OpenAI usage is optional; the classifier falls back to local heuristics and ML models if the API key or package is not available.
- Telemetry of OpenAI responses is appended to `reports/openai_telemetry.csv` for auditing and prompt improvement.

## Usage

### User Registration
1. Navigate to the signup page
2. Enter your full name, email, and password
3. Click "CREATE ACCOUNT"
4. You'll be automatically logged in and redirected to the dashboard

### Login
1. Enter your email and password
2. Click "LOGIN"
3. Access the dashboard and waste tracking features

### Recording Waste
1. On the dashboard, scroll to "Record New Waste"
2. Select a waste category
3. Enter quantity in kg
4. Add location and optional notes
5. Click "Record Waste"

### Viewing Categories
1. Click on any waste category from the dashboard
2. View detailed information about that waste type
3. See your reports for that category
4. Check treatment methods and environmental impact

### Viewing Statistics
- Dashboard shows total waste recorded
- View number of reports submitted
- See category-wise breakdown

## Admin Interface

Access the admin panel at: `http://127.0.0.1:8000/admin/`

Login with your superuser credentials to:
- Manage waste categories
- View and delete user reports
- Monitor user profiles
- Manage user accounts

## Database Models

### WasteCategory
- name (choices: biodegradable, plastic, ewaste, metal, glass, hazardous)
- icon (Font Awesome icon class)
- description
- color (hex color code)
- treatment_method
- environmental_impact

### WasteReport
- user (ForeignKey to User)
- category (ForeignKey to WasteCategory)
- quantity (float, in kg)
- date (auto-set on creation)
- location (default: Bangalore, India)
- notes (optional text)

### UserProfile
- user (OneToOneField to User)
- location
- total_waste_recorded

## URL Routes

| Route | Purpose |
|-------|---------|
| `/` | Login page |
| `/signup/` | User registration |
| `/logout/` | Logout user |
| `/dashboard/` | Main dashboard |
| `/biodegradable/` | Biodegradable waste details |
| `/plastic/` | Plastic waste details |
| `/ewaste/` | E-waste details |
| `/metal/` | Metal waste details |
| `/glass/` | Glass waste details |
| `/hazardous/` | Hazardous waste details |
| `/add-report/` | Add new waste report |
| `/reports/` | View all user reports |
| `/statistics/` | View statistics (JSON) |
| `/admin/` | Admin panel |

## Customization

### Adding New Waste Categories

Edit the `populate_categories.py` file in `waste/management/commands/` and add new categories.

### Styling

Modify the CSS embedded in the templates or create separate CSS files in the `static/css/` directory.

### Adding More Fields

Modify the models in `waste/models.py` and create new migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

## Environment Variables

Create a `.env` file for production (not included in the repository):

```
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
DATABASE_URL=your-database-url
```

## Security Notes

⚠️ **Important for Production:**
- Change `DEBUG = False` in `settings.py`
- Update `ALLOWED_HOSTS` with your domain
- Use a strong `SECRET_KEY`
- Use PostgreSQL instead of SQLite
- Configure CSRF and CORS settings
- Enable HTTPS
- Set up proper database backups

## Troubleshooting

### Database Errors
```bash
python manage.py makemigrations
python manage.py migrate
```

### Port Already in Use
```bash
python manage.py runserver 8001
```

### Module Not Found
```bash
pip install -r requirements.txt --upgrade
```

### Static Files Not Loading
```bash
python manage.py collectstatic
```

## Performance Optimization

1. **Database Indexing**: Add indexes to frequently queried fields
2. **Caching**: Implement Redis caching for frequently accessed data
3. **Pagination**: Add pagination to report listings
4. **Database**: Use PostgreSQL for production
5. **CDN**: Serve static files from a CDN

## Future Enhancements

- 📊 Advanced analytics and charts
- 🗺️ Interactive waste generation maps
- 📱 Mobile application
- 🔔 Notifications and reminders
- 📧 Email reports
- 🌍 Leaderboards for waste reduction
- 🎯 Sustainability goals tracking
- 📈 Historical data analysis

## License

This project is open source and available under the MIT License.

## Support

For issues and questions, please refer to Django documentation:
- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/) (for API extension)

## Contributors

Created as a full Django conversion of the Eco Waste Management project.

---

**Happy waste tracking! Together, let's build a sustainable India.** 🌱
