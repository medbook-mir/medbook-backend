from .base import *
import dj_database_url
import os

DEBUG = os.getenv('DJANGO_DEBUG', 'False').lower() == 'true'
SECRET_KEY = 'django-insecure-ic$x3f-&ajn6(p5&7pxjjcv!+v%m*kxiv4=qp50x8bj=k)e105'

ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '').split(',') if os.getenv('DJANGO_ALLOWED_HOSTS') else []

DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.config(
            default='postgresql://test_database_edai_user:5H42RaqlJkI1oZf4B2hboPvYn5kPJBPYY@dpg-d0q7338d13ps73bcv1hg-a:5422/test_database_edai',
            conn_max_age=600,
        )
    }

    DATABASES['default']['TEST'] = {
        'NAME': 'test_database_edai',
        'MIRROR': None,
    }
    print("this is a test database")

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

STORAGES = {
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = []
