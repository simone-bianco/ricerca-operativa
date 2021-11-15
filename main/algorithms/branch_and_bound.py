import copy

import numpy as np

import main.solutors.SimplexAlgorithm as simplex_algorithm
import gurobipy as gp
from gurobipy import GRB, Model


def is_zero(number):
    return abs(number) < 0.0000001


def is_float(number):
    return abs(number - np.floor(number)) > 0.0000001


class Node:
    def __init__(self, index: int, model_data, parent=None):
        self.index = index
        self.parent = parent
        self.left_child = None
        self.right_child = None
        self.model_data = model_data
        self.is_solution = False
        self.upper_bound = None
        self.solution = True

    def print(self):
        print("Nodo: %s" % self.index)
        print("Nodo Padre: %s" % self.parent.index)
        print("Model Data:")

    def is_root(self):
        return self.parent is None

    def is_leaf(self):
        return (self.left_child is None) and (self.right_child is None)

    def solve(self, solutions):
        # creo modello
        model = simplex_algorithm.initialize_model_by_model_data(self.model_data)
        # risolvo il modello
        model.optimize()
        # se non è risolvibile termino, il nodo risulterà come foglia non risolvibile
        if model.feasibility() == GRB.INFEASIBLE:
            return
        # se tutte le variabili sono intere questa è soluzione
        variables = model.getAttr('x')
        for i in range(len(variables)):
            # se almeno una variabile non è intera, devo passare ai figli
            if is_float(variables[i]):
                # creo nodo di sinistra aggiungendo tra i vincoli il fatto che la variabile frazionaria deve essere
                # <= dell'approssimazione per difetto
                left_model_data = copy.deepcopy(self.model_data)
                constraint_array = [0] * len(variables)
                constraint_array[i] = 1
                left_model_data.absorption_rates.append(constraint_array)
                left_model_data.signs.append('<=')
                left_model_data.costs.append(np.floor(variables[i]))
                left_model_data.print()
                self.left_child = Node(self.index + 1, left_model_data, self)
                self.left_child.solve(solutions)

                # creo nodo di destra aggiungendo tra i vincoli il fatto che la variabile frazionaria deve essere
                # >= dell'approssimazione per eccesso
                right_model_data = copy.deepcopy(self.model_data)
                constraint_array = [0] * len(variables)
                constraint_array[i] = 1
                right_model_data.absorption_rates.append(constraint_array)
                right_model_data.signs.append('>=')
                right_model_data.costs.append(np.ceil(variables[i]))
                self.right_child = Node(self.index + 2, right_model_data, self)
                self.right_child.solve(solutions)

                self.solution = False

                break
        if self.solution:
            self.solution = model.getVars()
            self.upper_bound = model.objVal
            solutions.append(model)
        return model


class Solver:
    def __init__(self, absorption_rates: list, signs: list, costs: list, obj_coefficients: list, mode):
        self.model_data = simplex_algorithm.ModelData('bnb', absorption_rates, signs, costs, obj_coefficients,
                                                      GRB.CONTINUOUS, mode)
        self.solutions = []

    def solve(self):
        root_node = Node(0, self.model_data)
        root_node.solve(self.solutions)

    def print_solutions(self):
        for solution in self.solutions:
            simplex_algorithm.printSolution(solution)
