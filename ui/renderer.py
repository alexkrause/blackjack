from __future__ import annotations
from engine.hand import Hand
from engine.game import Game


def render_hand(label: str, hand: Hand, hide_first: bool = False) -> None:
    cards = hand.cards
    if hide_first and cards:
        display = ["[?]"] + [str(c) for c in cards[1:]]
        visible_value = sum(c.value() for c in cards[1:])
        value_str = f"?+{visible_value}"
    else:
        display = [str(c) for c in cards]
        value_str = str(hand.value())
    print(f"  {label}: {' '.join(display)}  [{value_str}]")


def render_game(game: Game, balance: int) -> None:
    print()
    is_complete = game.state.value == "complete"
    render_hand("Dealer", game.dealer_hand, hide_first=not is_complete)
    render_hand("You   ", game.player_hand)
    print(f"  Balance: ${balance}")
    if is_complete and game.result:
        result_msg = {
            "blackjack": "Blackjack! You win $15.",
            "win": "You win!",
            "lose": "You lose.",
            "push": "Push — bet returned.",
        }.get(game.result.value, game.result.value)
        print(f"  Result: {result_msg}")


def render_help() -> None:
    print("""
Available commands:
  hit      - Request another card
  stand    - End your turn
  double   - Double your bet and take one card
  split    - Split a pair into two hands
  balance  - Show current balance
  quit     - Exit the game
  help     - Show this help message
""")


def render_options(game: Game) -> None:
    if game.state.value == "playing":
        options = ["hit", "stand", "double"]
        if game.player_hand.is_pair():
            options.append("split")
        print(f"  Options: {', '.join(options)}")
