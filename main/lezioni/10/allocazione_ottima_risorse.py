# La Meko è una multinazionale che produce biocarburanti
# Presso lo stabilimento di Oaxaca si realizzano 2 prodotti: biometanolo e biodimetiletere
# Il processo produttivo richiede la lavorazione in 3 stabilimenti: preparazione, purificazione ed estrazione
# I tempi necessari per la lavorazione di una tonnellata dei due biocarburanti sono riportati in tabella, insieme
# alla capacità produttiva dei 3 stabilimenti:
#
#                 = Ore lavorazione/tonnellata =
# Stabilimento    Biometanolo  Biodimetilicristo  Capacità_Giornaliera(h)
# Preparazione    0.72         0.85               18
# Purificazione   1.68         1.42               18
# Estrazione      1.92         2.12               16
#
# Il responsabile del marketing ha confermato che ogni tonnellata prodotta di biometanolo e di biocristo può
# essere venduta, realizzando un profitto pari rispettivamente a 540€ e 590€
# Vincoli:
# 0.72x + 0.85y <= 18
# 1.68x + 1.42y <= 18
# 1.92x + 2.12y <= 16
# FO: max 540x + 590y = z

import gurobipy as gp
from gurobipy import GRB

import numpy as np

# Inizializzo il modello
mod = gp.Model('Meko')

# Creo variabili di decisione
prod = range(2)  # equivale ad aggiungerne una per volta con mod.addVar(name='x1')
xvar = mod.addVars(prod, name='X')  # x0, x1
res = range(3)

# Coefficienti della FO
objcoeff = [540, 590]
# Definisco FO
obj = mod.setObjective(xvar.prod(objcoeff), GRB.MAXIMIZE)

# Definisco tassi assorbimento
tassi_assorbimento = [[0.72, 0.85], [1.68, 1.42], [1.92, 2.12]]
# Definisco capacità
cap = [18, 18, 16]

# Aggiungo i vincoli alla funzione obiettivo
constraints = mod.addConstrs(
    (xvar.prod(tassi_assorbimento[i]) <= cap[i] for i in res),
    'ore_per_tonnellata'
)

# Risoluzione
mod.optimize()

# Prelevo soluzione e stampo
if mod.status == GRB.OPTIMAL:
    print("\nSoluzione ottima trovata: %g\n" % mod.objVal)

    X = mod.getAttr('x', xvar)
    for i in prod:
        print("X(%s) = %g" % (i, X[i]))

    # Per vedere il valore delle variabili slack
    y0 = cap[0] - X[0] * tassi_assorbimento[0][0] - X[1] * tassi_assorbimento[0][1]
    y1 = cap[1] - X[1] * tassi_assorbimento[1][0] - X[1] * tassi_assorbimento[1][1]
else:
    print("\nNon esiste una soluzione ottima :(")

mod.write("Meko.lp")
