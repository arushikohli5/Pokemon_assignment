import pandas as pd
import numpy as np
import Levenshtein
from fastapi import FastAPI, BackgroundTasks, HTTPException

df = pd.read_csv("pokemon.csv")
valid_pokemon_names = df["name"].str.lower().tolist()


# Function to get the data for a particular pokemon
def get_pokemon_data(pokemon_name: str):
    corrected_name = correct_spelling(pokemon_name, valid_pokemon_names)

    pokemon = df[df["name"].str.lower() == corrected_name]
    if pokemon.empty:
        raise HTTPException(status_code=404, detail="Pokémon not found")
    return pokemon.iloc[0]


# Function to check if the correct pokemon is present
def correct_spelling(pokemon_name: str, choices: list):
    pokemon_name_lower = pokemon_name.lower()

    # Checking for close matches with Levenshtein distance of 1 (one-word mistake)
    for valid_name in choices:
        if Levenshtein.distance(pokemon_name_lower, valid_name) <= 1:
            return valid_name

    # If no one-word mistakes found, provide suggestions with more than one-word mistake
    suggestions = [
        name for name in choices if Levenshtein.distance(pokemon_name_lower, name) <= 2
    ]
    if suggestions:
        raise HTTPException(
            status_code=400,
            detail=f"More than one-word mistake. Did you mean: {', '.join(suggestions)}?",
        )

    # If no match or suggestion, throw an error
    raise HTTPException(
        status_code=404,
        detail=f"Pokémon '{pokemon_name}' not found or too many spelling mistakes.",
    )


def calculate_damage(pokemon_a, pokemon_b):
    """
    Calculates the damage dealt by Pokemon A to Pokemon B.
    Formula is based on the provided attack value and resistance.
    """
    # breakpoint()
    type1_a = pokemon_a["type1"]
    type2_a = pokemon_a["type2"]
    attack_a = pokemon_a["attack"]

    if attack_a is None:
        attack_a = 0
    if not isinstance(type2_a, str) and np.isnan(type2_a):
        type2_a = 0.0
    if type1_a is None or type1_a == "":
        type1_a = ""

    # Extract 'against_' values for type1 and type2 from Pokemon B
    against_type1_b = pokemon_b[f"against_{type1_a}"]
    against_type2_b = pokemon_b[f"against_{type2_a}"] if type2_a else 1

    if np.isnan(against_type1_b):
        against_type1_b = 1.0  # Set default resistance to 1 if NaN
    if np.isnan(against_type2_b):
        against_type2_b = 1  # Set default resistance to 1 if NaN

    # Calculate damage based on the formula
    damage = (attack_a / 200) * 100 - (
        ((against_type1_b / 4) * 100) + ((against_type2_b / 4) * 100)
    )
    return damage
