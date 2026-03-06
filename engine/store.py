from __future__ import annotations
import uuid
from engine.game import Game, BET


STARTING_BALANCE = 1000


class GameStore:
    def __init__(self):
        self._games: dict[str, Game] = {}
        self._balances: dict[str, int] = {}

    def get_balance(self, player_id: str) -> int:
        return self._balances.setdefault(player_id, STARTING_BALANCE)

    def _deduct_bet(self, player_id: str) -> None:
        balance = self.get_balance(player_id)
        if balance < BET:
            raise ValueError(f"Insufficient balance: {balance}")
        self._balances[player_id] = balance - BET

    def _apply_payout(self, player_id: str, amount: int) -> None:
        self._balances[player_id] = self._balances[player_id] + amount

    def start_game(self, player_id: str) -> Game:
        self._deduct_bet(player_id)
        game_id = str(uuid.uuid4())
        game = Game(game_id=game_id, player_id=player_id)
        game.deal_initial()
        self._games[game_id] = game
        if game.state.value == "complete":
            self._apply_payout(player_id, game.payout())
        return game

    def get_game(self, game_id: str) -> Game:
        game = self._games.get(game_id)
        if game is None:
            raise KeyError(f"Game not found: {game_id}")
        return game

    def apply_action(self, game_id: str, action: str) -> Game:
        game = self.get_game(game_id)
        if game.state.value == "complete":
            raise ValueError("Game is already complete")

        was_playing = game.state.value == "playing"

        if action == "hit":
            game.hit()
        elif action == "stand":
            game.stand()
        elif action == "double":
            if was_playing:
                self._deduct_bet(game.player_id)
            game.double()
        elif action == "split":
            game.split()
        else:
            raise ValueError(f"Unknown action: {action}")

        if game.state.value == "complete":
            self._apply_payout(game.player_id, game.payout())

        return game
