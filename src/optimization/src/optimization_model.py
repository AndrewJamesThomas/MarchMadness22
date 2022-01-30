import pandas as pd
import numpy as np
from pyomo.environ import *

points = pd.read_csv("src/optimization/data/points_earned.csv")
winners = pd.read_csv("src/optimization/data/winning_teams.csv")
details = pd.read_csv("src/simulation/data/team_details.csv")
details.iloc[44, 0] = "Florida"

teams = details["team_name"]
games = winners.columns
sims = points.index

# initialize optimization model
model = ConcreteModel()

# establish DVs
model.dv = Var(teams, games, domain=Binary)

# establish objective functions
model.points = Objective(expr=sum([sum([points.loc[i, g] * model.dv[(winners.loc[i, g], g)] for g in games]) for i in sims]),
                         sense=maximize)
# set up constraints
# TODO: Fix this, all columns in the decision variable matrix should add to exactly one ie, 1-game-1-winner
#model.cons = ConstraintList()
#for g in games:
#    model.cons.add(expr=sum(model.dv[]) == 1)

# TODO: Add constraints that will enforce tournament rules

# Solver the problem
SolverFactory("glpk").solve(model)
# without constraints we would expect this to return all ones
model.display()

# TODO: export to excel and visualize results
