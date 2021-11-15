# 2 prodotti A e B
# 2 materie prima P1 e P2 per produrli
# A richiede 4 P1 e 7 P2
# B richiede 7 P1 e 7 P2
# P1 usata almeno 40 volte/settimana
# P2 usata massimo 49 volte/settimana
# il rapporto tra A e B deve essere tra 1/2 e 4
# Profitto di A è il doppio del profitto di B

# Coefficienti della FO
from main.solutors import SimplexAlgorithm

objcoeff = [1, 2]
# Definisco tassi assorbimento
tassi_assorbimento = [[2, 5], [1, 1], [1, -4], [2, -1]]
# Definisco coeff vincoli
cap = [20, 7, 0, 0]
# Definisco i segni
signs = ['>=', '<=', '<=', '>=']

modContinuous = SimplexAlgorithm.solveMaximizeContinuous('continuous', tassi_assorbimento, signs, cap, objcoeff)
modInteger = SimplexAlgorithm.solveMaximizeInteger('integer', tassi_assorbimento, signs, cap, objcoeff)

SimplexAlgorithm.printSolution(modContinuous)
SimplexAlgorithm.printSolution(modInteger)
