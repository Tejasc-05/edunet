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

## AI Classifier — Training & Usage

This project includes an image-based waste classifier located at `waste/waste_classifier.py` and a transfer-learning training helper at `waste/train_classifier.py`.

- Dataset layout expected by the training script:
	- `data/train/biodegradable/*`
	- `data/train/plastic/*`
	- `data/train/ewaste/*`
	- `data/train/metal/*`
	- `data/train/glass/*`
	- `data/train/hazardous/*`

- Quick dry-run (builds model and saves initial weights):
```bash
./.venv/bin/python -m waste.train_classifier --dry-run
# or: python3 -m waste.train_classifier --dry-run
```

- Train (example short run):
```bash
./.venv/bin/python -m waste.train_classifier --data data/train --epochs 10 --batch 16
```

- Avoid downloading ImageNet weights (useful in restricted/SSL-failing environments):
	- Train without ImageNet weights:
```bash
./.venv/bin/python -m waste.train_classifier --data data/train --epochs 10 --batch 16 --weights none
```
	- By default the classifier will initialize base models without downloading ImageNet weights. To explicitly allow runtime ImageNet weight downloads set the environment variable `WASTE_LOAD_IMAGENET=1` before running the app or scripts.

- Trained artifacts and integration:
	- Fine-tuned weights saved to `waste/model_weights/mobilenet_finetuned.weights.h5`
	- Class index mapping saved to `waste/model_weights/class_indices.json`
	- `waste/waste_classifier.py` will automatically load the fine-tuned weights (if present) and use them for classification.

- Notes:
	- For best accuracy train with ImageNet initialization (if available) and a sufficiently large, real dataset.
	- If you encounter SSL/certificate errors when downloading weights, use `--weights none` during training and set `WASTE_LOAD_IMAGENET=1` only on machines with working certificate chains.


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
