from django.urls import path, include
from rest_framework.routers import SimpleRouter

from cards.views import CardsViewSet

router = SimpleRouter()
router.register(
    'card-info',
    CardsViewSet,
    'card-info'
)

urlpatterns = [
    path('', include(router.urls)),
]