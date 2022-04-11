import pandas as pd
from joblib import load

# ---- Import raw data and model
model = load("src/ml/deployment/output/mmml22.joblib")
df = pd.read_csv("src/ml/deployment/data/postpro/model_deployment.csv")
teams = pd.read_csv("src/ml/deployment/data/postpro/teams.csv").drop(['Unnamed: 0'], axis=1)
seeds = pd.read_csv("src/ml/deployment/data/prepro/MNCAATourneySeeds.csv")

# ---- narrow dataset to only relevant teams
seeds = seeds[seeds["Season"]==2022]

df = df[df["team_id"].isin(seeds["TeamID"])]

# ---- Cross join teams so every combination is present
df = df.assign(key=1)
df = df\
    .merge(df, on="key", suffixes=("_team1", "_team2"))\
    .drop(["key"], axis=1)

# ---- split data into a final output dataframe and a predictors dataframe
X = df[['dok_team1', 'mas_team1', 'mor_team1', 'pom_team1', 'sag_team1',
        'dok_team2', 'mas_team2', 'mor_team2', 'pom_team2', 'sag_team2']]

output = df[['team_id_team1', 'team_id_team2']]\
    .rename(columns={"team_id_team1": "team1",
                     "team_id_team2": "team2"})

# ---- Run predictions!!!!!
output["probability"] = model.predict_proba(X)[:, 1]

# ---- Format for Kaggle
# create dataframe
kaggle = output.copy()

# filter out redundant or unneeded records
kaggle["diff_teams"] = kaggle["team1"]!=kaggle["team2"]
kaggle["team1_lower"] = kaggle["team1"]<kaggle["team2"]
kaggle = kaggle[kaggle["diff_teams"] & kaggle["team1_lower"]]

# create concatenated field
kaggle["team1"] = kaggle["team1"].astype("str")
kaggle["team2"] = kaggle["team2"].astype("str")
kaggle["ID"] = "2022_" + kaggle["team1"] + "_" + kaggle["team2"]
kaggle = kaggle.rename(columns={"probability": "Pred"})
kaggle = kaggle[["ID", "Pred"]]

# save kaggle submission
kaggle.to_csv("src/ml/deployment/output/AndrewThomas-20220316-MNCAA2022KaggleSubmission.csv", index=False)

# ---- Format for Brackets
# join to human readable team names
sam = output\
    .merge(teams, left_on="team1", right_on="team_id", how="inner")\
    .merge(teams, left_on="team2", right_on="team_id", how="inner", suffixes=("_1", "_2"))\
    [["team_name_1", "team_name_2", "probability"]]\
    .rename(columns={"team_name_1": "team1", "team_name_2": "team2"})

# pivot from long to wide
sam = sam.pivot(index="team1", columns="team2", values="probability")

# save to csv
sam.to_csv("src/ml/deployment/output/game_predictions.csv")

