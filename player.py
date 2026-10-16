class Player:
    """Base class for a player. Remembers the player's moves and points."""

    def __init__(self, name):
        self.name = name
        self.moves = []   # the choice made in each round, e.g. ["C", "D", "C"]
        self.points = []  # the points earned in each round, e.g. [3, 0, 5]

    def total_score(self):
        return sum(self.points)

    def count_moves(self):
        """Text like '2 C / 1 D'."""
        return f"{self.moves.count('C')} C / {self.moves.count('D')} D"

    def label(self):
        """How the player is named when they win."""
        return self.name

    # HumanPlayer and ComputerPlayer each have their own version of the two
    # methods below.

    def choose_move(self, opponent, hide_input):
        """Return "C" or "D" for this round, or None if the player quits."""
        raise NotImplementedError

    def strategy_name(self, opponent):
        """Return the name of the strategy this player used."""
        raise NotImplementedError
