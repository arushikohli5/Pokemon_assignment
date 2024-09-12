from pydantic import BaseModel
from typing import Optional


class Pokemon(BaseModel):
    name: str
    type1: str
    type2: Optional[str] = None
    attack: int
    against_grass: float
    against_poison: float
    # Add fields for other Pokémon types (against_water, etc.)


class BattleResult(BaseModel):
    winnerName: str
    wonByMargin: float


class BattleStatusResponse(BaseModel):
    status: str
    result: Optional[BattleResult] = None
