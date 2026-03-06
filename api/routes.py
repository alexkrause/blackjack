from __future__ import annotations
from fastapi import APIRouter, HTTPException
from api.models import StartRequest, ActionRequest, GameResponse
from engine.store import GameStore

router = APIRouter()
_store: GameStore | None = None


def set_store(store: GameStore) -> None:
    global _store
    _store = store


def _get_store() -> GameStore:
    if _store is None:
        raise RuntimeError("Store not initialized")
    return _store


def _game_response(game, store: GameStore) -> GameResponse:
    return GameResponse(
        **game.to_dict(),
        balance=store.get_balance(game.player_id),
    )


@router.post("/game/start", response_model=GameResponse)
def start_game(body: StartRequest):
    store = _get_store()
    try:
        game = store.start_game(body.player_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return _game_response(game, store)


@router.post("/game/{game_id}/action", response_model=GameResponse)
def game_action(game_id: str, body: ActionRequest):
    store = _get_store()
    try:
        game = store.apply_action(game_id, body.action)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except (ValueError, NotImplementedError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    return _game_response(game, store)


@router.get("/game/{game_id}/state", response_model=GameResponse)
def game_state(game_id: str):
    store = _get_store()
    try:
        game = store.get_game(game_id)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return _game_response(game, store)
