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

    def __str__(self):
        line1 = f"Game ID: {self.game['game_id']}; Round: {self.game['round']}"
        line2 = f"{self.game['team1']['team_name']} ({self.game['team1']['seed']}) Vs. " \
                f"{self.game['team2']['team_name']} ({self.game['team2']['seed']})"
        line3 = f"Probability that {self.game['team1']['team_name']} wins: {self.game['team1_probability']:.2f}"

        return f"{line1}\n{line2}\n{line3}"

    def load_game(self, team1_id, team2_id):
        """
        Adds the teams to the game and updates their details. Note, use the team ID NUMBERS, not names
        :param team1_id: Team ID for the first team
        :param team2_id: Team ID for the second team
        :return: None
        """
        self.game['team1']['team_id'] = team1_id
        self.game['team2']['team_id'] = team2_id

        self.game['team1']['seed'] = self.team_details[self.team_details["team_id"] == team1_id]["seed"].values[0]
        self.game['team2']['seed'] = self.team_details[self.team_details["team_id"] == team2_id]["seed"].values[0]

        self.game['team1']['team_name'] = self.team_details[self.team_details["team_id"] == team1_id]["team_name"].values[0]
        self.game['team2']['team_name'] = self.team_details[self.team_details["team_id"] == team2_id]["team_name"].values[0]

        self.game['team1_probability'] = self.predictions.loc[self.game['team1']['team_name'], self.game['team2']['team_name']]

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
    game.load_game(1, 2)

# TODO: Write tournement simulation; create dictionary of all game ids and assign a game object as the value
# ie:
'''
    {
        round1 {
            game1: Game(...),
            game2: Game(...),
            ...
            round2 {
            game12: Game(...),
            ...
                    }
                }
    }
'''
# Then find a way to loop through that tournement, execute the games, return the results, and repeat
