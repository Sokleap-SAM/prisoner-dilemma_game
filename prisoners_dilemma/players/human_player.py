from prisoners_dilemma.players.player import Player


class HumanPlayer(Player):
    """A person who types C or D."""

    def __init__(self, name, console):
        super().__init__(name)
        self.console = console

    def choose_move(self, opponent, hide_input):
        prompt = f"{self.name}, choose C (Cooperate) or D (Defect)  [0 = back to main menu]: "
        while True:
            answer = self.console.read_text(prompt, hide_input).strip().upper()
            if answer == "C" or answer == "D":
                return answer
            if answer == "0":
                if self.console.ask_yes_no("  Quit this game and go back to the main menu? "
                                           "The game's progress will be lost. (y/n): "):
                    return None
                continue
            # Don't repeat what was typed, so a hidden choice stays hidden.
            print("  Invalid choice. Type C to cooperate, D to defect, "
                  "or 0 to go back to the main menu.")

    def strategy_name(self, opponent):
        """A person doesn't pick a strategy, so work it out from their moves."""
        if "D" not in self.moves:
            return "Always Cooperate"
        if "C" not in self.moves:
            return "Always Defect"
        if self.played_tit_for_tat(opponent):
            return "Tit-for-Tat"
        return "Mixed"

    def played_tit_for_tat(self, opponent):
        """True if the first move was C and every later move copied the
        opponent's move from the round before."""
        if self.moves[0] != "C":
            return False
        for i in range(1, len(self.moves)):
            if self.moves[i] != opponent.moves[i - 1]:
                return False
        return True
