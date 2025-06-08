from .base import BASE_DIR
import dj_database_url
import os
import logging

logger = logging.getLogger(__name__)

DEBUG = os.getenv('DJANGO_DEBUG', 'False').lower() == 'true'
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'fallback-secret-key')

ALLOWED_HOSTS = list(filter(None, os.getenv('DJANGO_ALLOWED_HOSTS', '').split(',')))

DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.config(conn_max_age=600),
    }
    logger.info("Connected to test database")
else:
    print("Something has gonna wrong!")

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

STORAGES = {
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = []
