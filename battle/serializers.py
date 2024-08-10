from rest_framework import serializers
from .models import Battle

class BattleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Battle
        fields = ['battle_id', 'pokemon_a', 'pokemon_b', 'status', 'result']