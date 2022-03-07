# ----------------------
# Regular Season Results
# ----------------------
# Description:
#     Lists every regular season game, their game number, the year and winning/losing team IDs

# Raw File:
#     MRegularSeasonCompactResults

# Transformations:
#     Add "win_ind" column
#     drop unneeded columns
#     subset to two different dataframes: only winners and only losers. Then append them together
# // this is probably the most controversial decision in this entire modelling processing //
#     Rename columns

# Output File(s):
#     regular_season_games.csv
# -------------------------------
import pandas as pd

df = pd.read_csv("src/ml/raw_data/mens-march-mania-2022/MDataFiles_Stage1/MRegularSeasonCompactResults.csv")

# drop columns
df = df.drop(["WScore", "LScore", "WLoc", "NumOT"], axis=1)

# split into winners and loosers dataframe
winners = df[["Season", "DayNum", "WTeamID"]]
winners = winners.rename(columns={"WTeamID": "team_id"})
winners['win_ind'] = True

loosers = df[["Season", "DayNum", "LTeamID"]]
loosers = loosers.rename(columns={"LTeamID": "team_id"})
loosers['win_ind'] = False

# append back into single dataframe
df2 = winners.append(loosers)

# rename
df2 = df2.rename(columns={"Season": "season", "DayNum": "day_num"})

# save to csv
df2.to_csv("src/ml/deveopment/data/regular_season_games.csv", index=False)
