import pandas as pd

# ---- import raw data
df = pd.read_csv("data/prepro/MRegularSeasonCompactResults.csv")

# ---- drop columns
df = df.drop(["WScore", "LScore", "WLoc", "NumOT"], axis=1)

# ---- split into winners and loosers dataframe
winners = df[["Season", "DayNum", "WTeamID", "LTeamID"]]
winners = winners.rename(columns={"WTeamID": "team1", "LTeamID": "team2"})
winners['win_ind'] = True

loosers = df[["Season", "DayNum", "WTeamID", "LTeamID"]]
loosers = loosers.rename(columns={"WTeamID": "team2", "LTeamID": "team1"})
loosers['win_ind'] = False

# ---- append back into single dataframe
df2 = winners.append(loosers)

# ---- rename
df2 = df2.rename(columns={"Season": "season", "DayNum": "day_num"})

# ---- save to csv
df2.to_csv("data/postpro/regular_season_games.csv", index=False)
