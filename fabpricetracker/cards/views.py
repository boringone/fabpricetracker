from django.db.models import Case, When, Value
from rest_framework import viewsets
from django.apps import apps
from cards.serializers import CardsSerializer


class CardsViewSet(viewsets.ModelViewSet):
    serializer_class = CardsSerializer

    def get_queryset(self):
        custom_order = Case(
            When(cardprinting__rarity__id='M', then=Value(1)),
            When(cardprinting__rarity__id='L', then=Value(2)),
        )
        return apps.get_model('cards.BasicCard').objects.filter(
            cardprinting__rarity__id__in=['M', 'L']).distinct().annotate(
            custom_order=custom_order).order_by('name', 'custom_order')
