from django.contrib.postgres.fields import ArrayField
from django.db import models


class BasicCard(models.Model):
    unique_id = models.CharField(max_length=21, primary_key=True)
    name = models.CharField(max_length=255)
    pitch = models.CharField(max_length=10)
    cost = models.CharField(max_length=10)
    power = models.CharField(max_length=10)
    defense = models.CharField(max_length=10)
    health = models.CharField(max_length=10)
    intelligence = models.CharField(max_length=10)
    types = ArrayField(models.CharField(max_length=255))
    card_keywords = ArrayField(models.CharField(max_length=255))
    abilities_and_effects = ArrayField(models.CharField(max_length=255))
    ability_and_effect_keywords = ArrayField(models.CharField(max_length=255))
    granted_keywords = ArrayField(models.CharField(max_length=255))
    removed_keywords = ArrayField(models.CharField(max_length=255))
    interacts_with_keywords = ArrayField(models.CharField(max_length=255))
    functional_text = models.CharField(max_length=10000)
    functional_text_plain = models.CharField(max_length=10000)
    type_text = models.CharField(max_length=1000)

    class Meta:
        db_table = 'FabCards'
        unique_together = ('name', 'pitch')


class ArtVariation(models.Model):
    id = models.CharField(max_length=3, primary_key=True)
    name = models.CharField(max_length=50)


class Rarity(models.Model):
    id = models.CharField(max_length=2, primary_key=True)
    description = models.CharField(max_length=50)


class Foiling(models.Model):
    id = models.CharField(max_length=2, primary_key=True)
    name = models.CharField(max_length=50)


class Edition(models.Model):
    id = models.CharField(max_length=2, primary_key=True)
    name = models.CharField(max_length=100)


class Set(models.Model):
    unique_id = models.CharField(max_length=21, primary_key=True)
    id = models.CharField(max_length=4)
    name = models.CharField(max_length=50)


class SetPrinting(models.Model):
    unique_id = models.CharField(max_length=21, primary_key=True)
    edition = models.ForeignKey(Edition, on_delete=models.PROTECT)
    start_card_id = models.CharField(max_length=15)
    end_card_id = models.CharField(max_length=15)
    set_obj = models.ForeignKey(Set, on_delete=models.PROTECT)
    initial_release_date = models.DateField(null=True)


class CardPrinting(models.Model):
    unique_id = models.CharField(max_length=21, primary_key=True)
    id = models.CharField(max_length=8)
    card = models.ForeignKey(BasicCard, on_delete=models.CASCADE)
    set = models.ForeignKey(Set, on_delete=models.PROTECT)
    edition = models.ForeignKey(Edition, on_delete=models.PROTECT)
    foiling = models.ForeignKey(Foiling, on_delete=models.PROTECT)
    rarity = models.ForeignKey(Rarity, on_delete=models.PROTECT)
    art_variation = models.ForeignKey(ArtVariation, on_delete=models.PROTECT, null=True)
    image_url = models.CharField(null=True, blank=False)
    objects = models.Manager()
