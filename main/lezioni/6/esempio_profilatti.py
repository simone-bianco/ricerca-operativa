# Un'azienda deve produrre 2 profilatti A e B che richiedono l'impiego di manodopera
# 36 squadre disponibili
# A richiede 3 squadre
# B richiede 6 squadre
# E' necessario produrre 4 lotti/giorno
# 2 tecnologie:
#   - 1: permette di produrre 2 A per ogni B
#   - 2: permette di produrre 2 B per ogni A
# Profitto unitario per A e B, si vuole massimizzare il profitto totale

# FO -> Max z = x + y
# v1 -> 3x + 6y <= 36
# v2 -> x + y >= 4
# v3 -> x <= 2y -> x - 2y <= 0
# v4 -> y <= 2x -> -2x + y <= 0
# v5 -> x,y >= 0

import gurobipy as gp
from gurobipy import GRB

# Inizializza il modello
model = gp.Model('esempio lezione 6: profilatti metallici')

# Crea Variabili Decisione
xA = model.addVar(name="XA")
xB = model.addVar(name="XB")

# Definisco FO
obj = model.setObjective(xA + xB, GRB.MAXIMIZE)

# Definisco i vincoli
constraint_1 = model.addConstr(3 * xA + 6 * xB <= 36, name="Vincolo squadre")
constraint_2 = model.addConstr(xA + xB >= 4, name="Vincolo produzione giornaliera")
constraint_3 = model.addConstr(xA - 2*xB <= 0, name="Vincolo prima tecnologia 1:2")
constraint_4 = model.addConstr(-2*xA + xB <= 0, name="Vincolo seconda tecnologia 2:1")
constraint_5 = model.addConstr(xA >= 0, name="Vincolo xA positiva")
constraint_6 = model.addConstr(xB >= 0, name="Vincolo xB positiva")

# Risolvo il problema
model.optimize()

if model.status == GRB.OPTIMAL:
    print("Soluzione ottima trovata!")
    print('\nObj: %g \n' % model.objVal)
    print('xA = %g' % xA.x)
    print('xB = %g' % xB.x)
else:
    print("Nessuna soluzione ottima trovata!")

#scrive il problema in standard lp compatibile con tutto, anche gurobi
model.write("esempio_profilatto.lp")
