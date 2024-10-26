from typing import Optional, Tuple

from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from rest_framework_simplejwt.tokens import Token

from users.models import CustomUserModel


class CustomJWTAuthentication(JWTTokenUserAuthentication):

    def authenticate(self, request: Request) -> Optional[Tuple[CustomUserModel, Token]]:
        if 'access' not in request.COOKIES:
            return None
        validated_token = self.get_validated_token(request.COOKIES['access'])
        return self.get_user(validated_token), validated_token
