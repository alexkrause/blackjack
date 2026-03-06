from __future__ import annotations
from dataclasses import dataclass, field
from engine.card import Card


@dataclass
class Hand:
    cards: list[Card] = field(default_factory=list)

    def add(self, card: Card) -> None:
        self.cards.append(card)

    def value(self) -> int:
        total = sum(c.value() for c in self.cards if c.face_up)
        aces = sum(1 for c in self.cards if c.rank == "A" and c.face_up)
        while total > 21 and aces:
            total -= 10
            aces -= 1
        return total

    def is_blackjack(self) -> bool:
        return len(self.cards) == 2 and self.value() == 21

    def is_bust(self) -> bool:
        return self.value() > 21

    def is_pair(self) -> bool:
        return len(self.cards) == 2 and self.cards[0].rank == self.cards[1].rank

    def reveal_all(self) -> None:
        for card in self.cards:
            card.face_up = True

    def to_dict(self) -> list[dict]:
        return [c.to_dict() for c in self.cards]
