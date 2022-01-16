import pandas as pd
import numpy as np


class Tournament:
    """
    Load external data that will be used in the tournament. This includes predictions, team names, etc.
    """
    def __init__(self,
                 team_details_path="src/simulation/data/team_details.csv",
                 game_predictions="assets/PreviousYear/game_predictions.csv"):
        self.team_details = pd.read_csv(team_details_path)
        self.predictions = pd.read_csv(game_predictions).set_index("team_1")
        self.points_lookup = {1: 2, 2: 3, 3: 5, 4: 8, 5: 13, 6: 21}


class Game(Tournament):
    def __init__(self, current_game_id, next_game, tournament_round):
        """
        Initialize game by entering game id, next game id and tournament round

        :param current_game_id: The current ID for that game
        :param next_game: The Game ID that the teams will play in next
        :param tournament_round: The tournament round for this game
        """
        # init super class
        super().__init__()

        self.game = {
            "game_id": current_game_id,
            "next_game_id": next_game,
            "round": tournament_round,
            "team1": {"team_id": None,
                      "team_name": None,
                      "seed": None,
                      "last_game": None},
            "team2": {"team_id": None,
                      "team_name": None,
                      "seed": None,
                      "last_game": None},
            "played": False,
            "winner": None,
            "team1_probability": -1,
            "points_earned": self.points_lookup[tournament_round]
        }

        self.team1_loaded = False

    def __str__(self):
        line1 = f"Game ID: {self.game['game_id']}; Round: {self.game['round']}"
        line2 = f"{self.game['team1']['team_name']} ({self.game['team1']['seed']}) Vs. " \
                f"{self.game['team2']['team_name']} ({self.game['team2']['seed']})"
        line3 = f"Probability that {self.game['team1']['team_name']} wins: {self.game['team1_probability']:.2f}"

        return f"{line1}\n{line2}\n{line3}"

# TODO: change load game to load games 1-at-a-time
    def load_game(self, team_id):
        """
        Adds the teams to the game and updates their details. Note, use the team ID NUMBERS, not names
        :param team_id: Team ID for either the first or second team
        :return: None
        """
        if self.team1_loaded is False:
            self.game['team1']['team_id'] = team_id
            self.game['team1']['seed'] = self.team_details[self.team_details["team_id"] == team_id]["seed"].values[0]
            self.game['team1']['team_name'] = self.team_details[self.team_details["team_id"] == team_id]["team_name"].values[0]
            self.team1_loaded = True
        else:
            self.game['team2']['team_id'] = team_id
            self.game['team2']['seed'] = self.team_details[self.team_details["team_id"] == team_id]["seed"].values[0]
            self.game['team2']['team_name'] = self.team_details[self.team_details["team_id"] == team_id]["team_name"].values[0]

            self.game['team1_probability'] = self.predictions\
                .loc[self.game['team1']['team_name'],
                     self.game['team2']['team_name']]

    def simulate_game(self, display_results=False):
        """
        Simulate the game and returns a winner. Simulation is based on the predicted probability
        and a randomly generated number. Displays the results of the game when done if desired
        :param display_results: set to True to print results (bool)
        :return: None
        """
        self.game["points_earned"] = self.points_lookup[self.game["round"]]
        self.game["played"] = True
        if np.random.rand() <= self.game["team1_probability"]:
            self.game["winner"] = self.game['team1']['team_name']
            if self.game['team1']['seed'] > self.game['team2']['seed']:
                self.game["points_earned"] += (self.game['team1']['seed'] - self.game['team2']['seed'])
        else:
            self.game["winner"] = self.game['team2']['team_name']
            if self.game['team2']['seed'] > self.game['team1']['seed']:
                self.game["points_earned"] += (self.game['team2']['seed'] - self.game['team1']['seed'])
        if display_results:
            self.show_game_result()

    def show_game_result(self):
        """
        Prints the results of the game
        :return: None
        """
        if self.game["played"]:
            print(f"Game Winner: {self.game['winner']}\nPoints Scored: {self.game['points_earned']}")
        else:
            print("Game not yet played. Play game first then proceed")


if __name__ == "__main__":
    game = Game(1, 2, 1)
    game.load_game(1)
    game.load_game(2)
    game.simulate_game(True)

# TODO: Write tournement simulation; create dictionary of all game ids and assign a game object as the value

# Step 1: List out all games in tournament by Game ID
# Step 2: Load initial games

# I feel like there must be an easier way of doing this. this is not dry code.
all_games = {
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
# Step 3: Simulate all games in current round
# Step 4: Load winners into next round
# Step 5: Repeat steps 3 & 4 until tournament is done
# Step 6: Export results into 1 row of a dataframe/matrix
# step 7: Repeat steps 1-7 10,000 times
