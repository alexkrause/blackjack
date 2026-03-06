
# Blackjack Game Specification

## Overview
A terminal-based blackjack game with RESTful API for conversational interfaces (Telegram, etc.).

## Architecture

### Components
- **Game Engine**: Core blackjack logic
- **API Server**: REST endpoints for game state and actions
- **Terminal UI**: Command-line interface
- **Conversation Bridge**: Adapter for external platforms (Telegram via OpenClaw)

## API Specification

### Endpoints

**POST /game/start**
- Request: `{ "player_id": "string" }`
- Response: `{ "game_id": "string", "player_hand": [...], "dealer_hand": [...], "balance": number }`

**POST /game/{game_id}/action**
- Request: `{ "action": "hit" | "stand" | "double" | "split" }`
- Response: `{ "game_id", "state": "playing" | "complete", "player_hand": [...], "dealer_hand": [...], "result": "win" | "lose" | "push", "balance": number }`

**GET /game/{game_id}/state**
- Response: Current game state object

## Game Logic

### Rules
- Standard blackjack (21 points max)
- Dealer hits on 16, stands on 17+
- Blackjack pays 3:2
- Push on equal hands

### Game Flow
1. Deal initial cards (player 2, dealer 1 visible)
2. Player turn: hit/stand/double/split
3. Dealer turn: automatic play
## Terminal Interface
- Display current hands, balance, options
- Accept player commands via stdin
- Call API endpoints internally

## Commands

### Help
- **Command**: `help`
- **Description**: Displays available commands and their usage
- **Output**: Lists all user commands with brief descriptions
- **Example**: 
  ```
  > help
  Available commands:
    hit      - Request another card
    stand    - End your turn
    double   - Double your bet and take one card
    split    - Split a pair into two hands
    balance  - Show current balance
    quit     - Exit the game
    help     - Show this help message
  ```
