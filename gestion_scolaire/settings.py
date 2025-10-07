"""
Django settings for gestion_scolaire project.
"""

from pathlib import Path
import os
import mongoengine

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-gmti56ech(i%4)@=uc@!#u6zb55@hr6j%5vdn@h=)v^q%*2)47')

DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'drf_spectacular',
    'core',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'gestion_scolaire.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'gestion_scolaire.wsgi.application'

# ============ CONFIGURATION MONGODB ============

# Configuration MongoDB avec votre chaîne de connexion
MONGODB_URI = "mongodb+srv://jelly:bJByktwM0hRaT0xU@cluster0.94mrjki.mongodb.net/gestion_scolaire_db?retryWrites=true&w=majority&appName=Cluster0"

# Connexion MongoDB
# try:
#     mongoengine.connect(
#         host=MONGODB_URI,
#         alias='default',
#         db='gestion_scolaire_db'
#     )
#     print("Connexion MongoDB Atlas etablie avec succes!")
# except Exception as e:
#     print(f"Erreur de connexion MongoDB: {e}")

# Configuration Django database (requise pour les fonctionnalités Django)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Africa/Douala'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ============ CONFIGURATION DRF ============
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'core.authentication.MongoTokenAuthentication',  # Votre authentification personnalisée
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# ============ CONFIGURATION DRF-SPECTACULAR ============
SPECTACULAR_SETTINGS = {
    'TITLE': 'Gestion Scolaire API',
    'DESCRIPTION': 'API pour la gestion scolaire avec authentification token',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
    'SECURITY': [
        {
            'TokenAuth': []
        }
    ],
    'SECURITY_DEFINITIONS': {
        'TokenAuth': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': 'Token-based authentication with required prefix "Token"'
        }
    },
}

# Configuration CORS
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8080",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8080",
]

CORS_ALLOW_ALL_ORIGINS = os.environ.get('CORS_ALLOW_ALL_ORIGINS', 'True') == 'True'

# Configuration pour servir les fichiers média
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'