from config.settings.base import *  # noqa: F403

SECRET_KEY = "0b3t%0&p!*x_dx*6p-@ey(3ihp5kz9s)*@ilwo+z4cc4d($hj7"

DEBUG = False

ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",  # noqa: F405
    }
}

STATIC_ROOT = BASE_DIR / "static"  # noqa: F405
STATIC_URL = "/static/"  # noqa: F405

MEDIA_ROOT = BASE_DIR / "media"  # noqa: F405
MEDIA_URL = "/media/"  # noqa: F405
