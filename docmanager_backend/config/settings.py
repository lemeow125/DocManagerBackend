"""
Django settings for docmanager_backend project.

Generated by "django-admin startproject" using Django 5.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os
from datetime import timedelta
from dotenv import find_dotenv, load_dotenv  # Python dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# Backend folder (/docmanager_backend)
BASE_DIR = Path(__file__).resolve().parent.parent
# Root folder where .env is located
ROOT_DIR = Path(__file__).resolve().parent.parent.parent

load_dotenv(find_dotenv())


def get_secret(secret_name):
    # Read from .env
    secret_value = os.getenv(secret_name)

    if secret_value is None:
        raise ValueError(f"Secret '{secret_name}' not found.")
    else:
        # Parse Boolean values
        if secret_value == "True":
            secret_value = True
        elif secret_value == "False":
            secret_value = False
        return secret_value


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_secret("SECRET_KEY")

# SECURITY WARNING: don"t run with debug turned on in production!
DEBUG = get_secret("DEBUG")

# URL Prefixes
USE_HTTPS = get_secret("USE_HTTPS")
URL_SCHEME = "https" if USE_HTTPS else "http"
# Building Backend URL
BACKEND_ADDRESS = get_secret("BACKEND_ADDRESS")
BACKEND_PORT = get_secret("BACKEND_PORT")
# Building Frontend URL
FRONTEND_ADDRESS = get_secret("FRONTEND_ADDRESS")
FRONTEND_PORT = get_secret("FRONTEND_PORT")
# Full URLs
BACKEND_URL = f"{URL_SCHEME}://{BACKEND_ADDRESS}"
FRONTEND_URL = f"{URL_SCHEME}://{BACKEND_ADDRESS}"

# Append port to full URLs if deployed locally
if not USE_HTTPS:
    BACKEND_URL += f":{BACKEND_PORT}"
    FRONTEND_URL += f":{FRONTEND_PORT}"

ALLOWED_HOSTS = ["*"]
CSRF_TRUSTED_ORIGINS = [
    FRONTEND_URL,
    BACKEND_URL,
    # You can also set up https://*.name.xyz for wildcards here
]


# Application definition

INSTALLED_APPS = [
    "unfold",
    "unfold.contrib.filters",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions",
    "rest_framework",
    "rest_framework_simplejwt",
    "djoser",
    "corsheaders",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "emails",
    "accounts",
    "documents",
    "document_requests",
    "questionnaires",
    "django_cleanup.apps.CleanupConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "emails/templates/",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 8,
        },
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
    # Additional password validators
    {
        "NAME": "accounts.validators.SpecialCharacterValidator",
    },
    {
        "NAME": "accounts.validators.LowercaseValidator",
    },
    {
        "NAME": "accounts.validators.UppercaseValidator",
    },
    {
        "NAME": "accounts.validators.NumberValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = get_secret("TIMEZONE")

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
MEDIA_URL = f"{BACKEND_URL}/api/v1/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
ROOT_URLCONF = "config.urls"
STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {"anon": "360/min", "user": "1440/min"},
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": get_secret("PROJECT_NAME"),
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
}

DJOSER = {
    "SEND_ACTIVATION_EMAIL": True,
    "SEND_CONFIRMATION_EMAIL": True,
    "PASSWORD_RESET_CONFIRM_URL": "reset_password_confirm/{uid}/{token}",
    "ACTIVATION_URL": "activation/{uid}/{token}",
    "USER_AUTHENTICATION_RULES": ["djoser.authentication.TokenAuthenticationRule"],
    "SERIALIZERS": {
        "user": "accounts.serializers.CustomUserSerializer",
        "current_user": "accounts.serializers.CustomUserSerializer",
        "user_create": "accounts.serializers.CustomUserRegistrationSerializer",
    },
    "PERMISSIONS": {
        # Disable some unneeded endpoints by setting them to admin only
        "username_reset": ["rest_framework.permissions.IsAdminUser"],
        "username_reset_confirm": ["rest_framework.permissions.IsAdminUser"],
        "set_username": ["rest_framework.permissions.IsAdminUser"],
        "set_password": ["rest_framework.permissions.IsAdminUser"],
    },
}

# SMTP (Email)
EMAIL_HOST = get_secret("EMAIL_HOST")
EMAIL_HOST_USER = get_secret("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = get_secret("EMAIL_HOST_PASSWORD")
EMAIL_PORT = get_secret("EMAIL_PORT")
EMAIL_USE_TLS = get_secret("EMAIL_USE_TLS")
EMAIL_ADDRESS = get_secret("EMAIL_ADDRESS")
DEFAULT_FROM_EMAIL = EMAIL_ADDRESS

AUTH_USER_MODEL = "accounts.CustomUser"

DATA_UPLOAD_MAX_NUMBER_FIELDS = 20480

GRAPH_MODELS = {"app_labels": [
    "accounts", "documents", "document_requests", "questionnaires"]}

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True