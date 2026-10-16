import random

from player import Player


class ComputerPlayer(Player):
    """A computer that follows one strategy."""

    # (name, description) of every strategy, in menu order.
    STRATEGIES = [
        ("Always Cooperate", "The computer always chooses C."),
        ("Always Defect", "The computer always chooses D."),
        ("Random", "The computer randomly chooses C or D."),
        ("Tit-for-Tat", "The computer cooperates initially, then copies the "
                        "opponent's previous decision."),
    ]

    def __init__(self, name, strategy):
        super().__init__(name)
        self.strategy = strategy  # one of the names in STRATEGIES

    def label(self):
        return f"{self.name} ({self.strategy})"

    def choose_move(self, opponent, hide_input):
        if self.strategy == "Always Cooperate":
            return "C"
        if self.strategy == "Always Defect":
            return "D"
        if self.strategy == "Random":
            return random.choice(["C", "D"])
        # Tit-for-Tat: cooperate in the first round, then copy the opponent's
        # move from the round before.
        if len(opponent.moves) == 0:
            return "C"
        return opponent.moves[-1]

    def strategy_name(self, opponent):
        return self.strategy
