from config.settings.base import *  # noqa: F403

SECRET_KEY = "django-insecure-3^_+0p9^!1zww(7xvlvd-gotqujvlmx_36%9_2k==fxl-+z(a6"

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS += [  # noqa: F405
    "django_extensions",
    "debug_toolbar",
]

MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]  # noqa: F405

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",  # noqa: F405
    }
}

GRAPH_MODELS = {
    "all_applications": True,
    "group_models": True,
}

# STATIC SETTINGS
STATIC_URL = "/static/"
STATICFILES_DIRS = [  # Include custom static directory (e.g. Source/static) for development
    BASE_DIR / "static"  # noqa: F405
]

INTERNAL_IPS = [
    "127.0.0.1",
]
