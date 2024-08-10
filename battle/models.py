from django.db import models
import uuid
# Create your models here.


class Battle(models.Model):
    battle_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pokemon_a = models.CharField(max_length=100)
    pokemon_b = models.CharField(max_length=100)
    status = models.CharField(max_length=50, default='BATTLE_INPROGRESS')
    result = models.JSONField(null=True, blank=True)



