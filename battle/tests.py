from django.test import TestCase
from rest_framework.test import APIClient
from .models import Battle
from .simulator import BattleSimulator
import pandas as pd

class BattleSimulatorTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.pokemon_data = pd.read_csv('data/pokemon.csv')
        cls.battle_simulator = BattleSimulator(cls.pokemon_data)

    def test_normalize_name(self):
        self.assertEqual(self.battle_simulator.normalize_name(' Pikachu '), 'pikachu')

    def test_find_pokemon(self):
        pikachu = self.battle_simulator.find_pokemon('Pikachu')
        self.assertEqual(pikachu['name'], 'Pikachu')

    def test_calculate_damage(self):
        pikachu = self.battle_simulator.find_pokemon('Pikachu')
        bulbasaur = self.battle_simulator.find_pokemon('Bulbasaur')
        damage = self.battle_simulator.calculate_damage(pikachu, bulbasaur)
        self.assertIsInstance(damage, float)

    def test_battle(self):
        winner, margin = self.battle_simulator.battle('Pikachu', 'Bulbasaur')
        self.assertIsInstance(winner, str)
        self.assertIsInstance(margin, float)

class BattleAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_battle(self):
        response = self.client.post('/api/battles/create/', {'pokemon_a': 'Pikachu', 'pokemon_b': 'Bulbasaur'})
        self.assertEqual(response.status_code, 201)
        self.assertIn('battle_id', response.data)

    def test_get_battle_status(self):
        response = self.client.post('/api/battles/create/', {'pokemon_a': 'Pikachu', 'pokemon_b': 'Bulbasaur'})
        battle_id = response.data['battle_id']
        response = self.client.get(f'/api/battles/status/{battle_id}/')
        self.assertEqual(response.status_code, 200)
