import Circuit as c
import random
import math
import copy

class Function_dict:
    def AND(x):
        return int(x[0] and x[1])
    def OR(x):
        return int(x[0] or x[1])
    def NAND(x):
        return int(not x[0] and x[1])
    def NOR(x):
        return int(not x[0] or x[1])
    def XOR(x):
        return int(x[0] != x[1])
    def XNOR(x):
        return int(x[0] == x[1])
    def ANDONENEG(x):
        return int(x[0] and not x[1])

    function_dict = {
        "AND" : AND,
        "OR"  : OR,
        "XOR" : XOR,
        #"NAND;": NAND,
        #"NOR;" : NOR,
        #"XNOR;": XNOR
    }

class Error_functions:
    def hamming_distance(self, n_inputs, n_outputs, n_columns, n_rows, function_dict, seed):
        circuit = c.Circuit(n_inputs, n_outputs, n_columns, n_rows, function_dict, seed)
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

    def num_error(self, n_inputs, n_outputs, n_columns, n_rows, function_dict, seed):
        circuit = c.Circuit(n_inputs, n_outputs, n_columns, n_rows, function_dict, seed)
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

    def error_probability(self, n_inputs, n_outputs, n_columns, n_rows, function_dict, seed):
        return self.num_error(n_inputs, n_outputs, n_columns, n_rows, function_dict, seed) / 2**n_inputs

    def absolute_error(self, n_inputs, n_outputs, n_columns, n_rows, function_dict, seed):
        circuit = c.Circuit(n_inputs, n_outputs, n_columns, n_rows, function_dict, seed)
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

    def mean_absolute_error(self, n_inputs, n_outputs, n_columns, n_rows, function_dict, seed):
        return self.absolute_error(n_inputs, n_outputs, n_columns, n_rows, function_dict, seed) / 2**n_inputs

    def squared_error(self, n_inputs, n_outputs, n_columns, n_rows, function_dict, seed):
        circuit = c.Circuit(n_inputs, n_outputs, n_columns, n_rows, function_dict, seed)
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

    def mean_squared_error(self, n_inputs, n_outputs, n_columns, n_rows, function_dict, seed):
        return self.squared_error(n_inputs, n_outputs, n_columns, n_rows, function_dict, seed) / 2**n_inputs

    def relative_error(self, n_inputs, n_outputs, n_columns, n_rows, function_dict, seed):
        circuit = c.Circuit(n_inputs, n_outputs, n_columns, n_rows, function_dict, seed)
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

    def mean_relative_error(self, n_inputs, n_outputs, n_columns, n_rows, function_dict, seed):
        return self.relative_error(n_inputs, n_outputs, n_columns, n_rows, function_dict, seed) / 2**n_inputs

    def worst_case_error(self, n_inputs, n_outputs, n_columns, n_rows, function_dict, seed):
        circuit = c.Circuit(n_inputs, n_outputs, n_columns, n_rows, function_dict, seed)
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

    def worst_case_relative_error(self, n_inputs, n_outputs, n_columns, n_rows, function_dict, seed):
        circuit = c.Circuit(n_inputs, n_outputs, n_columns, n_rows, function_dict, seed)
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
        return error

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

def rand_seed_generator(n_inputs, n_outputs, n_columns, n_rows, function_dict):
    seed = []
    for column in range(n_columns):
        for row in range(n_rows):
            gate = []
            gate.append(random.randrange(0,n_inputs + (n_rows*column)))
            gate.append(random.randrange(0,n_inputs + (n_rows*column)))
            gate.append(random.choice(list(function_dict.function_dict.keys())))
            seed.append(gate)
    seed += random.sample(range(len(seed)), n_outputs)
    return seed

def choose_best(n_inputs, n_outputs, n_columns, n_rows, function_dict, seeds, error_function):
    best_weight = math.inf
    for seed in seeds:
        weight = error_function(n_inputs, n_outputs, n_columns, n_rows, function_dict, seed)
        if weight <= best_weight:
            best_seed = copy.deepcopy(seed)
            best_weight = weight
    return best_seed

def mutate(n_inputs, n_outputs, n_columns, n_rows, function_dict, seed):
    seeds = [copy.deepcopy(seed), copy.deepcopy(seed), copy.deepcopy(seed), copy.deepcopy(seed), copy.deepcopy(seed), copy.deepcopy(seed)]
    #loop through seeds
    for seed in seeds[1:]:
        #Chooses random gate in seed
        max_column = random.randrange(n_columns)
        rand_row = random.randrange(n_rows)
        gate_index = max_column * rand_row
        gate_seed = seed[gate_index]
        #Choose between all entries in the gate seed        
        k = random.randrange(len(gate_seed))
        #If not a function
        if k != len(gate_seed) - 1:
            seed[gate_index][k] = random.randrange(gate_index - n_rows + n_inputs)
        else:
            seed[gate_index][k] = random.choice(list(function_dict.function_dict.keys()))
    return seeds
        
def true_func(a, b):
        return a + b

def main():
    n_inputs = 8
    n_outputs = 5
    n_columns = 8
    n_rows = 2
    function_dict = Function_dict()
    EF = Error_functions()
    error_functions = EF.error_functions
        
    error_function = "MSE"
    e_f = error_functions[error_function]

    lmda = 5

    best_seed = []
    seeds = []
    for i in range(1+lmda):
        seeds += [rand_seed_generator(n_inputs, n_outputs, n_columns, n_rows, function_dict)]
    for i in range(5000):
        best_seed = choose_best(n_inputs, n_outputs, n_columns, n_rows, function_dict, seeds, e_f)
        seeds = mutate(n_inputs, n_outputs, n_columns, n_rows, function_dict, best_seed)

    print(best_seed)
    print(str(c.Circuit(n_inputs, n_outputs, n_columns, n_rows, function_dict, best_seed)))
    print("{0}: {1}".format(error_function, e_f(n_inputs, n_outputs, n_columns, n_rows, function_dict, best_seed)))

if __name__ == "__main__":
    main()
