import pandas as pd
from scipy.stats import uniform

from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import log_loss, roc_auc_score, accuracy_score

from joblib import dump

# ---- Load Raw Data
df = pd.read_csv("src/ml/deployment/data/postpro/model_training.csv")
testing = pd.read_csv("src/ml/deployment/data/postpro/model_testing.csv")

# ---- split training data into x and y
x = df.drop(["team1_win"], axis=1)
y = df["team1_win"]

# ---- Split into training/test
xtrain, xtest, ytrain, ytest = train_test_split(x, y, train_size=0.8, random_state=4206969)

# ---- Begin modeling process | 0.5388
# Simple Logistic
model1 = LogisticRegression()
model1.fit(xtrain, ytrain)
proba1 = model1.predict_proba(xtest)[:, 1]

model1_results = log_loss(ytest, proba1)

# Ridge | 0.5485
grid2 = {"C": uniform()}
model2 = LogisticRegression(penalty="l2", solver="liblinear")
srch2 = RandomizedSearchCV(model2, grid2, scoring="neg_log_loss", cv=10, random_state=4206969)
srch2.fit(xtrain, ytrain)
print(srch2.best_score_)

proba2 = srch2.predict_proba(xtest)[:, 1]
results2 = log_loss(ytest, proba2)

# Lasso | 0.5485
grid3 = {"C": uniform()}
model3 = LogisticRegression(penalty="l1", solver="liblinear")
srch3 = RandomizedSearchCV(model3, grid3, scoring="neg_log_loss", cv=10, random_state=4206969)
srch3.fit(xtrain, ytrain)
print(srch3.best_score_)

# Elastic Net |
grid4 = {"C": uniform(), "l1_ratio": uniform()}
model4 = LogisticRegression(penalty="elasticnet", solver="saga")
srch4 = RandomizedSearchCV(model4, grid4, scoring="neg_log_loss", cv=10, random_state=4206969)
srch4.fit(xtrain, ytrain)
print(srch4.best_score_)

proba4 = srch4.predict_proba(xtest)[:, 1]
log_loss(ytest, proba4)

# ---- Train winning model on all data, then master test
main_model = LogisticRegression(C=0.045130244267808206)
main_model.fit(x, y)
x_master_test = testing.drop(["team1_win"], axis=1)
y_master_test = testing["team1_win"]

master_test_proba = main_model.predict_proba(x_master_test)[:, 1]
log_loss(y_master_test, master_test_proba)
roc_auc_score(y_master_test, master_test_proba)
accuracy_score(y_master_test, master_test_proba>=.5)

# Master Results: Log Loss 0.57 | AUC 0.78 | Accuracy 71% | Good enough
dump(main_model, "src/ml/deployment/output/mmml22.joblib")
