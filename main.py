from fastapi import FastAPI, BackgroundTasks, HTTPException
import pandas as pd
from uuid import uuid4
import Levenshtein
import numpy as np
import asyncio
from models import BattleStatusResponse, BattleResult
from helper import get_pokemon_data, correct_spelling, calculate_damage


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


# Geenerating a list of valid Pokémon names (lowercase)
valid_pokemon_names = df["name"].str.lower().tolist()


# API to start a battle
@app.post("/battle/")
def start_battle(pokemon_a: str, pokemon_b: str, background_tasks: BackgroundTasks):
    # breakpoint()
    str_pk1 = pokemon_a
    str_pk2 = pokemon_b
    pokemon_a = get_pokemon_data(pokemon_a)
    pokemon_b = get_pokemon_data(pokemon_b)
    battle_id = str(uuid4())
    battles[battle_id] = {"status": BattleStatus.IN_PROGRESS, "result": None}
    # battle_simulator(battle_id, pokemon_a, pokemon_b)
    background_tasks.add_task(battle_simulator, battle_id, str_pk1, str_pk2)
    return {"battle_id": battle_id}


# API to Get battle status
@app.get("/battle/{battle_id}", response_model=BattleStatusResponse)
def get_battle_status(battle_id: str):
    battle = battles.get(battle_id)
    if not battle:
        raise HTTPException(status_code=404, detail="Battle not found")
    return battle


# Background battle function
async def battle_simulator(battle_id: str, pokemon_a: str, pokemon_b: str):
    async with lock:
        try:
            breakpoint()
            # get the data for pokemon
            pkm_a = get_pokemon_data(pokemon_a)
            pkm_b = get_pokemon_data(pokemon_b)

            # Perform battle logic
            damage_a_to_b = calculate_damage(pkm_a, pkm_b)
            damage_b_to_a = calculate_damage(pkm_b, pkm_a)

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
            battles[battle_id] = {
                "status": BattleStatus.COMPLETED,
                "result": BattleResult(winnerName=winner, wonByMargin=margin),
            }
        except Exception as e:
            battles[battle_id] = {"status": BattleStatus.FAILED, "result": None}
