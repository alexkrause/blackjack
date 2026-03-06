from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from engine.card import Deck
from engine.hand import Hand


class GameState(str, Enum):
    PLAYING = "playing"
    COMPLETE = "complete"


class Result(str, Enum):
    WIN = "win"
    LOSE = "lose"
    PUSH = "push"
    BLACKJACK = "blackjack"


BET = 10
BLACKJACK_PAYOUT = 25  # bet returned + 1.5× profit
WIN_PAYOUT = 20        # bet returned + $10 profit
PUSH_PAYOUT = 10       # bet returned


@dataclass
class Game:
    game_id: str
    player_id: str
    deck: Deck = field(default_factory=Deck)
    player_hand: Hand = field(default_factory=Hand)
    dealer_hand: Hand = field(default_factory=Hand)
    state: GameState = GameState.PLAYING
    result: Result | None = None

    def deal_initial(self) -> None:
        self.player_hand.add(self.deck.deal())
        dealer_card = self.deck.deal()
        dealer_card.face_up = False
        self.dealer_hand.add(dealer_card)
        self.player_hand.add(self.deck.deal())
        self.dealer_hand.add(self.deck.deal())

        # Check for player blackjack immediately
        if self.player_hand.is_blackjack():
            self._resolve()

    def hit(self) -> None:
        self._require_playing()
        self.player_hand.add(self.deck.deal())
        if self.player_hand.is_bust():
            self._resolve()

    def stand(self) -> None:
        self._require_playing()
        self._dealer_play()
        self._resolve()

    def double(self) -> None:
        self._require_playing()
        if len(self.player_hand.cards) != 2:
            raise ValueError("Can only double on initial two cards")
        self.player_hand.add(self.deck.deal())
        if not self.player_hand.is_bust():
            self._dealer_play()
        self._resolve()

    def split(self) -> None:
        raise NotImplementedError("Split is not yet implemented")

    def _require_playing(self) -> None:
        if self.state != GameState.PLAYING:
            raise ValueError("Game is already complete")

    def _dealer_play(self) -> None:
        self.dealer_hand.reveal_all()
        while self.dealer_hand.value() < 17:
            self.dealer_hand.add(self.deck.deal())

    def _resolve(self) -> None:
        self.dealer_hand.reveal_all()
        self.state = GameState.COMPLETE

        p = self.player_hand.value()
        d = self.dealer_hand.value()

        if self.player_hand.is_bust():
            self.result = Result.LOSE
        elif self.player_hand.is_blackjack() and not self.dealer_hand.is_blackjack():
            self.result = Result.BLACKJACK
        elif self.dealer_hand.is_bust():
            self.result = Result.WIN
        elif p > d:
            self.result = Result.WIN
        elif p < d:
            self.result = Result.LOSE
        else:
            self.result = Result.PUSH

    def payout(self) -> int:
        """Return amount to add back to balance (bet was already deducted)."""
        if self.result == Result.BLACKJACK:
            return BLACKJACK_PAYOUT
        if self.result == Result.WIN:
            return WIN_PAYOUT
        if self.result == Result.PUSH:
            return PUSH_PAYOUT
        return 0

    def to_dict(self) -> dict:
        return {
            "game_id": self.game_id,
            "state": self.state.value,
            "player_hand": self.player_hand.to_dict(),
            "dealer_hand": self.dealer_hand.to_dict(),
            "result": self.result.value if self.result else None,
        }
