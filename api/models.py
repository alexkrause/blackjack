from __future__ import annotations
from pydantic import BaseModel
from typing import List, Literal, Optional


class StartRequest(BaseModel):
    player_id: str


class ActionRequest(BaseModel):
    action: Literal["hit", "stand", "double", "split"]


class CardSchema(BaseModel):
    rank: str
    suit: str
    face_up: bool


class GameResponse(BaseModel):
    game_id: str
    state: str
    player_hand: List[CardSchema]
    dealer_hand: List[CardSchema]
    result: Optional[str] = None
    balance: int
    split_hand: Optional[List[CardSchema]] = None
    split_result: Optional[str] = None
    on_split: Optional[bool] = None
