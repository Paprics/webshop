# base.py
import os
from datetime import timedelta
from pathlib import Path

from celery.schedules import crontab
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv()


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "drf_yasg",  # swagger docs
    "django_celery_beat",
    # app
    "accounts.apps.AccountsConfig",
    "api.apps.ApiConfig",
    "blog.apps.BlogConfig",
    "common.apps.CommonConfig",
    "store.apps.StoreConfig",
    "cart.apps.CartConfig",
    "favorites.apps.FavoritesConfig",
    "payments.apps.PaymentsConfig",
    "askrate.apps.AskrateConfig",
    # extantions
    "mptt",
    "rest_framework",
    "djoser",
    "rest_framework_simplejwt",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
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
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # context for menu
                "common.context_processors.category_processor_nested",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",  # noqa: F405
    }
}

LANGUAGE_CODE = "uk"

TIME_ZONE = "Europe/Kyiv"

USE_I18N = True

USE_L10N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "accounts.CustomerUser"

# DRF standard permission: Django model permissions
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    "DEFAULT_AUTHENTICATION_CLASSES": ("rest_framework_simplejwt.authentication.JWTAuthentication",),
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.AllowAny"],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
}


SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("Bearer",),
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=120),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=14),
}

DJOSER = {"LOGIN_FIELD": "phone_number", "USER_CREATE_PASSWORD_RETYPE": True}

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")

CELERY_BROKER_URL = "redis://redis"
CELERY_RESULT_BACKEND = "redis://redis"
CELERY_ACCEPT_CONTENT = ["application/json"]
SELERY_RESULT_SERIALIZER = "json"
CELERY_TASK_SERIALIZER = "json"

CELERY_BEAT_SCHEDULE = {
    "delete_notactive_user": {
        "task": "common.tasks.delete_notactive_user",
        "schedule": crontab(hour=12, minute=0, day_of_week="tue"),
    }
}

# Email
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.ukr.net"
EMAIL_PORT = 465
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = "privet.poka@ukr.net"
