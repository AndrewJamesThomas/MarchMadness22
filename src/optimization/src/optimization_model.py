import pandas as pd
import numpy as np
from pyomo.environ import *

points = pd.read_csv("src/optimization/data/points_earned.csv")
winners = pd.read_csv("src/optimization/data/winning_teams.csv")
details = pd.read_csv("src/simulation/data/team_details.csv")

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
model.cons = ConstraintList()
for g in games:
    model.cons.add(sum([model.dv[t, g] for t in teams])==1)


# TODO: Add constraints that will enforce tournament rules

# Solver the problem
SolverFactory("glpk").solve(model)
# without constraints we would expect this to return all ones

pd.DataFrame([(model.dv[i](), i[0], i[1]) for i in model.dv])\
    .pivot(index=1, columns=2)[0]\
    .to_csv("src/dashboard/data/optimal_results.csv", index=True)

# export results distribution
pd.DataFrame([sum([points.loc[i, g] * model.dv[(winners.loc[i, g], g)]() for g in games]) for i in sims])\
    .to_csv("src/dashboard/data/optimal_distribution.csv", index=False)
