import pandas as pd

# ---- import raw data
df = pd.read_csv("data/prepro/MMasseyOrdinals_thruDay128.csv")

# ---- convert from long to wide
df = df.pivot(index=["Season", "RankingDayNum", "TeamID"],
              columns="SystemName",
              values="OrdinalRank")

# ---- handle null values
df = df\
    .reset_index()\
    [["Season", "RankingDayNum", "TeamID", "DOK", "MAS", "MOR", "POM", "SAG"]]\
    .query("Season>=2016")

# ---- rename columns
df.columns = ['season', "day_num", "team_id", "dok", "mas", "mor", "pom", "sag"]

# ---- save to csv
df.to_csv("data/postpro/team_rankings.csv",
          index=False)
