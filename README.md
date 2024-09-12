Pokemon Battle API
Welcome to the Pokemon Battle API project! This FastAPI application allows users to initiate battles between Pokemon and check the status of ongoing or completed battles. The API also includes functionality to detect and correct Pokémon name misspellings and calculate battle outcomes based on Pokemon attributes.

Features
List Pokemon: Retrieve a list of Pokemon with pagination.
Start Battle: Initiate a battle between two Pokemon.
Get Battle Status: Check the status and result of an ongoing or completed battle.
Spell Correction: Automatically correct and suggest Pokemon names based on Levenshtein distance.

Prerequisites
Before you begin, ensure you have the following installed:

Python 3.7 or later
All the requirements are present in requirements.txt


Initial setup:
1)git clone https://github.com/arushikohli5/Pokemon_assignment.git
2) cd Pokemon_assignment
3) pip install -r requirements.txt


Ensure the pokemon.csv file is in the root directory of the project. This file should contain Pokemon data used by the API.

Running the Application:
To start the FastAPI server, use the following command:

uvicorn main:app --reload
The application will be available at http://127.0.0.1:8000.

API Endpoints
List Pokemon
Endpoint: GET /getPokemonPagination/

Parameters:

skip (optional): Number of items to skip (pagination)
limit (optional): Number of items to return (pagination)
Response:

Returns a list of Pokemon with details.

Start Battle
Endpoint: POST /battle/

Parameters:

pokemon_a: Name of the first Pokémon
pokemon_b: Name of the second Pokémon
Response:

Returns a battle_id which can be used to check the status of the battle.

Get Battle Status
Endpoint: GET /battle/{battle_id}

Parameters:

battle_id: The ID of the battle
Response:

Returns the status and result of the battle.


Testing
To run the tests, 
python -m unittest test_pokemon.py
