from http.client import responses
from idlelib.pyshell import use_subprocess

import pytest

from users.models import CustomUserModel


class TestUser:

    def teardown_method(self):
        self.teardown_user()

    @staticmethod
    def teardown_user():
        CustomUserModel.objects.all().delete()

    @pytest.fixture()
    def default_user_data(self):
        return {'email': 'wplew1@wp.pl', 'password': 'wplew1'}

    @pytest.fixture()
    def new_user(self, api_client, default_user_data):
        def _new_user(user_data=None):
            if user_data is None:
                user_data = default_user_data
            return api_client.post('/users/', user_data)
        yield _new_user
        CustomUserModel.objects.all().delete()

    @pytest.fixture()
    def default_user(self, new_user):
        return new_user()

    def test_user_creation(self, default_user):
        assert default_user.data.get('email') == 'wplew1@wp.pl'

    def test_token_refresh(self, api_client, default_user):
        login_response = api_client.post(
            '/auth/jwt/create/',
            {
                'email': default_user.data['email'],
                'password': "wplew1"
            }
        )
        assert login_response.status_code == 200
        refresh_response = api_client.post('/auth/jwt/refresh/')
        assert 'access' in refresh_response.data
        assert refresh_response.status_code == 200

    def test_wrong_email_user(self, new_user):
        response = new_user({'email': 'wplew2', "password": 'wplew1'})
        assert response.status_code == 400
        assert 'email' in response.data.keys()

    def test_create_superuser_method(self, default_user_data):
        user_obj = CustomUserModel.objects.create_superuser(**default_user_data)
        assert user_obj.is_superuser == True
        assert user_obj.is_staff == True

    def test_invalid_superuser_creation(self):
        with pytest.raises(ValueError) as user_error:
            CustomUserModel.objects.create_superuser(**{})
        assert user_error.value.args[0] == 'The given email must be set'

        with pytest.raises(ValueError) as user_error:
            CustomUserModel.objects.create_superuser(**{'is_staff': False})
        assert user_error.value.args[0] == "Superuser must have is_staff=True."

        with pytest.raises(ValueError) as user_error:
            CustomUserModel.objects.create_superuser(**{'is_superuser': False})
        assert user_error.value.args[0] == "Superuser must have is_superuser=True."


