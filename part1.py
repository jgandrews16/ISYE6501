import pandas as pd
from pulp import *

data = pd.read_excel('diet.xls', header=0)
data2 = data[0:64]

data2 = data2.values.tolist()
nnames = list(data.columns.values)

#automation of the column headers
t = []
for i in range(0, 11):
    t.append(dict([(x[0], float(x[i+3])) for x in data2]))

foods = [x[0] for x in data2]

# our min and max
allmin = data[65:66].values.tolist()
allmax = data[66:67].values.tolist()

cost = dict([(x[0], float(x[1])) for x in data2])


# define the problem
prob = LpProblem('DietProblem', LpMinimize)

# continuous variable
food_vars = LpVariable.dicts("foods", foods, 0)

# binary variable of our chosen foods
chosen_vars = LpVariable.dicts("Chosen", foods, 0, 1, "Binary")

# set our problem to solve
prob += lpSum([cost[f] * food_vars[f] for f in foods]), "Total Cost"

# min max
for i in range(0, 11):
    prob += lpSum([t[i][j] * food_vars[j] for j in foods]) >= allmin[0][i+3], 'min' + nnames[i]
    prob += lpSum([t[i][j] * food_vars[j] for j in foods]) <= allmax[0][i+3], 'max' + nnames[i]


prob.solve()

# print solutions
print('Solution:')
for var in prob.variables():
    if var.varValue > 0:
        if str(var).find('Chosen'):
            print(str(var.varValue) + " units of " + str(var))

# cost of diet
print("Total Cost: $ %.2f" % value(prob.objective))
