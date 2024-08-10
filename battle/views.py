from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Battle
from .serializers import BattleSerializer
from .tasks import battle_task
import uuid
from django.utils import timezone

class BattleListView(APIView):
    def get(self, request):
        battles = Battle.objects.all()
        serializer = BattleSerializer(battles, many=True)
        return Response(serializer.data)

class BattleCreateView(APIView):
    def post(self, request):
        pokemon_a = request.data.get('pokemon_a')
        pokemon_b = request.data.get('pokemon_b')
        if not pokemon_a or not pokemon_b:
            return Response({'error': 'Both Pokémon names are required.'}, status=status.HTTP_400_BAD_REQUEST)
        battle_id = uuid.uuid4()
        battle = Battle.objects.create(battle_id=battle_id, pokemon_a=pokemon_a, pokemon_b=pokemon_b)
        battle_task(str(battle_id), pokemon_a, pokemon_b)  ##schedule=timezone.now()
        return Response({'battle_id': str(battle_id)}, status=status.HTTP_201_CREATED)

class BattleStatusView(APIView):
    def get(self, request, battle_id):
        try:
            battle = Battle.objects.get(battle_id=battle_id)
            serializer = BattleSerializer(battle)
            return Response(serializer.data)
        except Battle.DoesNotExist:
            return Response({'error': 'Battle not found'}, status=status.HTTP_404_NOT_FOUND)


