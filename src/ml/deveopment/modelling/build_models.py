import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import log_loss, roc_auc_score, accuracy_score
from scipy.stats import uniform, poisson

games = pd.read_csv("src/ml/deveopment/data/regular_season_games.csv")
rankings = pd.read_csv("src/ml/deveopment/data/team_rankings.csv")
major_test = pd.read_csv("src/ml/deveopment/data/tourney_games.csv")

# join games to rankings (dependent and independent vars)
df = games.merge(rankings,
                 on=["season", "day_num", "team_id"],
                 how="inner")


# create train/test split
x = df[['dok', 'mas', 'mor', 'pom', 'sag']]
y = df["win_ind"]
x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.9, random_state=420)

# build model 1: Logistic Regression (Lasso) | Log Loss 0.65; Not nearly good enough
model1 = LogisticRegression()
grid = {"C": uniform(loc=0, scale=4)}
srch = RandomizedSearchCV(model1,
                          grid,
                          scoring="neg_log_loss",
                          cv=10,
                          random_state=420)
srch.fit(x_train, y_train)
print(f"Best Score: {srch.best_score_:.2f}")
print(srch.best_params_)

# build model 2: Elastic Net | Log Loss: 0.66
model2 = LogisticRegression(solver='saga', penalty="elasticnet", max_iter=500)
grid2 = {
    "C": uniform(loc=0, scale=4),
    "l1_ratio": uniform(loc=0, scale=4)
}
srch2 = RandomizedSearchCV(model2, grid2,
                           scoring="neg_log_loss",
                           cv=10,
                           random_state=420)
srch2.fit(x_train, y_train)
print(f"Best Score: {srch2.best_score_:.2f}")
print(srch2.best_params_)

# Model 3: Random Forrest | 0.65
model3 = RandomForestClassifier(random_state=420)
grid3 = {
 "n_estimators": np.arange(1, 21, 1),
 "criterion": ["gini", "entropy"],
 "max_depth": [7, 8, 9, 10, 11, 12],
 "min_samples_leaf": [100, 110, 120, 130, 140, 150, 160, 170, 180]
}

srch3 = RandomizedSearchCV(model3, grid3,
                           scoring="neg_log_loss",
                           cv=10,
                           random_state=420)

srch3.fit(x_train, y_train)
print(f"Best Score: {srch3.best_score_:.2f}")
print(srch3.best_params_)

# Model 4: KNearest Neighbor | Log Loss: 0.65
model4 = KNeighborsClassifier()
grid4 = {
    "n_neighbors": np.arange(90, 150, 1)
}
srch4 = RandomizedSearchCV(
    model4,
    grid4,
    scoring="neg_log_loss",
    cv=10,
    random_state=420
)

srch4.fit(x_train, y_train)
print(f"Best Score: {srch4.best_score_:.2f}")
print(srch4.best_params_)

# test
proba = srch.predict_proba(x_test)[:, 1]
log_loss(y_test, proba).round(2)
roc_auc_score(y_test, proba).round(2)
accuracy_score(y_test, proba>=0.5).round(2)
