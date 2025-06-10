"""
Django settings for ryanair_flight_search project - DATABASE-FREE VERSION
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-your-secret-key-here')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DJANGO_DEBUG', 'False')

ALLOWED_HOSTS_ENV = os.environ.get('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1,0.0.0.0')
ALLOWED_HOSTS = [host.strip() for host in ALLOWED_HOSTS_ENV.split(',') if host.strip()]

# Application definition - MINIMAL APPS (no auth, no admin, no sessions)
INSTALLED_APPS = [
    'django.contrib.staticfiles',   # For CSS/JS files
    'flights',                      # Your flight search app
]

# MINIMAL MIDDLEWARE (no sessions, no auth, no CSRF)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    # Note: Static files are served automatically in DEBUG mode
]

ROOT_URLCONF = 'ryanair_flight_search.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                # Removed: auth and messages context processors
            ],
        },
    },
]

WSGI_APPLICATION = 'ryanair_flight_search.wsgi.application'

# 🚫 NO DATABASE CONFIGURATION AT ALL!

# Internationalization
LANGUAGE_CODE = os.environ.get('DJANGO_LANGUAGE_CODE', 'en-us')
TIME_ZONE = os.environ.get('DJANGO_TIME_ZONE', 'UTC')
USE_I18N = False  # Disable to avoid any DB-related queries
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom settings for the flight search app
RYANAIR_API_SETTINGS = {
    'DEFAULT_CURRENCY': 'EUR',
    'MAX_RESULTS_PER_PAGE': 20,
    'CACHE_TIMEOUT': 300,  # 5 minutes
}

