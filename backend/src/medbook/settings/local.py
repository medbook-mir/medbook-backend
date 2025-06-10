from .base import *
import os

DEBUG = True
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'Django_secret_key')
ALLOWED_HOSTS = ['localhost', '127.0.0.1']


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB', 'medbook'),
        'USER': os.getenv('POSTGRES_USER', 'medbook_user'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'password'),
        'HOST': os.getenv('POSTGRES_HOST', 'db'), 
        'PORT': os.getenv('POSTGRES_PORT', '5432'),
    }
}