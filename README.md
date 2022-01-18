# MarchMadness22
My 2022 March Madness Model: Builds off of and hopefully improves on my 2021 model.

There are actually three key parts to this model:
1) A predictive model that returns the probability a team will win any given match-up
2) A monte-carlo simulation that uses the model from step 1 to simulate the outcome of the tournament
3) An optimization model that selects the best bracket based on the data produced from step 1

### Step 1: Predictive Model
The 2022 Model is still in development. The monte carlo and optimization portions of this system will be based on the
terrible 2021 model

### Step 2: Monte Carlo Simulation
This simulation takes as input two different data files:
1) The probabilities from step 1; Must be stored in a 2D matrix and each row/column must have the name of the team.
2) The team details file that lists the team name, seed and id number.

It is <i>Very Important</i> that these files are consistent with the input from 2021. This means a) The team names must
be consistent across files and b) the team ids should be presented in descending order from group A-D. Consult previous
year files if this is confusing.

### Step 3: Optimization
TBD - Seems hard


### TODO:
1) Improve the way data is exported to the simulation
2) create data to use for the optimization model
3) Build optimization model
4) Improve documentation
5) Build predictive model
6) Run final model