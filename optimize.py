import gurobipy as gp
import pandas as pd
import numpy as np

# PARAMETERS
# ---------------------------------
# amount of track you build (in miles)
trackAmt = 4000
# penalty for building new route (in miles)
penaltyAmt = 200  # can do 0 to void this constraint
# maximum amount of lines per city
perCity = 3 # can do 1000 to void this constraint
# ---------------------------------




# get first columnm of distances.csv as df
geoNames = pd.read_csv('combDistances.csv', usecols=[0]).to_numpy()

# read indata from distances.csv and tdemand.csv
dists = pd.read_csv('combDistances.csv', index_col=0)
pop2020 = dists['2020 census'].to_numpy()
# remove first two columns from dists
dists = dists.drop(dists.columns[[0]], axis=1)
tdemand = pd.read_csv('combTDemand.csv', index_col=0)
tdemand = tdemand.drop(tdemand.columns[[0]], axis=1)




# Create a new model
m = gp.Model()
# add binary variables xij
il = []
numcity = len(pop2020)
for i in range(0, numcity):
	for j in range(0, numcity):
		il.append((i,j))

x = m.addVars(il, vtype=gp.GRB.BINARY, name="x") # +str(i) + "," + str(j)
m.update()
# Set objective function
# 
m.setObjective(gp.quicksum(x[i,j]*tdemand.iloc[i,j] for i in range(0, numcity) for j in range(0, numcity)), gp.GRB.MAXIMIZE)

# total track length built + penalty for adding new train lines <= (total track built parameter)
# xij * dij + xij*penalty <= (total track built parameter) 
m.addConstr(gp.quicksum(x[i,j]*dists.iloc[i,j] + x[i,j]*penaltyAmt for i in range(0, numcity) for j in range(0, numcity)) <= trackAmt)

# xij + xji <= 1
for i in range(0, numcity):
	for j in range(0, numcity):
		m.addConstr(x[i,j] + x[j,i] <= 1)

# xij + xji <= (parameter for maximum number of lines per city)
for i in range(0,numcity):
	m.addConstr(gp.quicksum(x[i,j]+x[j,i] for j in range(0, numcity)) <= perCity)

m.update()

m.optimize()

# Print solution

# make a dataframe of stuff to print out
printDf = pd.DataFrame(columns=["City Pair" , "Travel Demand", "Distance between cities"])
if m.status == gp.GRB.Status.OPTIMAL:
	solution = m.getAttr('x', x)
	for i in range(0, numcity):
		for j in range(0, numcity):
			if solution[i,j] > 0:
				cityPair = str(geoNames[i][0]) +  " <-> " + str(geoNames[j][0])
				tdemandVar = tdemand.iloc[i,j]
				distIJ = dists.iloc[i,j]
				printDf.loc[len(printDf)] = [cityPair, tdemandVar, distIJ]

# sort dataframe by travel demand
printDf = printDf.sort_values(by="Travel Demand", ascending=False)

print(printDf)

print(printDf.to_latex(index=False))