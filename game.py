from human_player import HumanPlayer
from payoff_matrix import PayoffMatrix


class Game:
    """Plays all the rounds between two players and shows the results."""

    def __init__(self, player1, player2, rounds, console):
        self.player1 = player1
        self.player2 = player2
        self.rounds = rounds
        self.console = console
        self.payoff_matrix = PayoffMatrix(console)

    def has_human(self):
        return isinstance(self.player1, HumanPlayer) or isinstance(self.player2, HumanPlayer)

    def play(self):
        """Play every round. Returns False if a player quit the game early."""
        # When two people share the keyboard, hide their typing from each other.
        hide_input = isinstance(self.player1, HumanPlayer) and isinstance(self.player2, HumanPlayer)

        for round_number in range(1, self.rounds + 1):
            if self.has_human():
                print(f"\n--- Round {round_number} of {self.rounds} ---")

            # Both players choose before either move is saved, so neither
            # player can see the other's choice for this round.
            move1 = self.player1.choose_move(self.player2, hide_input)
            if move1 is None:
                return False
            move2 = self.player2.choose_move(self.player1, hide_input)
            if move2 is None:
                return False

            points1, points2 = self.payoff_matrix.get_points(move1, move2)
            self.player1.moves.append(move1)
            self.player1.points.append(points1)
            self.player2.moves.append(move2)
            self.player2.points.append(points2)

            if self.has_human():
                self.print_round(move1, move2, points1, points2)
        return True

    def winner(self):
        """The player with the higher total score, or None for a draw."""
        if self.player1.total_score() > self.player2.total_score():
            return self.player1
        if self.player2.total_score() > self.player1.total_score():
            return self.player2
        return None

    def print_round(self, move1, move2, points1, points2):
        p1, p2 = self.player1, self.player2
        print(f"{p1.name} chose {self.describe(move1)}, {p2.name} chose {self.describe(move2)}.")
        print(f"Payoff this round: {p1.name} {points1}, {p2.name} {points2}"
              f"   |   Total: {p1.name} {p1.total_score()}, {p2.name} {p2.total_score()}")

    def describe(self, move):
        if move == "C":
            return "C (Cooperate)"
        return "D (Defect)"

    def count_outcomes(self):
        """How many rounds ended each way, e.g. {("C", "D"): 2, ...}."""
        counts = {("C", "C"): 0, ("C", "D"): 0, ("D", "C"): 0, ("D", "D"): 0}
        for move1, move2 in zip(self.player1.moves, self.player2.moves):
            counts[(move1, move2)] += 1
        return counts

    def print_decision_table(self):
        p1, p2 = self.player1, self.player2
        headers = ["Round", f"{p1.name} choice", f"{p2.name} choice",
                   f"{p1.name} payoff", f"{p2.name} payoff"]
        rows = []
        for i in range(len(p1.moves)):
            rows.append([i + 1, p1.moves[i], p2.moves[i], p1.points[i], p2.points[i]])
        footer = ["Total", p1.count_moves(), p2.count_moves(),
                  p1.total_score(), p2.total_score()]
        self.console.print_table(headers, rows, footer)

    def show_results(self, title="GAME RESULT"):
        p1, p2 = self.player1, self.player2
        self.console.print_heading(title)
        print(f"Strategy used : {p1.name} = {p1.strategy_name(p2)}, "
              f"{p2.name} = {p2.strategy_name(p1)}")
        if self.has_human():
            print("                (a human's strategy is identified from the moves they made)")
        print(f"Rounds played : {len(p1.moves)}")

        print("\nTable of decisions:")
        self.print_decision_table()

        print("\nPayoff matrix score  [payoff (A, B) x times it happened = points earned (A, B)]:")
        self.payoff_matrix.show(p1.name, p2.name, self.count_outcomes())

        print(f"\n{p1.name}'s moves: {p1.count_moves()}")
        print(f"\n{p2.name}'s moves: {p2.count_moves()}")
        print(f"\nFinal score   : {p1.name} = {p1.total_score()}, {p2.name} = {p2.total_score()}")
        winner = self.winner()
        if winner is None:
            print("Result        : Draw")
        else:
            print(f"Winner        : {winner.label()}")
