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
objcoeff = [3000, 5000]
# Definisco FO
obj = mod.setObjective(xvar.prod(objcoeff), GRB.MAXIMIZE)

# Definisco tassi assorbimento
tassi_assorbimento = [[1, 1], [1, 0], [0, 1], [1, 2]]
# Definisco capacità
cap = [12, 10, 6, 16]

# Aggiungo i vincoli alla funzione obiettivo
constraints = mod.addConstrs(
    (xvar.prod(tassi_assorbimento[i]) <= cap[i] for i in res),
    'cose'
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
