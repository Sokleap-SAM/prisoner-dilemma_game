class PayoffMatrix:
    """The points each player gets for every combination of choices.
    Higher points are better."""

    # (choice of player 1, choice of player 2) -> (points of player 1, points of player 2)
    POINTS = {
        ("C", "C"): (3, 3),
        ("C", "D"): (0, 5),
        ("D", "C"): (5, 0),
        ("D", "D"): (1, 1),
    }

    def __init__(self, console):
        self.console = console

    def get_points(self, move1, move2):
        return self.POINTS[(move1, move2)]

    def show(self, name1="Player A", name2="Player B", counts=None):
        """Print the matrix as a table.

        If counts is given, each cell also shows how many rounds ended that way
        and the points it earned, e.g. "(3, 3) x 2 = (6, 6)".
        """
        headers = [f"{name1} \\ {name2}", "Cooperate (C)", "Defect (D)"]
        rows = []
        for move1, row_title in [("C", "Cooperate (C)"), ("D", "Defect (D)")]:
            row = [row_title]
            for move2 in ["C", "D"]:
                points1, points2 = self.get_points(move1, move2)
                cell = f"({points1}, {points2})"
                if counts is not None:
                    times = counts[(move1, move2)]
                    cell += f" x {times} = ({points1 * times}, {points2 * times})"
                row.append(cell)
            rows.append(row)
        self.console.print_table(headers, rows)
