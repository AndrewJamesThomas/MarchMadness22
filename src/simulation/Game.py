import pandas as pd
import numpy as np


class Tournament:
    '''
    Load external data that will be used in the tournament. This includes predictions, team names, etc.
    '''
    def __init__(self,
                 team_details_path="src/simulation/data/team_details.csv",
                 game_predictions="assets/PreviousYear/game_predictions.csv"):
        self.team_details = pd.read_csv(team_details_path)
        self.predictions = pd.read_csv(game_predictions).set_index("team_1")
        self.points_lookup = {1: 2, 2: 3, 3: 5, 4: 8, 5: 13, 6: 21}


class Game(Tournament):
    '''
    Sets up and simulates a game
    '''
    def __init__(self, current_game_id, last_game, next_game, tournament_round):
        '''

        :param current_game_id: The current ID for that game
        :param last_game: The Game ID for the last game both teams played in
        :param next_game: The Game ID that the teams will play in next
        :param tournament_round: The tournement round for this game
        '''
        # init super class
        super().__init__()

        # Game information; loaded on init
        self.game_id = current_game_id
        self.last_game = last_game
        self.next_game = next_game
        self.round = tournament_round

        # Team information; loaded by "load_game" method
        self.teams = [None, None]
        self.team_names = [None, None]
        self.seeds = [None, None]
        self.team1_proba = None

        # Game outcomes; loaded with "play_game" method
        self.played = False
        self.winner = None
        self.points_earned = self.points_lookup[self.round]

    def __str__(self):
        line1 = f"Game ID: {self.game_id}; Round: {self.round}"
        line2 = f"{self.team_names[0]} ({self.seeds[0]}) Vs. {self.team_names[1]} ({self.seeds[1]})"
        line3 = f"Probability that {self.team_names[0]} wins: {self.team1_proba:.2f}"

        return f"{line1}\n{line2}\n{line3}"

    def load_game(self, team1, team2):
        '''
        Adds the teams to the game and updates their details. Note, use the team ID NUMBERS, not names
        :param team1: Team ID for the first team
        :param team2: Team ID for the second team
        :return: None
        '''
        self.teams[0] = team1
        self.teams[1] = team2

        self.seeds[0] = self.team_details[self.team_details["team_id"] == team1]["seed"].values[0]
        self.seeds[1] = self.team_details[self.team_details["team_id"] == team2]["seed"].values[0]

        self.team_names[0] = self.team_details[self.team_details["team_id"] == team1]["team_name"].values[0]
        self.team_names[1] = self.team_details[self.team_details["team_id"] == team2]["team_name"].values[0]

        self.team1_proba = self.predictions.loc[self.team_names[0], self.team_names[1]]

    def simulate_game(self, display_results=False):
        '''
        Simulate the game and returns a winner. Simulation is based on the predicted probaiblity
        and a randomly generated number. Displays the results of the game when done if desired
        :param display_results: set to True to print results (bool)
        :return: None
        '''
        self.played = True
        if np.random.rand() <= self.team1_proba:
            self.winner = self.teams[0]
            if self.seeds[0] > self.seeds[1]:
                self.points_earned += (self.seeds[0] - self.seeds[1])
        else:
            self.winner = self.teams[1]
            if self.seeds[1] > self.seeds[0]:
                self.points_earned += (self.seeds[1] - self.seeds[0])
        if display_results:
            self.show_game_result()

    def show_game_result(self):
        '''
        Prints the results of the game
        :return: None
        '''
        if self.played:
            winning_team = self.team_details[self.team_details["team_id"] == self.winner]["team_name"].values[0]
            print(f"Game Winner: {winning_team}\nPoints Scored: {self.points_earned}")
        else:
            print("Game not yet played. Play game first then proceed")


if __name__ == "__main__":
    # do stuff

    game1 = Game(1, 2, 3, 4)
    game1.load_game(1, 2)
    game1.simulate_game()
