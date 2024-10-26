from django.conf import settings

from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.models import CustomUserModel
from users.serializers import UserSerializer



class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUserModel.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data.pop('password')
        return response


class CustomTokenObtainView(TokenObtainPairView):

    def post(self, request: Request, *args, **kwargs) -> Response:
        response = super().post(request, *args, **kwargs)
        response.set_cookie('access', response.data['access'], max_age=settings.ACCESS_COOKIES_MAX_AGE,
                            secure=settings.COOKIES_SECURE, httponly=True, samesite=settings.COOKIES_SAMESITE)
        response.set_cookie('refresh', response.data['refresh'], max_age=settings.REFRESH_COOKIES_MAX_AGE,
                            secure=settings.COOKIES_SECURE, httponly=True, samesite=settings.COOKIES_SAMESITE)

        return response

class CustomTokenRefreshView(TokenRefreshView):

    def post(self, request: Request, *args, **kwargs) -> Response:
        refresh_token = request.COOKIES.get('refresh')
        if refresh_token:
            request.data['refresh'] = refresh_token
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            access_token = response.data.get('access')
            response.set_cookie(
                'access',
                access_token,
                max_age=settings.ACCESS_COOKIES_MAX_AGE,
                secure=settings.COOKIES_SECURE,
                httponly=True,
                samesite=settings.COOKIES_SAMESITE
            )
        return response
