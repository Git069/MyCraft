"""
Django settings for the MyCraft project.
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# --- SECURITY WARNINGS ---
# It's crucial to keep secret information out of version control.
# We use environment variables to manage sensitive data.

# SECRET_KEY: Fallback to an insecure key for local development only.
# In production, this MUST be set as an environment variable.
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY", "django-insecure-default-dev-key-change-me"
)

# DEBUG: Defaults to 'True' for development.
# In production, set DJANGO_DEBUG='False' as an environment variable.
DEBUG = os.environ.get("DJANGO_DEBUG", "True") == "True"

# ALLOWED_HOSTS: Defines which domains can access the application.
# 'backend' is the service name within the Docker network.
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "backend"]


# --- Application Definition ---

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "rest_framework",
    "rest_framework.authtoken",
    "users",
    "jobs",
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Corrected ROOT_URLCONF to point to the 'config' module
ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# Corrected WSGI_APPLICATION to point to the 'config' module
WSGI_APPLICATION = "config.wsgi.application"


# --- Database ---
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

'''
# --- Database Configuration ---
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'MyCraftDB', # Standard-DB-Name von Supabase
        'USER': 'postgres', # Standard-Benutzer von Supabase
        'PASSWORD': 'UKkFfRk5e7KjyLTy', # <-- IHR PASSWORT VON SUPABASE
        'HOST': 'sldqevyzgsxkbnqxmytt.supabase.co', # <-- IHR HOST VON SUPABASE
        'PORT': '5432', # Standard-Port
    }
}
'''

# --- Password Validation ---
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# --- Internationalization ---
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# --- Static Files ---
STATIC_URL = "static/"

# --- Default Primary Key ---
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- REST Framework Configuration ---
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

# --- CORS Configuration ---
# Updated to allow requests from the Vite development server.
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
CORS_ALLOW_CREDENTIALS = True
