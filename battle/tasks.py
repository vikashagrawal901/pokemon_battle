from .models import Battle
from .factory import BattleSimulatorFactory
from django.conf import settings
from background_task import background


# @background(schedule=10)
def battle_task(battle_id, pokemon_a_name, pokemon_b_name):
    simulator = BattleSimulatorFactory.create_simulator('default')
    try:
        winner, margin = simulator.battle(pokemon_a_name, pokemon_b_name)
        result = {
            'status': 'BATTLE_COMPLETED',
            'result': {
                'winnerName': winner,
                'wonByMargin': margin
            }
        }
    except Exception as e:
        print("error as e ", e)
        result = {
            'status': 'BATTLE_FAILED',
            'result': None
        }
    Battle.objects.filter(battle_id=battle_id).update(status=result['status'], result=result['result'])
