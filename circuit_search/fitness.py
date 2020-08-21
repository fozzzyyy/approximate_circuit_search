from . import circuit_as_func as c_f
from . import circuit_as_obj as c_o
import random
import math
import copy
import itertools
import numpy as np
from time import time


class Error_functions:
    # circuit_def = [n_inputs, n_outputs, n_columns, n_rows, function_dict, chromosome, true_func]
    def hamming_distance(self, circuit_def):
        n_inputs = circuit_def[0]
        n_outputs = circuit_def[1]
        n_columns = circuit_def[2]
        n_rows = circuit_def[3]
        function_dict = circuit_def[4]
        chromosome = circuit_def[5]
        true_func = circuit_def[6]
        
        circuit_function = c_f.chrom_to_func(chromosome, n_inputs, n_outputs)
        lookup = [np.count_nonzero(int_to_bin_list(i, n_outputs)) for i in range(2**n_outputs)]
        error = 0
        for i in list(itertools.product(range(2**(n_inputs//2)), repeat=2)):
            a = circuit_function(i[0], i[1])
            b = true_func(i[0], i[1])
            error += lookup[a^b]
        return error

    def num_error(self, circuit_def):
        n_inputs = circuit_def[0]
        n_outputs = circuit_def[1]
        n_columns = circuit_def[2]
        n_rows = circuit_def[3]
        function_dict = circuit_def[4]
        chromosome = circuit_def[5]
        true_func = circuit_def[6]

        circuit_function = c_f.chrom_to_func(chromosome, n_inputs, n_outputs)
        error = 0
        for i in list(itertools.product(range(2**(n_inputs//2)), repeat=2)):
            output = circuit_function(i[0], i[1])
            if output != true_func(i[0], i[1]):
                error += 1
        return error

    def error_probability(self, circuit_def):
        n_inputs = circuit_def[0]        
        return self.num_error(circuit_def) / 2**n_inputs

    def absolute_error(self, circuit_def):
        n_inputs = circuit_def[0]
        n_outputs = circuit_def[1]
        n_columns = circuit_def[2]
        n_rows = circuit_def[3]
        function_dict = circuit_def[4]
        chromosome = circuit_def[5]
        true_func = circuit_def[6]
        
        circuit_function = c_f.chrom_to_func(chromosome, n_inputs, n_outputs)
        error = 0
        for i in list(itertools.product(range(2**(n_inputs//2)), repeat=2)):
            output = circuit_function(i[0], i[1])
            error += abs(true_func(i[0], i[1]) - output)
        return error

    def mean_absolute_error(self, circuit_def):
        n_inputs = circuit_def[0]        
        return self.absolute_error(circuit_def) / 2**n_inputs

    def squared_error(self, circuit_def):
        n_inputs = circuit_def[0]
        n_outputs = circuit_def[1]
        n_columns = circuit_def[2]
        n_rows = circuit_def[3]
        function_dict = circuit_def[4]
        chromosome = circuit_def[5]
        true_func = circuit_def[6]
        
        circuit_function = c_f.chrom_to_func(chromosome, n_inputs, n_outputs)
        error = 0
        for i in list(itertools.product(range(2**(n_inputs//2)), repeat=2)):
            output = circuit_function(i[0], i[1])
            error += (true_func(i[0], i[1]) - output)**2
        return error

    def mean_squared_error(self, circuit_def):
        n_inputs = circuit_def[0]
        return self.squared_error(circuit_def) / 2**n_inputs

    def relative_error(self, circuit_def):
        n_inputs = circuit_def[0]
        n_outputs = circuit_def[1]
        n_columns = circuit_def[2]
        n_rows = circuit_def[3]
        function_dict = circuit_def[4]
        chromosome = circuit_def[5]
        true_func = circuit_def[6]
        
        circuit_function = c_f.chrom_to_func(chromosome, n_inputs, n_outputs)
        error = 0
        for i in list(itertools.product(range(2**(n_inputs//2)), repeat=2)):
            output = circuit_function(i[0], i[1])
            true_output = true_func(i[0], i[1])
            this_error = abs(true_output - output)
            if true_output > 1:
                error += this_error / true_output
            else:
                error += this_error
        return error

    def mean_relative_error(self, circuit_def):
        n_inputs = circuit_def[0]
        return self.relative_error(circuit_def) / 2**n_inputs

    def worst_case_error(self, circuit_def):
        n_inputs = circuit_def[0]
        n_outputs = circuit_def[1]
        n_columns = circuit_def[2]
        n_rows = circuit_def[3]
        function_dict = circuit_def[4]
        chromosome = circuit_def[5]
        true_func = circuit_def[6]
        
        circuit_function = c_f.chrom_to_func(chromosome, n_inputs, n_outputs)
        error = 0
        for i in list(itertools.product(range(2**(n_inputs//2)), repeat=2)):
            output = circuit_function(i[0], i[1])
            true_output = true_func(i[0], i[1])
            this_error = abs(true_output - output)
            if this_error > error:
                error = this_error
        return error

    def worst_case_relative_error(self, circuit_def):
        n_inputs = circuit_def[0]
        n_outputs = circuit_def[1]
        n_columns = circuit_def[2]
        n_rows = circuit_def[3]
        function_dict = circuit_def[4]
        chromosome = circuit_def[5]
        true_func = circuit_def[6]
        
        circuit_function = c_f.chrom_to_func(chromosome, n_inputs, n_outputs)
        error = 0
        for i in list(itertools.product(range(2**(n_inputs//2)), repeat=2)):
            output = circuit_function(i[0], i[1])
            true_output = true_func(i[0], i[1])
            this_error = abs(true_output - output)
            if true_output > 1:
                this_error /= true_output
            if this_error > error:
                error = this_error

    def power(self, circuit_def):
        n_inputs = circuit_def[0]
        n_outputs = circuit_def[1]
        n_columns = circuit_def[2]
        n_rows = circuit_def[3]
        function_dict = circuit_def[4]
        chromosome = circuit_def[5]
        true_func = circuit_def[6]
        
        power_dict = {
            "AND" : 75,
            "OR" : 75,
            "XOR" : 161,
            "NAND" : 39,
            "NOR" : 35,
            "XNOR" : 161,
            "NOT" : 22,
            "AND3" : 52,
            "OR3" : 48,
            "XOR3" : 56,
            "NAND3" : 56,
            "NOR3" : 55,
            "XNOR3" : 161
        }
        
        phenotype = get_phenotype(circuit_def)
        return sum([power_dict[chromosome[gate-n_inputs][2]] for gate in phenotype])

    def area(self, circuit_def):
        n_inputs = circuit_def[0]
        n_outputs = circuit_def[1]
        n_columns = circuit_def[2]
        n_rows = circuit_def[3]
        function_dict = circuit_def[4]
        chromosome = circuit_def[5]
        true_func = circuit_def[6]
        
        area_dict = {
            "AND" : 32,
            "OR" : 32,
            "XOR" : 56,
            "NAND" : 24,
            "NOR" : 24,
            "XNOR" : 56,
            "NOT" : 16,
            "AND3" : 32,
            "OR3" : 23,
            "XOR3" : 56,
            "NAND3" : 36,
            "NOR3" : 64,
            "XNOR3" : 56
        }
        
        phenotype = get_phenotype(circuit_def)

        return sum([area_dict[chromosome[gate-n_inputs][2]] for gate in phenotype])

    def __init__(self):
        self.error_functions = {
            "HD": self.hamming_distance,
            "EP": self.error_probability,
            "MAE": self.mean_absolute_error,
            "MSE": self.mean_squared_error,
            "MRE": self.mean_relative_error,
            "WCE": self.worst_case_error,
            "WCRE": self.worst_case_relative_error,
            "PWR": self.power,
            "ARE": self.area
        }


def rand_chromosome_generator(n_inputs, n_outputs, n_columns, n_rows, function_dict):
    chromosome = []
    for column in range(n_columns):
        for row in range(n_rows):
            chromosome.append(rand_gate_generator(n_inputs + (n_rows*column), function_dict))
    chromosome += random.sample(range(len(chromosome)), n_outputs)
    return chromosome

def rand_gate_generator(position, function_dict):
    gate = []
    func = random.choice(list(function_dict.function_dict.keys()))
    k = 2
    if "3" in func:
        k = 3
    elif func == "NOT":
        k = 1
    for i in range(k):
        gate.append(random.randrange(0,position))
    gate.append(func)
    return gate

def choose_best(solutions, error_function):
    best_weight = math.inf
    for solution in solutions:
        weight = error_function(solution)
        if weight <= best_weight:
            best_solution = copy.deepcopy(solution)
            best_weight = weight
    return [best_solution, best_weight]

def get_phenotype(circuit_def):
    n_inputs = circuit_def[0]
    n_outputs = circuit_def[1]
    n_columns = circuit_def[2]
    n_rows = circuit_def[3]
    function_dict = circuit_def[4]
    chromosome = circuit_def[5]
    true_func = circuit_def[6]
    
    circuit = c_o.Circuit(n_inputs, n_outputs, n_columns, n_rows, function_dict, chromosome)
    circuit.execute_without_clear()
    phenotype = []
    for i in range(len(chromosome) - n_outputs):
        if circuit.gates[i + n_inputs].evaluated:
            phenotype.append(i + n_inputs)
    return phenotype

def mutate(circuit_def):
    n_inputs = circuit_def[0]
    n_outputs = circuit_def[1]
    n_columns = circuit_def[2]
    n_rows = circuit_def[3]
    function_dict = circuit_def[4]
    chromosome = circuit_def[5]
    true_func = circuit_def[6]

    phenotype = get_phenotype(circuit_def)
        
    # Remove this line to only modify gates in phenotype
    phenotype = list(range(n_inputs, n_inputs + n_columns * n_rows))

    new_chromosome = copy.deepcopy(chromosome)

    # Change 3 genes in the chromosome
    genes_to_change = random.sample(range(len(new_chromosome)), k=3)
    for i in genes_to_change:
        if i < n_rows*n_columns:
            new_chromosome[i] = rand_gate_generator(i + n_inputs, function_dict)
        else:
            new_chromosome[i] = random.randrange(n_inputs + n_rows*n_columns)
    
    return [n_inputs, n_outputs, n_columns, n_rows, function_dict, new_chromosome, true_func]

def mutate_into_list(circuit_def, lmbda, rand):
    n_inputs = circuit_def[0]
    n_outputs = circuit_def[1]
    n_columns = circuit_def[2]
    n_rows = circuit_def[3]
    function_dict = circuit_def[4]
    chromosome = circuit_def[5]
    true_func = circuit_def[6]
    
    solutions = [circuit_def]

    for i in range(lmbda):
        solutions.append(mutate(circuit_def))
    
    for i in range(rand):
        solutions.append(circuit_def[:5] + [rand_chromosome_generator(n_inputs, n_outputs, n_columns, n_rows, function_dict)] + circuit_def[6:])
    
    return solutions

def int_to_bin_list(x, num_bits):
    output = [1 if digit=='1' else 0 for digit in bin(x)[2:]]
    output = (num_bits * [0] + output)[-num_bits:]
    return output
