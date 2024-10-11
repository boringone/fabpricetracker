from django.urls import path, include
from rest_framework.routers import SimpleRouter

from cards.views import CardsViewSet, scrap_card,\
    view_task_result, CardSetViewSet, CardsTypeViewSet

router = SimpleRouter()
router.register(
    'card-info',
    CardsViewSet,
    'card-info'
)
router.register(
    'set-info',
    CardSetViewSet,
    'set-info'
)
router.register(
    'types-info',
    CardsTypeViewSet,
    'types-info'
)


urlpatterns = [
    path('', include(router.urls)),
    path('task_queue/<str:card_printing_pk>', scrap_card),
    path('task_result/<str:task_id>', view_task_result),
]
