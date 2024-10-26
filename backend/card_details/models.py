from django.db import models

from cards.models import CardPrinting


class CardPriceDetails(models.Model):
    seller_name = models.CharField(max_length=50)
    card_condition = models.CharField(max_length=10)
    card_language = models.CharField(max_length=20)
    card_price = models.FloatField()
    quantity = models.IntegerField()
    seller_profile_link = models.CharField(max_length=100)
    seller_country = models.CharField(max_length=50)
    printing = models.ForeignKey(CardPrinting, on_delete=models.CASCADE)
