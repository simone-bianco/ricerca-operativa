# 2 prodotti A e B
# 2 materie prima P1 e P2 per produrli
# A richiede 4 P1 e 7 P2
# B richiede 7 P1 e 7 P2
# P1 usata almeno 40 volte/settimana
# P2 usata massimo 49 volte/settimana
# il rapporto tra A e B deve essere tra 1/2 e 4
# Profitto di A è il doppio del profitto di B

# Coefficienti della FO
from main.algorithms.branch_and_bound import Solver
from main.solutors import SimplexAlgorithm
import operator

import gurobipy as gp
from gurobipy import GRB, Constr
from gurobipy.gurobipy import Model

ops = {'>': operator.gt,
       '<': operator.lt,
       '>=': operator.ge,
       '<=': operator.le,
       '==': operator.eq}

model_name = 'test'

obj_coefficients = [1, 2]
# Definisco tassi assorbimento
absorption_rates = [[2, 5], [1, 1], [1, -4], [2, -1]]
# Definisco coeff vincoli
costs = [20, 7, 0, 0]
# Definisco i segni
signs = ['>=', '<=', '<=', '>=']

solver = Solver(absorption_rates, signs, costs, obj_coefficients, GRB.MAXIMIZE)
solver.solve()
solver.print_solutions()

modInteger = SimplexAlgorithm.solveMaximizeInteger('integer', absorption_rates, signs, costs, obj_coefficients)
SimplexAlgorithm.printSolution(modInteger)

# mod = gp.Model(model_name)
# prod = range(len(obj_coefficients))
# xvar = mod.addVars(prod, name='X', vtype=GRB.CONTINUOUS)
# mod.setObjective(xvar.prod(obj_coefficients), GRB.MAXIMIZE)
# for i in range(len(absorption_rates)):
#     constraint_name = 'constraint_' + str(i)
#     operation = ops[signs[i]]
#     mod.addConstr(
#         operation(xvar.prod(absorption_rates[i]), costs[i]),
#         constraint_name
#     )
# mod.optimize()
#
# constr = mod.getObjective()
# print(constr.getAttr('ObjBound'))
