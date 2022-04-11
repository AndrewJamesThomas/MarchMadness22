import pandas as pd

# ---- Import raw data
games = pd.read_csv("data/postpro/regular_season_games.csv")
rankings = pd.read_csv("data/postpro/team_rankings.csv")

# ---- merge dataframes together
df = games\
    .merge(rankings,
           left_on=["season", "day_num", "team1"],
           right_on=["season", "day_num", "team_id"],
           how="inner") \
    .merge(rankings,
           left_on=["season", "day_num", "team2"],
           right_on=["season", "day_num", "team_id"],
           suffixes=("_team1", "_team2"),
           how="inner")

# ---- Drop columns not used in modelling
df = df.drop(["season", "day_num", "team1", "team2", "team_id_team1", "team_id_team2"], axis=1)

# ---- Rename dependent variable for clarity
df = df.rename(columns={"win_ind": "team1_win"})

# ---- Save to CSV
df.to_csv("data/postpro/model_training.csv", index=False)

