import random

from prisoners_dilemma.game import Game
from prisoners_dilemma.players.human_player import HumanPlayer


class Tournament:
    """A knockout tournament between people. Every match is Player vs Player.

    The players are paired up, each pair plays a game, and the winner goes on
    to the next round. This repeats until only the champion is left.
    """

    MAX_PLAYERS = 64
    MAX_NAME_LENGTH = 15

    def __init__(self, rounds, console):
        self.rounds = rounds  # rounds in every match
        self.console = console
        # One dictionary per match (and per bye), for example:
        # {"round": "Round 1", "match": 1, "player1": "Alice", "player2": "Bob",
        #  "strategy1": "Tit-for-Tat", "strategy2": "Mixed", "score1": 7, "score2": 2,
        #  "winner": "Alice", "decided_by": "Higher score"}
        self.records = []
        self.lost_in_round = {}  # player name -> number of the round they lost in
        self.final_round = 0     # number of the last round (the final)

    def start(self):
        """Run the whole tournament.

        Returns "back" if the user went back from the setup, "quit" if a player
        quit during a match, or "done" when the champion was found.
        """
        names = self.ask_setup()
        if names is None:
            return "back"
        self.show_players(names)
        champion = self.play_all_rounds(names)
        if champion is None:
            return "quit"
        self.show_summary(names, champion)
        return "done"

    # ----- Setup ------------------------------------------------------------

    def ask_setup(self):
        """Ask for the number of players and their names. Returns the names,
        or None if the user went back to the game mode menu."""
        while True:
            count = self.ask_player_count()
            if count == 0:
                return None
            names = self.ask_player_names(count)
            if names is not None:
                return names
            # The user went back from the first name, so ask the number again.

    def ask_player_count(self):
        """Returns an even number of players, or 0 to go back."""
        prompt = (f"\nEnter the number of players (even number, 2-{self.MAX_PLAYERS}), "
                  f"or 0 to go back to game mode: ")
        while True:
            count = self.console.ask_number(prompt, 2, self.MAX_PLAYERS)
            if count == 0 or count % 2 == 0:
                return count
            print(f"  {count} is an odd number. The tournament needs an even number "
                  f"of players so everyone has a pair.")

    def ask_player_names(self, count):
        """Ask for each player's name. Enter keeps the default name, and 0 goes
        back to the previous player. Returns the names, or None if the user went
        back from the first player."""
        print(f"\nEnter the names of the {count} players.")
        names = []
        while len(names) < count:
            number = len(names) + 1
            default = f"Player {number}"
            if number == 1:
                back_to = "number of players"
            else:
                back_to = f"player {number - 1}"
            name = input(f"Name of player {number} (Enter = '{default}', "
                         f"0 = back to {back_to}): ").strip()

            if name == "0":
                if len(names) == 0:
                    return None
                names.pop()  # forget the previous name so it is asked again
                continue
            if name == "":
                name = default
            if len(name) > self.MAX_NAME_LENGTH:
                print(f"  That name is too long. Please use at most "
                      f"{self.MAX_NAME_LENGTH} characters.")
            elif self.is_name_taken(name, names):
                print(f"  '{name}' is already taken. Please choose a different name.")
            else:
                names.append(name)
        return names

    def is_name_taken(self, name, names):
        """Compare names without caring about upper or lower case."""
        for taken in names:
            if taken.lower() == name.lower():
                return True
        return False

    def show_players(self, names):
        self.console.print_heading("TOURNAMENT PLAYERS")
        rows = []
        for number, name in enumerate(names, start=1):
            rows.append([number, name])
        self.console.print_table(["No.", "Player"], rows)
        print(f"Every match is Player vs Player and lasts {self.rounds} round(s); choices are hidden")
        print("while typing. The higher total score wins the match, a draw is settled by a")
        print("coin toss, and winners advance until one champion remains.")

    # ----- Playing ----------------------------------------------------------

    def play_all_rounds(self, names):
        """Play knockout rounds until one player is left. Returns the
        champion's name, or None if a player quit."""
        remaining = names[:]       # a copy, so the list of names is not changed
        random.shuffle(remaining)  # random draw for the first round
        round_number = 0
        while len(remaining) > 1:
            round_number += 1
            remaining = self.play_round(remaining, round_number)
            if remaining is None:
                return None
        self.final_round = round_number
        return remaining[0]

    def play_round(self, players, round_number):
        """Pair the players up and play every match of one round. Returns the
        names of the players who go through, or None if a player quit."""
        if len(players) == 2:
            round_title = "Final"
        else:
            round_title = f"Round {round_number}"
        self.console.print_heading(f"TOURNAMENT {round_title.upper()}  ({len(players)} players)")

        # With an odd number of players, one random player goes through to the
        # next round without playing. This is called a "bye".
        players = players[:]
        bye_player = None
        if len(players) % 2 == 1:
            bye_player = random.choice(players)
            players.remove(bye_player)

        # Pair the players in order: 1st vs 2nd, 3rd vs 4th, and so on.
        pairs = []
        for i in range(0, len(players), 2):
            pairs.append((players[i], players[i + 1]))

        for match_number, (name1, name2) in enumerate(pairs, start=1):
            print(f"  Match {match_number}: {name1}  vs  {name2}")
        if bye_player is not None:
            print(f"  Bye    : {bye_player} advances automatically (odd number of players)")

        winners = []
        for match_number, (name1, name2) in enumerate(pairs, start=1):
            winner = self.play_match(round_number, round_title, match_number, name1, name2)
            if winner is None:
                return None
            winners.append(winner)

        if bye_player is not None:
            winners.append(bye_player)
            self.records.append({"round": round_title, "player1": bye_player,
                                 "winner": bye_player, "decided_by": "Bye"})

        print(f"\n{round_title} summary:")
        self.print_match_table(round_title)
        if len(winners) > 1:
            print("Advancing to the next round: " + ", ".join(winners))
        return winners

    def play_match(self, round_number, round_title, match_number, name1, name2):
        """Play one match. Returns the winner's name, or None if a player quit."""
        title = f"{round_title} - Match {match_number}: {name1} vs {name2}"
        self.console.print_heading(title, "-")

        # New player objects for every match, so their moves and points start empty.
        player1 = HumanPlayer(name1, self.console)
        player2 = HumanPlayer(name2, self.console)
        game = Game(player1, player2, self.rounds, self.console)
        if not game.play():
            return None
        game.show_results(f"RESULT - {title}")

        winner = game.winner()
        if winner is None:
            winner = random.choice([player1, player2])
            decided_by = "Coin toss (draw)"
            print(f"Tie-break     : coin toss won by {winner.name}")
        else:
            decided_by = "Higher score"
        print(f"Advances      : {winner.name}")

        if winner is player1:
            loser = player2
        else:
            loser = player1
        self.lost_in_round[loser.name] = round_number

        self.records.append({
            "round": round_title,
            "match": match_number,
            "player1": name1,
            "player2": name2,
            "strategy1": player1.strategy_name(player2),
            "strategy2": player2.strategy_name(player1),
            "score1": player1.total_score(),
            "score2": player2.total_score(),
            "winner": winner.name,
            "decided_by": decided_by,
        })
        return winner.name

    # ----- Results ----------------------------------------------------------

    def print_match_table(self, round_title=None):
        """Print the matches of one round, or of every round if no round is given."""
        headers = ["Round", "Match", "Player A (strategy used)", "Player B (strategy used)",
                   "Score", "Winner", "Decided by"]
        rows = []
        for record in self.records:
            if round_title is not None and record["round"] != round_title:
                continue
            if record["decided_by"] == "Bye":
                rows.append([record["round"], "-", record["player1"], "(bye)", "-",
                             record["winner"], "Bye"])
            else:
                rows.append([record["round"], record["match"],
                             f"{record['player1']} ({record['strategy1']})",
                             f"{record['player2']} ({record['strategy2']})",
                             f"{record['score1']} - {record['score2']}",
                             record["winner"], record["decided_by"]])
        self.console.print_table(headers, rows)

    def show_summary(self, names, champion):
        self.console.print_heading("TOURNAMENT SUMMARY")
        print("All matches:")
        self.print_match_table()

        print("\nPlayer standings:")
        self.print_standings(names, champion)

        print("\nStrategy performance (one entry per player per match):")
        self.print_strategy_table()
        print("Strategy used is identified from each player's moves in a match "
              "(Mixed = no fixed pattern).")

        self.console.print_heading(f"CHAMPION: {champion}", "*")

    def print_standings(self, names, champion):
        # Add up each player's matches, wins, points and strategies used.
        stats = {}
        for name in names:
            stats[name] = {"matches": 0, "wins": 0, "points": 0, "strategies": []}
        for record in self.records:
            if record["decided_by"] == "Bye":
                continue
            self.add_player_result(stats[record["player1"]], record["score1"], record["strategy1"])
            self.add_player_result(stats[record["player2"]], record["score2"], record["strategy2"])
            stats[record["winner"]]["wins"] += 1

        # Players who lasted more rounds rank higher. If equal, more points rank higher.
        ranking = sorted(names, key=lambda name: (self.rounds_lasted(name), stats[name]["points"]),
                         reverse=True)

        rows = []
        for rank, name in enumerate(ranking, start=1):
            player_stats = stats[name]
            rows.append([rank, name, player_stats["matches"], player_stats["wins"],
                         player_stats["points"], " / ".join(player_stats["strategies"]),
                         self.result_text(name, champion)])
        self.console.print_table(["Rank", "Player", "Matches", "Wins", "Points",
                                  "Strategy used", "Result"], rows)

    def add_player_result(self, player_stats, points, strategy):
        player_stats["matches"] += 1
        player_stats["points"] += points
        if strategy not in player_stats["strategies"]:
            player_stats["strategies"].append(strategy)

    def rounds_lasted(self, name):
        """The round a player lost in. The champion never lost, so they count
        as lasting one round more than the final."""
        if name in self.lost_in_round:
            return self.lost_in_round[name]
        return self.final_round + 1

    def result_text(self, name, champion):
        if name == champion:
            return "Champion"
        if self.lost_in_round[name] == self.final_round:
            return "Runner-up"
        return f"Lost in round {self.lost_in_round[name]}"

    def print_strategy_table(self):
        # For each strategy: how many times it was used, how often it won,
        # and the points it earned.
        totals = {}
        for record in self.records:
            if record["decided_by"] == "Bye":
                continue
            self.add_strategy_result(totals, record["strategy1"], record["score1"],
                                     record["player1"] == record["winner"])
            self.add_strategy_result(totals, record["strategy2"], record["score2"],
                                     record["player2"] == record["winner"])

        rows = []
        for strategy, strategy_totals in totals.items():
            rounds_played = strategy_totals["times"] * self.rounds
            rows.append([strategy, strategy_totals["times"], strategy_totals["wins"],
                         strategy_totals["points"],
                         f"{strategy_totals['points'] / rounds_played:.2f}"])
        rows.sort(key=lambda row: row[2], reverse=True)  # most wins first
        self.console.print_table(["Strategy used", "Times used", "Wins", "Points",
                                  "Avg points per round"], rows)

    def add_strategy_result(self, totals, strategy, points, won):
        if strategy not in totals:
            totals[strategy] = {"times": 0, "wins": 0, "points": 0}
        totals[strategy]["times"] += 1
        totals[strategy]["points"] += points
        if won:
            totals[strategy]["wins"] += 1
