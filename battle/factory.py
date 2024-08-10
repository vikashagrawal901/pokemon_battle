from .simulator import BattleSimulator
import pandas as pd

class BattleSimulatorFactory:
    @staticmethod
    def create_simulator(simulator_type='default'):
        pokemon_data = pd.read_csv('Data/pokemon.csv')
        if simulator_type == 'default':
            return BattleSimulator(pokemon_data)
        else:
            raise ValueError(f"Simulator type {simulator_type} is not supported")
