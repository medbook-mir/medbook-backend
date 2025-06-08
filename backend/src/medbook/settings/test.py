from .base import *
import dj_database_url
import os

DEBUG = os.getenv('DJANGO_DEBUG', 'False').lower() == 'true'
SECRET_KEY = 'django-insecure-ic$x3f-&ajn6(p5&7pxjjcv!+v%m*kxiv4=qp50x8bj=k)e105'

ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '').split(',') if os.getenv('DJANGO_ALLOWED_HOSTS') else []

DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL:
    # DATABASES = {
    #     'default': dj_database_url.config(
    #         default=DATABASE_URL,
    #         conn_max_age=600,
    #         ssl_require=True
    #     )
    # }
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('TEST_DB_URL', 'test_database_edai'),
            'USER': os.getenv('TEST_DB_USER','medbook_user'),
            'PASSWORD': os.getenv('TEST_DB_PASSWORD','password'),
            'HOST': os.getenv('TEST_DB_HOST', 'localhost'),
            'PORT': os.getenv('TEST_DB_PORT', '5432'),
        }
    }
    print("this is a test database")
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = []