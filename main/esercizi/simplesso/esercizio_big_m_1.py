import gurobipy as gp
from gurobipy import GRB

import numpy as np

# Inizializzo il modello
mod = gp.Model('Farmer')

# Creo variabili di decisione
prod = range(2)  # equivale ad aggiungerne una per volta con mod.addVar(name='x1')
xvar = mod.addVars(prod, name='X')  # x0, x1
res = range(4)

# Coefficienti della FO
objcoeff = [1, 1]
# Definisco FO
obj = mod.setObjective(xvar.prod(objcoeff), GRB.MAXIMIZE)

# Definisco tassi assorbimento
tassi_assorbimento = [[1, 0], [0, 1], [2, 5], [2, 1]]
signs = ['lte', 'lte', 'gte', 'gte']
# Definisco capacità
cap = [6, 4, 10, 4]

# Aggiungo i vincoli alla funzione obiettivo
constraints = []
for i in res:
    constraints.append(
        mod.addConstr(
            (xvar.prod(tassi_assorbimento[i]) <= cap[i]) if signs[i] == 'lte' else (xvar.prod(tassi_assorbimento[i]) >= cap[i]),
            'constraints'
        )
    )

# Risoluzione
mod.optimize()

# Prelevo soluzione e stampo
if mod.status == GRB.OPTIMAL:
    print("\nSoluzione ottima trovata: %g\n" % mod.objVal)

    X = mod.getAttr('x', xvar)
    for i in prod:
        print("X(%s) = %g" % (i, X[i]))
else:
    print("\nNon esiste una soluzione ottima :(")

mod.write("Meko.lp")
