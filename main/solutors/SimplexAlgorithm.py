import operator

import gurobipy as gp
from gurobipy import GRB
from gurobipy.gurobipy import Model

ops = {'>': operator.gt,
       '<': operator.lt,
       '>=': operator.ge,
       '<=': operator.le,
       '==': operator.eq}


class ModelData:
    def __init__(self, model_name: str, absorption_rates: list, signs: list, costs: list, obj_coefficients: list,
                 vtype=GRB.CONTINUOUS, mode=GRB.MAXIMIZE):
        self.model_name = model_name
        self.absorption_rates = absorption_rates
        self.signs = signs
        self.costs = costs
        self.vtype = vtype
        self.obj_coefficients = obj_coefficients
        self.mode = mode

    def print(self):
        print("model_name: ", self.model_name)
        print("absorption_rates: ", self.absorption_rates)
        print("signs: ", self.signs)
        print("costs: ", self.costs)
        print("vtype: ", self.vtype)
        print("obj_coefficients: ", self.obj_coefficients)
        print("mode: ", self.mode)

def solveMaximizeInteger(model_name: str, absorption_rates: list, signs: list, costs: list,
                         obj_coefficients: list):
    return solve(model_name, absorption_rates, signs, costs, obj_coefficients, GRB.INTEGER, GRB.MAXIMIZE)


def solveMinimizeInteger(model_name: str, absorption_rates: list, signs: list, costs: list,
                         obj_coefficients: list):
    return solve(model_name, absorption_rates, signs, costs, obj_coefficients, GRB.INTEGER, GRB.MINIMIZE)


def solveMaximizeContinuous(model_name: str, absorption_rates: list, signs: list, costs: list,
                            obj_coefficients: list):
    return solve(model_name, absorption_rates, signs, costs, obj_coefficients)


def solveMinimizeContinuous(model_name: str, absorption_rates: list, signs: list, costs: list,
                            obj_coefficients: list):
    return solve(model_name, absorption_rates, signs, costs, obj_coefficients, mode=GRB.MINIMIZE)


def initialize_model_by_model_data(model_data: ModelData) -> Model:
    return initialize_model(
        model_data.model_name,
        model_data.absorption_rates,
        model_data.signs,
        model_data.costs,
        model_data.obj_coefficients,
        model_data.vtype,
        model_data.mode
    )


def initialize_model(model_name: str, absorption_rates: list, signs: list, costs: list, obj_coefficients: list,
                     vtype=GRB.CONTINUOUS, mode=GRB.MAXIMIZE) -> Model:
    mod = gp.Model(model_name)

    prod = range(len(obj_coefficients))
    xvar = mod.addVars(prod, name='X', vtype=vtype)

    mod.setObjective(xvar.prod(obj_coefficients), mode)

    for i in range(len(absorption_rates)):
        constraint_name = 'constraint_' + str(i)
        operation = ops[signs[i]]
        mod.addConstr(
            operation(xvar.prod(absorption_rates[i]), costs[i]),
            constraint_name
        )
    return mod


def solve(model_name: str, absorption_rates: list, signs: list, costs: list, obj_coefficients: list,
          vtype=GRB.CONTINUOUS, mode=GRB.MAXIMIZE) -> Model:
    mod = initialize_model(model_name, absorption_rates, signs, costs, obj_coefficients, vtype, mode)
    mod.optimize()
    return mod


def printSolution(model: Model):
    # Prelevo soluzione e stampo
    if model.status == GRB.OPTIMAL:
        print("\nSoluzione ottima trovata: %g\n" % model.objVal)

        X = model.getAttr('x', model.getVars())
        for i in range(len(model.getVars())):
            print("X(%s) = %g" % (i, X[i]))
    else:
        print("\nNon esiste una soluzione ottima")
