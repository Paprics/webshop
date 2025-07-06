# prod.py
import os

from config.settings.base import *  # noqa: F403

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")

DEBUG = False

ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",  # noqa: F405
    }
}

STATIC_ROOT = BASE_DIR / "static/"  # noqa: F405
STATIC_URL = "static/"  # noqa: F405

MEDIA_ROOT = BASE_DIR / "media/"  # noqa: F405
MEDIA_URL = "media/"  # noqa: F405
