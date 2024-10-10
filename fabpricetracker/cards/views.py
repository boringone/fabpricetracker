from celery.result import AsyncResult
from django.db.models import Case, When, Value
from django.http import JsonResponse
from django_filters import CharFilter
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from rest_framework import viewsets
from django.apps import apps
from cards.serializers import CardsSerializer, CardSetSerializer
from cards.tasks import scrap_cm_card


class BasicCardFilter(FilterSet):
    set_id = CharFilter(field_name='cardprinting__set__name', lookup_expr='icontains')
    name = CharFilter(field_name='name', lookup_expr='icontains')
    type = CharFilter(field_name='types', lookup_expr='icontains')

    class Meta:
        model = apps.get_model('cards.BasicCard')
        fields = ['set_id', 'name', 'type']


class CardSetViewSet(viewsets.ModelViewSet):
    serializer_class = CardSetSerializer
    queryset = apps.get_model('cards.Set').objects.all()
    pagination_class = None


class CardsViewSet(viewsets.ModelViewSet):
    serializer_class = CardsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = BasicCardFilter

    def get_queryset(self):
        custom_order = Case(
            When(cardprinting__rarity__id='M', then=Value(1)),
            When(cardprinting__rarity__id='L', then=Value(2)),
        )
        return apps.get_model('cards.BasicCard').objects.filter(
            cardprinting__rarity__id__in=['M', 'L']).distinct().annotate(
            custom_order=custom_order).order_by('name', 'custom_order')


CORE_SETS = ['WTR', 'ARC', 'CRU', 'MON', 'ELE', 'EVR', 'UPR', 'DYN',
             'OUT', 'DTD', 'EVO', 'HVY', 'MST']


def scrap_card(request, card_printing_pk):
    card_model = apps.get_model('cards.cardprinting')
    try:
        card_model.objects.get(pk=card_printing_pk)
    except card_model.DoesNotExist:
        return JsonResponse({'error': 'Incorrect object data'})
    async_result = scrap_cm_card.delay(card_printing_pk)
    return JsonResponse({'task_id': async_result.task_id})


def view_task_result(request, task_id):
    result = AsyncResult(task_id)
    return JsonResponse({'result': result.get()})
