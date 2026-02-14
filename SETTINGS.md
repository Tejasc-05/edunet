# Django Configuration Guide

## Settings File: `waste_management/settings.py`

This file contains all configuration for the Django project.

### Key Settings

#### DEBUG
```python
DEBUG = True  # Set to False in production
```

#### ALLOWED_HOSTS
```python
ALLOWED_HOSTS = []  # Add your domain in production: ['yourdomain.com']
```

#### INSTALLED_APPS
All Django apps including our `waste` app are configured here.

#### DATABASES
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # SQLite for development
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

#### TEMPLATES
HTML templates are loaded from `waste/templates/` directory.

#### STATIC_URL
Static files (CSS, JS) are served from `/static/` URL.

---

## Environment-Specific Configuration

### Development
```python
DEBUG = True
ALLOWED_HOSTS = ['*']
```

### Production
```python
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
SECRET_KEY = 'use-secure-key-generator'
```

---

## Running with Different Configurations

### Custom Port
```bash
python manage.py runserver 0.0.0.0:8001
```

### Specific Host and Port
```bash
python manage.py runserver 192.168.1.100:8000
```

### With WSGI Server (Gunicorn)
```bash
pip install gunicorn
gunicorn waste_management.wsgi:application
```

---

## Database Management

### Create Superuser
```bash
python manage.py createsuperuser
```

### Change Password
```bash
python manage.py changepassword <username>
```

### Reset Database
```bash
# Delete db.sqlite3
# Then run migrations
python manage.py migrate
```

### Backup Database
```bash
python manage.py dumpdata > backup.json
```

### Restore Database
```bash
python manage.py loaddata backup.json
```

---

## Performance Tuning

### Database Query Optimization
- Use `select_related()` for ForeignKey
- Use `prefetch_related()` for ManyToMany
- Add database indexes

### Caching
Add to settings.py for Redis caching:
```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

### Middleware Optimization
- Remove unnecessary middleware
- Order middleware by execution time

### Static Files
```bash
python manage.py collectstatic --noinput
```

---

## Security Settings for Production

```python
# security/settings.py

DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']

# HTTPS
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_SECURITY_POLICY = {
    'default-src': ("'self'",),
}

# HSTS
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

---

## Logging Configuration

Add to settings.py:
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'error.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
```

---

## Email Configuration

For sending emails, add:
```python
# Gmail
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

---

## Media Files Configuration

Already configured:
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

Access uploaded files at: `/media/filename`

---

## Customizing Settings

### Create a Local Settings File

Create `waste_management/local_settings.py`:
```python
# Override specific settings here
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
```

Import in main settings.py:
```python
try:
    from .local_settings import *
except ImportError:
    pass
```

---

## Common Configuration Errors

### Error: `No module named 'waste'`
- Add 'waste' to INSTALLED_APPS

### Error: `TemplateDoesNotExist`
- Check TEMPLATES configuration
- Ensure templates folder exists

### Error: `DatabaseError`
- Run `python manage.py migrate`
- Check database path

---

## Deployment Checklist

- [ ] Set DEBUG = False
- [ ] Update ALLOWED_HOSTS
- [ ] Generate new SECRET_KEY
- [ ] Configure database
- [ ] Set up static files
- [ ] Configure email
- [ ] Set up logging
- [ ] Enable HTTPS
- [ ] Set security headers
- [ ] Create superuser
- [ ] Run migrations
- [ ] Test with gunicorn

---

## Useful Django Management Commands

```bash
# Check project
python manage.py check

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Shell access
python manage.py shell

# Run tests
python manage.py test

# Dump data
python manage.py dumpdata > backup.json

# Load data
python manage.py loaddata backup.json

# Database operations
python manage.py dbshell

# Show migrations
python manage.py showmigrations

# SQL for migrations
python manage.py sqlmigrate waste 0001
```

---

**For more information, visit: https://docs.djangoproject.com/en/6.0/ref/settings/**
