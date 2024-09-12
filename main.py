from fastapi import FastAPI, BackgroundTasks, HTTPException
import pandas as pd
from uuid import uuid4
import Levenshtein
import numpy as np
import asyncio

app = FastAPI()
lock = asyncio.Lock()


# Loading the dataset
df = pd.read_csv("pokemon.csv")
print(df["name"])

# battle storage
battles = {}


# Diffrent status for battle
class BattleStatus:
    IN_PROGRESS = "BATTLE_INPROGRESS"
    COMPLETED = "BATTLE_COMPLETED"
    FAILED = "BATTLE_FAILED"


# Get a list of valid Pokémon names (lowercase)
valid_pokemon_names = df["name"].str.lower().tolist()


# API to start a battle
@app.post("/battle/")
def start_battle(pokemon_a: str, pokemon_b: str, background_tasks: BackgroundTasks):
    pokemon_a = get_pokemon_data(pokemon_a)
    pokemon_b = get_pokemon_data(pokemon_b)
    battle_id = str(uuid4())
    battles[battle_id] = {"status": BattleStatus.IN_PROGRESS, "result": None}
    # battle_simulator(battle_id, pokemon_a, pokemon_b)
    background_tasks.add_task(battle_simulator, battle_id, pokemon_a, pokemon_b)
    return {"battle_id": battle_id}


# Helper function to fetch Pokémon data
def get_pokemon_data(pokemon_name: str):
    corrected_name = correct_spelling(pokemon_name, valid_pokemon_names)

    pokemon = df[df["name"].str.lower() == corrected_name]
    if pokemon.empty:
        raise HTTPException(status_code=404, detail="Pokémon not found")
    return pokemon.iloc[0]


# Background battle function
async def battle_simulator(battle_id: str, pokemon_a: str, pokemon_b: str):
    async with lock:
        try:
            # breakpoint()
            # print("called")
            # Fetch Pokémon data
            # pkmn_a = get_pokemon_data(pokemon_a)
            # pkmn_b = get_pokemon_data(pokemon_b)

            # Perform battle logic (e.g., damage calculation)
            damage_a_to_b = calculate_damage(pkmn_a, pkmn_b)
            damage_b_to_a = calculate_damage(pkmn_b, pkmn_a)

            # Determine winner
            if damage_a_to_b > damage_b_to_a:
                winner = pokemon_a
                margin = damage_a_to_b - damage_b_to_a
            elif damage_b_to_a > damage_a_to_b:
                winner = pokemon_b
                margin = damage_b_to_a - damage_a_to_b
            else:
                winner = "draw"
                margin = 0
            # print(battles)
            # Update battle status
            battles[battle_id] = {
                "status": BattleStatus.COMPLETED,
                "result": BattleResult(winnerName=winner, wonByMargin=margin),
            }
        except Exception as e:
            battles[battle_id] = {"status": BattleStatus.FAILED, "result": None}


def calculate_damage(pokemon_a, pokemon_b):
    """
    Calculates the damage dealt by Pokemon A to Pokemon B.
    Formula is based on the provided attack value and resistance.
    """
    type1_a = pokemon_a["type1"]
    type2_a = pokemon_a["type2"]
    attack_a = pokemon_a["attack"]

    # Extract 'against_' values for type1 and type2 from Pokémon B
    against_type1_b = pokemon_b[f"against_{type1_a}"]
    against_type2_b = pokemon_b[f"against_{type2_a}"] if type2_a else 1

    # Calculate damage based on the provided formula
    damage = (attack_a / 200) * 100 - (
        ((against_type1_b / 4) * 100) + ((against_type2_b / 4) * 100)
    )
    return damage


# Helper function to detect spelling mistakes using Levenshtein distance
def correct_spelling(pokemon_name: str, choices: list):
    pokemon_name_lower = pokemon_name.lower()

    # Check for close matches with Levenshtein distance of 1 (one-word mistake)
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
