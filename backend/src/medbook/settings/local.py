# medbook/settings/local.py
from .base import *

DEBUG = True
SECRET_KEY = 'django-insecure-ic$x3f-&ajn6(p5&7pxjjcv!+v%m*kxiv4=qp50x8bj=k)e105'
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}