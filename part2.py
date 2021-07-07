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
prob2 = LpProblem('DietProblem', LpMinimize)

# continuous variable
food_vars = LpVariable.dicts("foods", foods, 0)

# binary variable of our chosen foods
chosen_vars = LpVariable.dicts("Chosen", foods, 0, 1, "Binary")

# set our problem to solve
prob2 += lpSum([cost[f] * food_vars[f] for f in foods]), "Total Cost"


# PART A constraint
for f in foods:
    prob2 += food_vars[f] <= 10000 * chosen_vars[f]
    prob2 += food_vars[f] >= .1 * chosen_vars[f]

# PART B constraint celery or broccoli, not both
prob2 += chosen_vars['Frozen Broccoli'] + chosen_vars['Celery, Raw'] <= 1

# PART C constraint one of the meats, ambiguous
prob2 += chosen_vars['Roasted Chicken'] + chosen_vars['Poached Eggs'] + \
         chosen_vars['Scrambled Eggs'] + chosen_vars['Frankfurter, Beef'] + \
         chosen_vars['Kielbasa,Prk'] + chosen_vars['Hamburger W/Toppings'] + \
         chosen_vars['Hotdog, Plain'] + chosen_vars['Pork'] + \
         chosen_vars['Bologna,Turkey'] + chosen_vars['Ham,Sliced,Extralean'] + \
         chosen_vars['White Tuna in Water'] + chosen_vars['Sardines in Oil'] \
         >= 3

# min max
for i in range(0, 11):
    prob2 += lpSum([t[i][j] * food_vars[j] for j in foods]) >= allmin[0][i+3], 'min' + nnames[i]
    prob2 += lpSum([t[i][j] * food_vars[j] for j in foods]) <= allmax[0][i+3], 'max' + nnames[i]


prob2.solve()

# print solutions
print('Solution:')
for var in prob2.variables():
    if var.varValue > 0:
        if str(var).find('Chosen'):
            print(str(var.varValue) + " units of " + str(var))

# cost of diet
print("Total Cost: $ %.2f" % value(prob2.objective))
