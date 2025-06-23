import os

from config.settings.base import *  # noqa: F403

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS += [  # noqa: F405
    "django_extensions",
    "debug_toolbar",
]

MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]  # noqa: F405

if os.environ.get("GITHUB_WORKFLOW"):
    DATABASES = {
        "default": {  # GitHub Action
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "postgres",
            "USER": "postgres",
            "PASSWORD": "postgres",
            "HOST": "0.0.0.0",
            "PORT": 5432,
        }
    }
else:
    DATABASES = {
        "default_sqlite": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",  # noqa: F405
        },
        "#default": {  # Local
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "webshop",
            "USER": "postgres",
            "PASSWORD": "1111",
            "HOST": "localhost",
            "PORT": "5432",
        },
        "default": {  # Docker
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get("POSTGRES_DB"),
            "USER": os.environ.get("POSTGRES_USER"),
            "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
            "HOST": os.environ.get("POSTGRES_HOST"),
            "PORT": os.environ.get("POSTGRES_PORT"),
        },
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
