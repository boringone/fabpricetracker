from django.apps import apps
from rest_framework import serializers


class CardSetSerializer(serializers.ModelSerializer):

    class Meta:
        model = apps.get_model('cards.Set')
        fields = ['name']


class CardFoilingSerializer(serializers.ModelSerializer):

    class Meta:
        model = apps.get_model('cards.Foiling')
        fields = ['name']


class CardEditionSerializer(serializers.ModelSerializer):

    class Meta:
        model = apps.get_model('cards.Edition')
        fields = ['name']


class CardPrintingSerializer(serializers.ModelSerializer):
    set = CardSetSerializer()
    edition = CardEditionSerializer()
    foiling = CardFoilingSerializer()

    class Meta:
        model = apps.get_model('cards.CardPrinting')
        fields = '__all__'


class CardsSerializer(serializers.ModelSerializer):
    cardprinting_set = CardPrintingSerializer(many=True)

    class Meta:
        model = apps.get_model('cards.BasicCard')
        fields = '__all__'


class CardTypeSerializer(serializers.ModelSerializer):
    unnested_types = serializers.ListField()

    class Meta:
        model = apps.get_model('cards.BasicCard')
        fields = ['unnested_types']

    def to_representation(self, instance):
        return self.instance
