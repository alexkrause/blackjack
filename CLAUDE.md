# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

**Install dependencies:**
```
pip install -r requirements.txt
```

**Run the API server:**
```
python main_api.py
```
API runs on `http://localhost:8000`. Interactive docs at `/docs`.

**Run the terminal UI:**
```
python main_terminal.py
```

## Architecture

The project has three layers:

### Engine (`engine/`)
Pure game logic with no I/O:
- `card.py` — `Card` and `Deck` classes
- `hand.py` — `Hand` class (value calculation with ace handling, blackjack/bust/pair detection)
- `game.py` — `Game` dataclass; encapsulates all game state and rules (hit/stand/double/split, dealer auto-play, result resolution, split hand lifecycle)
- `store.py` — `GameStore`; in-memory store managing `player_id → balance` and `game_id → Game`; handles bet deduction and payout on game completion

### API (`api/`)
FastAPI app exposing the engine over HTTP:
- `server.py` — creates `FastAPI` app and `GameStore`, wires them via `set_store()`
- `routes.py` — three endpoints: `POST /game/start`, `POST /game/{game_id}/action`, `GET /game/{game_id}/state`
- `models.py` — Pydantic request/response schemas

### UI (`ui/`)
Terminal rendering for the CLI mode (`main_terminal.py`).

### Key Design Details
- **State machine**: `Game.state` is `PLAYING` or `COMPLETE`. Actions raise `ValueError` if called on a completed game.
- **Split flow**: When a split exists, `Game.on_split` toggles which hand the player acts on. Split aces auto-resolve immediately.
- **Payouts** (fixed bet of $10): Blackjack pays $25 (returned bet + 1.5×), win pays $20, push returns $10, loss returns $0. Split hands pay even money only.
- **Balance**: `GameStore` holds balances in memory (starting at $1000); not persisted across server restarts.
- **Dealer first card**: dealt face-down; revealed when dealer plays.

## Planned Web Frontend
`specs_web.md` describes a planned web UI consuming the existing REST API — responsive casino-themed design targeting desktop and mobile.
