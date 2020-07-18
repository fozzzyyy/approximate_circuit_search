from . import circuit as c
import random
import math
import copy

class Error_functions:
    def hamming_distance(self, n_inputs, n_outputs, n_columns, n_rows, function_dict, chromosome, true_func):
        circuit = c.Circuit(n_inputs, n_outputs, n_columns, n_rows, function_dict, chromosome)
        error = 0
        for i in range(2**(n_inputs//2)):
            for j in range(2**(n_inputs//2)):
                input_a = [int(x) for x in list(format(i, "#0{0}b".format(2 + n_inputs//2))[2:])]
                input_b = [int(x) for x in list(format(j, "#0{0}b".format(2 + n_inputs//2))[2:])]
                inputs = input_a + input_b
                circuit.set_inputs(inputs)
                output_gates = circuit.execute()
                true_outputs = list(map(int, list(format(true_func(i,j), "#0{0}b".format(2 + n_outputs))[2:])))
                for k in range(n_outputs):
                    error += true_outputs[k] ^ output_gates[k]
        return error

    def num_error(self, n_inputs, n_outputs, n_columns, n_rows, function_dict, chromosome, true_func):
        circuit = c.Circuit(n_inputs, n_outputs, n_columns, n_rows, function_dict, chromosome)
        error = 0
        for i in range(2**(n_inputs//2)):
            for j in range(2**(n_inputs//2)):
                input_a = [int(x) for x in list(format(i, "#0{0}b".format(2 + n_inputs//2))[2:])]
                input_b = [int(x) for x in list(format(j, "#0{0}b".format(2 + n_inputs//2))[2:])]
                inputs = input_a + input_b
                circuit.set_inputs(inputs)
                output_gates = circuit.execute()
                output = 0
                for k in range(n_outputs):
                    output += output_gates[-k-1] * 2**k
                if output != true_func(i, j):
                    error += 1
        return error

    def error_probability(self, n_inputs, n_outputs, n_columns, n_rows, function_dict, chromosome, true_func):
        return self.num_error(n_inputs, n_outputs, n_columns, n_rows, function_dict, chromosome, true_func) / 2**n_inputs

    def absolute_error(self, n_inputs, n_outputs, n_columns, n_rows, function_dict, chromosome, true_func):
        circuit = c.Circuit(n_inputs, n_outputs, n_columns, n_rows, function_dict, chromosome)
        error = 0
        for i in range(2**(n_inputs//2)):
            for j in range(2**(n_inputs//2)):
                input_a = [int(x) for x in list(format(i, "#0{0}b".format(2 + n_inputs//2))[2:])]
                input_b = [int(x) for x in list(format(j, "#0{0}b".format(2 + n_inputs//2))[2:])]
                inputs = input_a + input_b
                circuit.set_inputs(inputs)
                output_gates = circuit.execute()
                output = 0
                for k in range(n_outputs):
                    output += output_gates[-k-1] * 2**k
                error += abs(true_func(i, j) - output)
        return error

    def mean_absolute_error(self, n_inputs, n_outputs, n_columns, n_rows, function_dict, chromosome, true_func):
        return self.absolute_error(n_inputs, n_outputs, n_columns, n_rows, function_dict, chromosome. true_func) / 2**n_inputs

    def squared_error(self, n_inputs, n_outputs, n_columns, n_rows, function_dict, chromosome, true_func):
        circuit = c.Circuit(n_inputs, n_outputs, n_columns, n_rows, function_dict, chromosome)
        error = 0
        for i in range(2**(n_inputs//2)):
            for j in range(2**(n_inputs//2)):
                input_a = [int(x) for x in list(format(i, "#0{0}b".format(2 + n_inputs//2))[2:])]
                input_b = [int(x) for x in list(format(j, "#0{0}b".format(2 + n_inputs//2))[2:])]
                inputs = input_a + input_b
                circuit.set_inputs(inputs)
                output_gates = circuit.execute()
                output = 0
                for k in range(n_outputs):
                    output += output_gates[-k-1] * 2**k
                error += (true_func(i, j) - output)**2
        return error

    def mean_squared_error(self, n_inputs, n_outputs, n_columns, n_rows, function_dict, chromosome, true_func):
        return self.squared_error(n_inputs, n_outputs, n_columns, n_rows, function_dict, chromosome, true_func) / 2**n_inputs

    def relative_error(self, n_inputs, n_outputs, n_columns, n_rows, function_dict, chromosome, true_func):
        circuit = c.Circuit(n_inputs, n_outputs, n_columns, n_rows, function_dict, chromosome)
        error = 0
        for i in range(2**(n_inputs//2)):
            for j in range(2**(n_inputs//2)):
                input_a = [int(x) for x in list(format(i, "#0{0}b".format(2 + n_inputs//2))[2:])]
                input_b = [int(x) for x in list(format(j, "#0{0}b".format(2 + n_inputs//2))[2:])]
                inputs = input_a + input_b
                circuit.set_inputs(inputs)
                output_gates = circuit.execute()
                output = 0
                true_output = true_func(i, j)
                for k in range(n_outputs):
                    output += output_gates[-k-1] * 2**k
                this_error = abs(true_output - output)
                if true_output > 1:
                    error += this_error / true_output
                else:
                    error += this_error
        return error

    def mean_relative_error(self, n_inputs, n_outputs, n_columns, n_rows, function_dict, chromosome, true_func):
        return self.relative_error(n_inputs, n_outputs, n_columns, n_rows, function_dict, chromosome, true_func) / 2**n_inputs

    def worst_case_error(self, n_inputs, n_outputs, n_columns, n_rows, function_dict, chromosome, true_func):
        circuit = c.Circuit(n_inputs, n_outputs, n_columns, n_rows, function_dict, chromosome)
        error = 0
        for i in range(2**(n_inputs//2)):
            for j in range(2**(n_inputs//2)):
                input_a = [int(x) for x in list(format(i, "#0{0}b".format(2 + n_inputs//2))[2:])]
                input_b = [int(x) for x in list(format(j, "#0{0}b".format(2 + n_inputs//2))[2:])]
                inputs = input_a + input_b
                circuit.set_inputs(inputs)
                output_gates = circuit.execute()
                output = 0
                true_output = true_func(i, j)
                for k in range(n_outputs):
                    output += output_gates[-k-1] * 2**k
                this_error = abs(true_output - output)
                if this_error > error:
                    error = this_error
        return error

    def worst_case_relative_error(self, n_inputs, n_outputs, n_columns, n_rows, function_dict, chromosome, true_func):
        circuit = c.Circuit(n_inputs, n_outputs, n_columns, n_rows, function_dict, chromosome)
        error = 0
        for i in range(2**(n_inputs//2)):
            for j in range(2**(n_inputs//2)):
                input_a = [int(x) for x in list(format(i, "#0{0}b".format(2 + n_inputs//2))[2:])]
                input_b = [int(x) for x in list(format(j, "#0{0}b".format(2 + n_inputs//2))[2:])]
                inputs = input_a + input_b
                circuit.set_inputs(inputs)
                output_gates = circuit.execute()
                output = 0
                true_output = true_func(i, j)
                for k in range(n_outputs):
                    output += output_gates[-k-1] * 2**k
                this_error = abs(true_output - output)
                if true_output > 1:
                    this_error /= true_output
                if this_error > error:
                    error = this_error


    def __init__(self):
        self.error_functions = {
            "HD"   : self.hamming_distance,
            "EP"   : self.error_probability,
            "MAE"  : self.mean_absolute_error,
            "MSE"  : self.mean_squared_error,
            "MRE"  : self.mean_relative_error,
            "WCE"  : self.worst_case_error,
            "WCRE" : self.worst_case_relative_error,
        }

def rand_chromosome_generator(n_inputs, n_outputs, n_columns, n_rows, function_dict):
    chromosome = []
    for column in range(n_columns):
        for row in range(n_rows):
            gate = []
            gate.append(random.randrange(0,n_inputs + (n_rows*column)))
            gate.append(random.randrange(0,n_inputs + (n_rows*column)))
            gate.append(random.choice(list(function_dict.function_dict.keys())))
            chromosome.append(gate)
    chromosome += random.sample(range(len(chromosome)), n_outputs)
    return chromosome

def choose_best(n_inputs, n_outputs, n_columns, n_rows, function_dict, chromosomes, error_function, true_func):
    best_weight = math.inf
    for chromosome in chromosomes:
        weight = error_function(n_inputs, n_outputs, n_columns, n_rows, function_dict, chromosome, true_func)
        if weight <= best_weight:
            best_chromosome = copy.deepcopy(chromosome)
            best_weight = weight
    return best_chromosome

def get_phenotype(n_inputs, n_outputs, n_columns, n_rows, function_dict, chromosome):
    circuit = c.Circuit(n_inputs, n_outputs, n_columns, n_rows, function_dict, chromosome)
    circuit.execute_without_clear()
    phenotype = []
    for i in range(len(chromosome) - n_outputs):
        if circuit.gates[i + n_inputs].evaluated:
            phenotype.append(i + n_inputs)
    return phenotype

def mutate(n_inputs, n_outputs, n_columns, n_rows, function_dict, chromosome, lmbda, rand):
    chromosomes = [chromosome]
    for i in range(lmbda):
        chromosomes.append(copy.deepcopy(chromosome))
    phenotype = get_phenotype(n_inputs, n_outputs, n_columns, n_rows, function_dict, chromosome)
    #Iterate over chromosome copies
    for chromosome in chromosomes[1:]:
        #Change 3 calues in each chromosome
        for j in range(3):
            #Choose a random gate/output that is in the phenotype of the chromosome
            i = random.randrange(len(phenotype) + n_outputs)
            #If we choose a gate
            if i < len(phenotype):
                gate_chromosome = chromosome[phenotype[i] - n_inputs]
                max_column = (phenotype[i] - n_inputs) // n_rows
                #Choose between all entries in the gate chromosome 
                k = random.randrange(len(gate_chromosome))
                #If not the function
                if k != len(gate_chromosome) - 1:
                    #Change input connection to some gate in a previous column
                    gate_chromosome[k] = random.randrange(n_inputs + max_column * n_rows)
                #If the function is chosen
                else:
                    #Change gate function to something from the function dictionary
                    gate_chromosome[k] = random.choice(list(function_dict.function_dict.keys()))
            else:
                k = random.randrange(len(chromosome) - n_outputs, len(chromosome))
                chromosome[k] = random.randrange(n_inputs + len(chromosome) - n_outputs)
    for i in range(rand):
        chromosomes.append(rand_chromosome_generator(n_inputs, n_outputs, n_columns, n_rows, function_dict))
    return chromosomes
