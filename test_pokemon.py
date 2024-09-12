import unittest
from fastapi import HTTPException
import pandas as pd
import numpy as np
from helper import get_pokemon_data, calculate_damage, correct_spelling

# Load a sample Pokémon DataFrame for tests (you can create a mock CSV or in-memory data)
sample_data = {
    "name": ["Bulbasaur", "Charmander", "Squirtle"],
    "type1": ["grass", "fire", "water"],
    "type2": ["poison", np.nan, np.nan],
    "attack": [49, 52, 48],
    "against_grass": [0.5, 2.0, 0.5],
    "against_fire": [2.0, 0.5, 0.5],
    "against_water": [0.5, 2.0, 1.0],
}
df = pd.DataFrame(sample_data)


# Test case for get_pokemon_data
class TestPokemon(unittest.TestCase):

    def test_get_pokemon_data_valid(self):
        # Testing valid Pokémon name
        pokemon_data = get_pokemon_data("Bulbasaur")
        self.assertEqual(pokemon_data["name"], "Bulbasaur")

    def test_get_pokemon_data_invalid(self):
        # Testing invalid Pokémon name with a one-character mistake
        with self.assertRaises(HTTPException) as context:
            get_pokemon_data("NotAPokemon")  # Try a clearly invalid name
        self.assertEqual(context.exception.status_code, 404)

    def test_correct_spelling(self):
        # Test spelling correction with valid and invalid names
        valid_name = correct_spelling("Bulbasur", ["bulbasaur"])
        self.assertEqual(valid_name, "bulbasaur")

        with self.assertRaises(HTTPException):
            correct_spelling("NotAPokemon", ["bulbasaur", "charmander"])

    def test_calculate_damage_basic(self):
        # Test basic damage calculation between two valid Pokémon
        pokemon_a = df.iloc[0]
        pokemon_b = df.iloc[1]
        damage = calculate_damage(pokemon_a, pokemon_b)
        self.assertTrue(not np.isnan(damage))

    def test_calculate_damage_with_nan(self):
        # Test damage calculation where type2 or attack may be NaN or None
        pokemon_a = df.iloc[2]  # Squirtle, which has NaN type2
        pokemon_b = df.iloc[0]  # Bulbasaur
        damage = calculate_damage(pokemon_a, pokemon_b)
        self.assertTrue(not np.isnan(damage))

    def test_calculate_damage_nan_resistance(self):
        # Test if resistance values being NaN are handled properly
        pokemon_a = df.iloc[0]  # Bulbasaur
        pokemon_b = df.copy()  # A modified Pokemon with NaN resistance
        pokemon_b.loc[1, "against_grass"] = np.nan
        damage = calculate_damage(pokemon_a, pokemon_b.iloc[1])
        self.assertTrue(not np.isnan(damage))


if __name__ == "__main__":
    unittest.main()
