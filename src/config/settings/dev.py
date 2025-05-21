from config.settings.base import *  # noqa: F403

SECRET_KEY = "django-insecure-3^_+0p9^!1zww(7xvlvd-gotqujvlmx_36%9_2k==fxl-+z(a6"

DEBUG = True

ALLOWED_HOSTS = []

# MIDDLEWARE += [""]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",  # noqa: F405
    }
}

STATIC_URL = "static/"
