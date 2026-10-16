from prisoners_dilemma.players.computer_player import ComputerPlayer
from prisoners_dilemma.console import Console
from prisoners_dilemma.game import Game
from prisoners_dilemma.players.human_player import HumanPlayer
from prisoners_dilemma.payoff_matrix import PayoffMatrix
from prisoners_dilemma.tournament import Tournament


class PrisonersDilemmaApp:
    """The menus: number of rounds -> game mode -> strategies -> play."""

    MAX_ROUNDS = 10

    def __init__(self):
        self.console = Console()

    def run(self):
        self.show_intro()
        while True:
            rounds = self.choose_rounds()
            self.console.clear()
            if rounds == 0:
                if self.console.ask_yes_no("\nAre you sure you want to exit? (y/n): "):
                    self.console.clear()
                    break
                continue

            result = self.choose_mode_and_play(rounds)
            if result == "back":
                continue
            if result == "quit":
                self.console.clear()
                print("\nGame abandoned. Returning to the main menu.")
                continue

            if not self.console.ask_yes_no("\nPlay again? (y/n): "):
                self.console.clear()
                break
        print("Thanks for playing!")

    def show_intro(self):
        self.console.print_heading("PRISONER'S DILEMMA")
        print("Two prisoners independently decide, without knowing the other's choice:")
        print("  C - Cooperate: remain silent and cooperate with the other prisoner.")
        print("  D - Defect   : betray the other prisoner.")
        print("Higher scores represent better outcomes.\n")
        PayoffMatrix(self.console).show()

    def choose_rounds(self):
        """Main menu. Returns the number of rounds, or 0 to exit the game."""
        while True:
            choice = self.console.ask_menu("MAIN MENU - Select the number of rounds:",
                                           ["Single round", "n rounds"], "Exit game")
            if choice == 0:
                return 0
            if choice == 1:
                return 1
            rounds = self.console.ask_number(
                f"Enter the number of rounds n (1-{self.MAX_ROUNDS}), or 0 to go back: ",
                1, self.MAX_ROUNDS)
            if rounds != 0:
                return rounds
            # 0 = back, so show the main menu again.

    def choose_mode_and_play(self, rounds):
        """Returns "back" if the user went back to the main menu, "quit" if a
        player quit during the game, or "done" when the game finished."""
        if rounds == 1:
            rounds_text = "single round"
        else:
            rounds_text = f"{rounds} rounds"

        while True:
            mode = self.console.ask_menu(f"Select a game mode ({rounds_text}):",
                                         ["Player vs Player", "Player vs Computer",
                                          "Computer vs Computer", "Tournament"],
                                         "Back to number of rounds")
            if mode == 0:
                return "back"

            if mode == 4:
                result = Tournament(rounds, self.console).start()
                if result == "back":
                    continue  # the user went back from the tournament setup
                return result

            if mode == 1:
                players = self.create_player_vs_player()
            elif mode == 2:
                players = self.create_player_vs_computer(rounds)
            else:
                players = self.create_computer_vs_computer(rounds)
            if players is None:
                continue  # the user went back from a strategy menu

            player1, player2 = players
            game = Game(player1, player2, rounds, self.console)
            if not game.play():
                return "quit"
            game.show_results()
            return "done"

    def create_player_vs_player(self):
        print("\nPlayer vs Player: choices are hidden while typing, so the other "
              "player cannot see them.")
        return HumanPlayer("Player 1", self.console), HumanPlayer("Player 2", self.console)

    def create_player_vs_computer(self, rounds):
        """Returns the two players, or None if the user went back."""
        self.print_strategy_note(rounds)
        strategy = self.choose_strategy("Select the computer's strategy:", rounds,
                                        "Back to game mode")
        if strategy is None:
            return None
        computer = ComputerPlayer("Computer", strategy)
        print(f"\nYou are playing against {computer.label()}.")
        return HumanPlayer("Player", self.console), computer

    def create_computer_vs_computer(self, rounds):
        """Returns the two players, or None if the user went back."""
        self.print_strategy_note(rounds)
        while True:
            strategy1 = self.choose_strategy("Select the strategy for Computer 1:", rounds,
                                             "Back to game mode")
            if strategy1 is None:
                return None
            strategy2 = self.choose_strategy("Select the strategy for Computer 2:", rounds,
                                             "Back to Computer 1's strategy")
            if strategy2 is not None:
                break
            # The user went back from Computer 2, so ask for Computer 1 again.

        computer1 = ComputerPlayer("Computer 1", strategy1)
        computer2 = ComputerPlayer("Computer 2", strategy2)
        print(f"\nComputer vs Computer: {computer1.label()} vs {computer2.label()}")
        return computer1, computer2

    def print_strategy_note(self, rounds):
        if rounds < 2:
            print("\nNote: Strategy 4 (Tit-for-Tat) needs at least 2 rounds, "
                  "so it is not available in a single-round game.")

    def choose_strategy(self, title, rounds, back_text):
        """Show the strategy menu. Returns the strategy name, or None to go back."""
        names = []
        options = []
        for number, strategy in enumerate(ComputerPlayer.STRATEGIES, start=1):
            name, description = strategy
            # Tit-for-Tat copies the opponent's previous move, so it needs at
            # least 2 rounds.
            if name == "Tit-for-Tat" and rounds < 2:
                continue
            names.append(name)
            options.append(f"Strategy {number}: {name}. {description}")

        choice = self.console.ask_menu(title, options, back_text)
        if choice == 0:
            return None
        return names[choice - 1]
