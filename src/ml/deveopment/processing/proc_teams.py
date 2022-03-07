# ----------------------
# Teams
# ----------------------
# Description:
#     Joins human-readable Team Names to team_id

# Raw File:
#     MTeams.csv

# Transformations:
#     Drop columns
#     Rename Columns
#     save to csv

# Output File(s):
#     teams.csv
# -------------------------------

import pandas as pd

# import raw data
df = pd.read_csv("src/ml/raw_data/mens-march-mania-2022/MDataFiles_Stage1/MTeams.csv")

# drop columns
df = df.drop(['FirstD1Season', 'LastD1Season'], axis=1)

# rename columns
df = df.rename(columns={"TeamID": "team_id", "TeamName": "tean_name"})

# save to csv
df.to_csv("src/ml/deveopment/data/teams.csv")
