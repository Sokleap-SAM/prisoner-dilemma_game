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

One class per file:
    console.py                Console              - reads what the user types, prints tables
    payoff_matrix.py          PayoffMatrix         - the points for every combination of choices
    player.py                 Player               - base class: name, moves made, points earned
    human_player.py           HumanPlayer          - a person who types C or D
    computer_player.py        ComputerPlayer       - a computer that follows a strategy
    game.py                   Game                 - plays the rounds between two players
    tournament.py             Tournament           - knockout rounds until one champion is left
    prisoners_dilemma_app.py  PrisonersDilemmaApp  - the menus that tie everything together

Run:  python main.py
"""

from prisoners_dilemma_app import PrisonersDilemmaApp

if __name__ == "__main__":
    try:
        PrisonersDilemmaApp().run()
    except (KeyboardInterrupt, EOFError):
        # Ctrl+C was pressed, or the input ended.
        print("\nGame ended. Goodbye!")
