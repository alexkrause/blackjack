from __future__ import annotations
from engine.store import GameStore
from ui.renderer import render_game, render_help, render_options

PLAYER_ID = "local"


def run(store: GameStore | None = None) -> None:
    if store is None:
        store = GameStore()

    print("Welcome to Blackjack! Type 'help' for commands.")
    print(f"Starting balance: ${store.get_balance(PLAYER_ID)}")

    current_game = None

    while True:
        if current_game is None or current_game.state.value == "complete":
            balance = store.get_balance(PLAYER_ID)
            if balance < 10:
                print("Insufficient balance to play. Game over.")
                break
            try:
                inp = input("\nPress Enter to deal a new hand (or 'quit' to exit): ").strip().lower()
            except EOFError:
                break
            if inp == "quit":
                break
            if inp and inp != "":
                if inp == "help":
                    render_help()
                elif inp == "balance":
                    print(f"  Balance: ${balance}")
                continue

            try:
                current_game = store.start_game(PLAYER_ID)
            except ValueError as e:
                print(f"Error: {e}")
                continue

            balance = store.get_balance(PLAYER_ID)
            render_game(current_game, balance)

            if current_game.state.value == "complete":
                continue

            render_options(current_game)

        else:
            try:
                inp = input("\n> ").strip().lower()
            except EOFError:
                break

            if not inp:
                continue

            if inp == "quit":
                break
            if inp == "help":
                render_help()
                render_options(current_game)
                continue
            if inp == "balance":
                print(f"  Balance: ${store.get_balance(PLAYER_ID)}")
                continue

            if inp not in ("hit", "stand", "double", "split"):
                print(f"Unknown command: '{inp}'. Type 'help' for options.")
                continue

            try:
                current_game = store.apply_action(current_game.game_id, inp)
            except (ValueError, NotImplementedError) as e:
                print(f"Error: {e}")
                continue

            balance = store.get_balance(PLAYER_ID)
            render_game(current_game, balance)

            if current_game.state.value == "playing":
                render_options(current_game)

    balance = store.get_balance(PLAYER_ID)
    print(f"\nThanks for playing! Final balance: ${balance}")
