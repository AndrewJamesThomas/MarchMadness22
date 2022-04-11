import pandas as pd

# ---- import raw data
df = pd.read_csv("data/prepro/MTeams.csv")

# ---- drop columns
df = df.drop(['FirstD1Season', 'LastD1Season'], axis=1)

# ---- rename columns
df = df.rename(columns={"TeamID": "team_id", "TeamName": "team_name"})

# ---- save to csv
df.to_csv("data/postpro/teams.csv")
