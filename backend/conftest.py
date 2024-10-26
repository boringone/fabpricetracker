import os

import pytest
from django.conf import settings
from django.db import connections
from rest_framework.test import APIClient

from users.models import CustomUserModel


@pytest.fixture(scope='session')
def django_db_setup():
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'test_django',
        'ATOMIC_REQUESTS': True,
        'USER': os.getenv('POSTGRES_USER', ''),
        'PASSWORD': os.getenv("POSTGRES_PASSWORD", ''),
        'HOST': os.getenv('POSTGRES_HOST', ''),
        'PORT': os.getenv('POSTGRES_PORT', '')
    }
    # re-configure the settings given the changed database config
    connections._settings = connections.configure_settings(settings.DATABASES)
    # open a connection to the database with the new database config
    connections["default"] = connections.create_connection("default")


@pytest.fixture(scope="function")
def api_client(test_user) -> APIClient:
    """
    Fixture to provide an API client
    :return: APIClient
    """
    client = APIClient()
    client.post(
        '/auth/jwt/create/',
        {
            'email': test_user.email,
            'password': "123!qwerty"
        }
    )
    return client

@pytest.fixture(scope='session')
def rf(test_user):
    from django.test import RequestFactory

    factory = RequestFactory()
    factory.user = test_user
    return factory


@pytest.fixture(scope='session')
def test_user(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        user = CustomUserModel.objects.create_user(
                email="sample2@gmail.com",
                password="123!qwerty",
                first_name='Wojciech',
                last_name='Testowy')
        yield user
        user.delete()
