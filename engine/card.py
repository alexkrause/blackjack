from __future__ import annotations
import random
from dataclasses import dataclass, field


SUITS = ("S", "H", "D", "C")
RANKS = ("A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K")


@dataclass
class Card:
    rank: str
    suit: str
    face_up: bool = True

    def value(self) -> int:
        if self.rank in ("J", "Q", "K"):
            return 10
        if self.rank == "A":
            return 11
        return int(self.rank)

    def to_dict(self) -> dict:
        if not self.face_up:
            return {"rank": "?", "suit": "?", "face_up": False}
        return {"rank": self.rank, "suit": self.suit, "face_up": True}

    def __str__(self) -> str:
        if not self.face_up:
            return "[?]"
        return f"{self.rank}{self.suit}"


class Deck:
    def __init__(self, num_decks: int = 6):
        self._cards: list[Card] = [
            Card(rank, suit)
            for _ in range(num_decks)
            for suit in SUITS
            for rank in RANKS
        ]
        random.shuffle(self._cards)

    def deal(self) -> Card:
        if not self._cards:
            raise RuntimeError("Deck is empty")
        return self._cards.pop()
