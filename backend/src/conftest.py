# backend/src/conftest.py
import pytest
from django.conf import settings

def pytest_configure():
    settings.DATABASES['default']['TEST'] = {
        'NAME': settings.DATABASES['default']['NAME']
    }

@pytest.fixture(scope='session')
def django_db_setup():
    """Override default test database creation"""
    pass