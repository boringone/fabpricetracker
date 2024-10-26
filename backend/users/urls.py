from django.urls import path, include
from rest_framework.routers import SimpleRouter

from users.views import UserViewSet, CustomTokenObtainView, CustomTokenRefreshView

router = SimpleRouter()
router.register(
    'users',
    UserViewSet,
    'users'
)


urlpatterns = [
    path('', include(router.urls)),
    path('auth/jwt/create/', CustomTokenObtainView.as_view(), name="jwt-create"),
    path('auth/jwt/refresh/', CustomTokenRefreshView.as_view(), name="jwt-refresh"),
    path(r'auth/', include('djoser.urls')),
    path(r'auth/', include('djoser.urls.jwt')),
]
