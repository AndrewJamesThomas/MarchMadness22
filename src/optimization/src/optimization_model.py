import pandas as pd
from pyomo.environ import *

points = pd.read_csv("src/optimization/data/points_earned.csv")
winners = pd.read_csv("src/optimization/data/winning_teams.csv")

# initialize optimization model
model = ConcreteModel()

# establish DVs
