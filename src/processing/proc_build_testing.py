import pandas as pd

# ---- Import raw data
games = pd.read_csv("data/postpro/tourney_games.csv")
rankings = pd.read_csv("data/postpro/team_rankings.csv")

# ---- Pull last ranking for each team in each season
final_rankings = rankings\
    .groupby(["season", "team_id"])\
    .max()\
    ["day_num"]\
    .reset_index()\
    .merge(rankings, on=["season", "team_id", "day_num"], how="inner")

# ---- join rankings to games
testing = games\
    .merge(final_rankings,
           left_on=["season", "team1"],
           right_on=["season", "team_id"],
           how="inner")\
    .merge(final_rankings,
           left_on=["season", "team2"],
           right_on=["season", "team_id"],
           how="inner",
           suffixes=("_team1", "_team2"))\
    .drop(["season", "day_num", "day_num_x", "day_num_y",
           "team1", "team2", "team_id_team1", "team_id_team2"], axis=1)\
    .rename(columns={"win_ind": "team1_win"})

# ---- Save testing data
testing.to_csv("data/postpro/model_testing.csv", index=False)

# ---- Extract 2022 final rankings data for each team
current_rankings = final_rankings\
    [final_rankings["season"]==2022]\
    .drop(["day_num", "season"], axis=1)

# ---- Save current rankings
current_rankings.to_csv("data/postpro/model_deployment.csv", index=False)
