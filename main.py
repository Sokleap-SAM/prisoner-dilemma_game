"""Prisoner's Dilemma game.

Two prisoners each choose, without knowing what the other one chooses:
    C = Cooperate (stay silent)
    D = Defect    (betray the other prisoner)

Game modes:
    1. Player vs Player      - two people share the keyboard (choices are hidden)
    2. Player vs Computer    - you pick the computer's strategy
    3. Computer vs Computer  - you pick a strategy for each computer
    4. Tournament            - knockout tournament, every match is player vs player

Type 0 at any menu to go back. Type 0 during a game to quit it.

Application code lives in the prisoners_dilemma package.
See README.md for the project layout.

Run:  python main.py
"""

from prisoners_dilemma.app import PrisonersDilemmaApp

if __name__ == "__main__":
    try:
        PrisonersDilemmaApp().run()
    except (KeyboardInterrupt, EOFError):
        # Ctrl+C was pressed, or the input ended.
        print("\nGame ended. Goodbye!")
