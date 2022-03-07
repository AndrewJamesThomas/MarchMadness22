# --------
# rankings
# --------
# Description:
#    Includes third-party rankings of each team.
#    Very useful but has some limitations:
#        a) uses someone else's input, not my own
#        b) Ordinal ranks but does nothing to indicate magnitude
#    None the less, this can be very useful and building a basic model

# Raw File:
#    MMasseyOrdinals.csv

# Transformations:
#    Transform from long to wide
#    handle NULL values (probably row-wise deletion)
#    Rename columns
#    Save to CSV

# Output File(s):
#    team_rankings.csv
#######################

import pandas as pd

# import raw data
df = pd.read_csv("src/ml/raw_data/mens-march-mania-2022/MDataFiles_Stage1/MMasseyOrdinals.csv")

# convert from long to wide
df = df.pivot(index=["Season", "RankingDayNum", "TeamID"],
              columns="SystemName",
              values="OrdinalRank")

# handle null values
df = df\
    .reset_index()\
    [["Season", "RankingDayNum", "TeamID", "DOK", "MAS", "MOR", "POM", "SAG"]]\
    .query("Season>=2016")

# rename columns
df.columns = ['season', "day_num", "team_id", "dok", "mas", "mor", "pom", "sag"]

# save to csv
df.to_csv("src/ml/deveopment/data/team_rankings.csv",
          index=False)
