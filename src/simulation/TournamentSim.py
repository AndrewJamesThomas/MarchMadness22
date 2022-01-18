from src.simulation.Game import Game

class TournamentSim:
    def __init__(self):
        # Step 1: List out all games in tournament by Game ID
        # I feel like there must be an easier way of doing this. this is not dry code.
        self.all_games = {
            # Group A; Round 1
            "A11": Game("A11", "A21", 1),
            "A12": Game("A12", "A21", 1),
            "A13": Game("A13", "A22", 1),
            "A14": Game("A14", "A22", 1),
            "A15": Game("A15", "A23", 1),
            "A16": Game("A16", "A23", 1),
            "A17": Game("A17", "A24", 1),
            "A18": Game("A18", "A24", 1),

            # Group A; Round 2
            "A21": Game("A21", "A31", 2),
            "A22": Game("A22", "A31", 2),
            "A23": Game("A23", "A32", 2),
            "A24": Game("A24", "A32", 2),

            # Group A; Round 3
            "A31": Game("A31", "A41", 3),
            "A32": Game("A32", "A41", 3),

            # Group A; Round 4
            "A41": Game("A41", "E51", 4),

            # Group B; Round 1
            "B11": Game("B11", "B21", 1),
            "B12": Game("B12", "B21", 1),
            "B13": Game("B13", "B22", 1),
            "B14": Game("B14", "B22", 1),
            "B15": Game("B15", "B23", 1),
            "B16": Game("B16", "B23", 1),
            "B17": Game("B17", "B24", 1),
            "B18": Game("B18", "B24", 1),

            # Group B; Round 2
            "B21": Game("B21", "B31", 2),
            "B22": Game("B22", "B31", 2),
            "B23": Game("B23", "B32", 2),
            "B24": Game("B24", "B32", 2),

            # Group B; Round 3
            "B31": Game("B31", "B41", 3),
            "B32": Game("B32", "B41", 3),

            # Group B; Round 4
            "B41": Game("B41", "E51", 4),

            # Group C; Round 1
            "C11": Game("C11", "C21", 1),
            "C12": Game("C12", "C21", 1),
            "C13": Game("C13", "C22", 1),
            "C14": Game("C14", "C22", 1),
            "C15": Game("C15", "C23", 1),
            "C16": Game("C16", "C23", 1),
            "C17": Game("C17", "C24", 1),
            "C18": Game("C18", "C24", 1),

            # Group C; Round 2
            "C21": Game("C21", "C31", 2),
            "C22": Game("C22", "C31", 2),
            "C23": Game("C23", "C32", 2),
            "C24": Game("C24", "C32", 2),

            # Group C; Round 3
            "C31": Game("C31", "C41", 3),
            "C32": Game("C32", "C41", 3),

            # Group C; Round 4
            "C41": Game("C41", "E52", 4),

            # Group D; Round 1
            "D11": Game("D11", "D21", 1),
            "D12": Game("D12", "D21", 1),
            "D13": Game("D13", "D22", 1),
            "D14": Game("D14", "D22", 1),
            "D15": Game("D15", "D23", 1),
            "D16": Game("D16", "D23", 1),
            "D17": Game("D17", "D24", 1),
            "D18": Game("D18", "D24", 1),

            # Group D; Round 2
            "D21": Game("D21", "D31", 2),
            "D22": Game("D22", "D31", 2),
            "D23": Game("D23", "D32", 2),
            "D24": Game("D24", "D32", 2),

            # Group D; Round 3
            "D31": Game("D31", "D41", 3),
            "D32": Game("D32", "D41", 3),

            # Group D; Round 4
            "D41": Game("D41", "E52", 4),

            # Group #
            "E51": Game("E51", "E69", 5),
            "E52": Game("E52", "E69", 5),
            "E69": Game("E69", None, 6)
        }

    def _play_round(self, round_number, first_round):
        games_in_round = [i for i in self.all_games.keys() if i[1] == str(round_number)]
        if first_round:
            # Step 2: Load initial games
            for team1, game_id in zip(range(1, len(games_in_round)*2, 2), games_in_round):
                team2 = team1 + 1
                self.all_games[game_id].load_all_games(team1, team2)

        # Step 3: Simulate all games in current round
        for g in games_in_round:
            self.all_games[g].simulate_game()

# Step 4: Load winners into next round

    def _load_next_round(self, round_number):
        games_in_round = [i for i in self.all_games.keys() if i[1] == str(round_number)]
        for game_id in games_in_round:
            next_game = self.all_games[game_id].game["next_game_id"]
            game_winner = self.all_games[game_id].game["winner_id"]
            self.all_games[next_game].load_game(game_winner)

# Step 5: Repeat steps 3 & 4 until tournament is done
    def simulate_tournament(self):
        self._play_round(1, True)
        self._load_next_round(1)

        self._play_round(2, False)
        self._load_next_round(2)

        self._play_round(3, False)
        self._load_next_round(3)

        self._play_round(4, False)
        self._load_next_round(4)

        self._play_round(5, False)
        self._load_next_round(5)

        self._play_round(6, False)

# Step 6: Export results into 1 row of a dataframe/matrix
    def export_results(self):
        output = []
        for g in self.all_games.keys():
            winner = self.all_games[g].game["winner"]
            winner_id = self.all_games[g].game["winner_id"]
            output.append((g, winner, winner_id))
        return output


if __name__ == "__main__":
    # step 7: Repeat steps 1-7 10,000 times
    # TODO: Speed this up, probably using Numpy; or just run for a long time
    simulation = []
    N = 100
    for x in range(N):
        T = TournamentSim()
        T.simulate_tournament()
        res = T.export_results()
        simulation.append(res)

    winner = []
    for i in simulation:
        winner.append(i[62][1])

# TODO: Use this to optimize bracket
