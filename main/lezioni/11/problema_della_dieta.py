import pandas as pd
import openpyxl
import gurobipy as gp
from gurobipy import GRB
import numpy as np

xlsx = pd.ExcelFile("Diet.xlsx")

nutrients = pd.read_excel(xlsx, 'Nutrients')

foods = pd.read_excel(xlsx, 'Foods')

print("Nutrienti:")
print(nutrients)
print("\nCibi:")
print(foods)

# Per stampare una singola colonna:
# nutrients.Daily_Recommended_Intake

# Inizializza Modello
mod = gp.Model('Stigler Diet')

# Definisco le variabili del problema
num_of_foods = len(foods)
num_of_nutrients = len(nutrients)

# Le faccio partire da 1
xvar = mod.addVars(range(1, num_of_foods + 1), 'F')

# Prendo i costi
obj_cost = []
for f in range(num_of_foods):
    obj_cost.append(foods.Price_cents_1939[f])

# Definisco la FO
obj = mod.setObjective(xvar.prod(obj_cost), GRB.MINIMIZE)

# Definisco i vincoli
constraints_columns = ["Calories", "Protein_g", "Calcium_g", "Iron_mg", "Vitamin_A_IU",
                       "Thiamine_mg", "Riboflavin_mg", "Ascorbic_Acid_mg", "Niacin_mg"]
constraints = {}
i = 0
for constraint_column in constraints_columns:
    constraints[constraint_column] = []
    for f in range(num_of_foods):
        constraints[constraint_column].append(foods[constraint_column][f])
    mod.addConstr(
        (xvar.prod(constraints[constraint_column]) >= nutrients.Daily_Recommended_Intake[i]),
        constraint_column
    )
    i = i + 1

for constraint_column in constraints_columns:
    print(constraints[constraint_column])

# Risolvo la FO
mod.optimize()

if mod.status == GRB.OPTIMAL:
    print("\nValore ottimale: %g \n" % mod.objVal)

    X = mod.getAttr('x', xvar)
    for f in range(num_of_foods):
        if X[f] > 0:
            print('%s: %s + %g' % (foods.Commodity[f], foods.Unit[f], X[f]))
else:
    print("Soluzione ottima non trovata :(")
