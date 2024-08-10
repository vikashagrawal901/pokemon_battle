import pandas as pd
import difflib
import math
class BattleSimulator:
    def __init__(self, pokemon_data):
        self.pokemon_data = pokemon_data

    def normalize_name(self, name):
        return name.strip().lower()

    def find_pokemon(self, name):
        normalized_name = self.normalize_name(name)
        possible_matches = difflib.get_close_matches(normalized_name, self.pokemon_data['name'].str.lower().tolist(), n=2, cutoff=0.8)
        if not possible_matches:
            raise ValueError(f"Pokémon {name} not found.")
        if len(possible_matches) > 1:
            raise ValueError(f"Multiple Pokémon matches found for {name}.")
        return self.pokemon_data[self.pokemon_data['name'].str.lower() == possible_matches[0]].iloc[0]

    def calculate_damage(self, attacker, defender):
        try:
            # Ensure attacker and defender have the required fields
            if 'attack' not in attacker or 'type1' not in attacker:
                raise ValueError("Attacker must have 'attack' and 'type1' fields.")
            if f'against_{attacker["type1"]}' not in defender:
                raise ValueError(f"Defender must have 'against_{attacker['type1']}' field.")

            attack = attacker['attack']
            type1 = attacker['type1']
            type2 = attacker.get('type2', None)

            # Handle possible nan values
            if isinstance(type1, float) and math.isnan(type1):
                raise ValueError("Type1 of attacker is nan.")
            if type2 and (isinstance(type2, float) and math.isnan(type2)):
                type2 = None

            against_type1 = defender[f'against_{type1}']
            against_type2 = defender.get(f'against_{type2}', 1.0) if type2 else 1.0


            damage = (attack / 200) * 100 - (((against_type1 / 4) * 100) + ((against_type2 / 4) * 100))
            return damage
        except Exception as e:
            print("error as e ", e)

    def battle(self, pokemon_a_name, pokemon_b_name):
        pokemon_a = self.find_pokemon(pokemon_a_name)
        pokemon_b = self.find_pokemon(pokemon_b_name)
        print("pokemon_a ", pokemon_a)
        print("pokemon_b", pokemon_b)

        damage_a_to_b = self.calculate_damage(pokemon_a, pokemon_b)
        damage_b_to_a = self.calculate_damage(pokemon_b, pokemon_a)

        if damage_a_to_b > damage_b_to_a:
            winner = pokemon_a['name']
            margin = damage_a_to_b - damage_b_to_a
        elif damage_b_to_a > damage_a_to_b:
            winner = pokemon_b['name']
            margin = damage_b_to_a - damage_a_to_b
        else:
            winner = 'Draw'
            margin = 0

        return winner, margin
