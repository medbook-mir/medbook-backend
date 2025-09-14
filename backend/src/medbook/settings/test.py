from .base import *
import os

DEBUG = False

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "test_secret_key")

ALLOWED_HOSTS = ["*"]

if os.getenv("POSTGRES_DB"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("POSTGRES_DB", "test_db"),
            "USER": os.getenv("POSTGRES_USER", "test_user"),
            "PASSWORD": os.getenv("POSTGRES_PASSWORD", "test_password"),
            "HOST": os.getenv("POSTGRES_HOST", "localhost"),
            "PORT": os.getenv("POSTGRES_PORT", "5432"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:",
        }
    }
