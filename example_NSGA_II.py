import circuit_search.circuit_as_func as c_f
import circuit_search.circuit_as_obj as c_o
import circuit_search.fitness as f
import circuit_search.NSGA_II as n

import random
import math
import copy
import time
from collections import Counter
import matplotlib.pyplot as plt

def true_func(a, b):
    return a + b

class Function_dict:
    def AND(x):
        return x[0] & x[1]
    def OR(x):
        return x[0] | x[1]
    def NAND(x):
        return ~(x[0] & x[1])
    def NOR(x):
        return int(not x[0] or x[1])
    def XOR(x):
        return x[0] ^ x[1]
    def XNOR(x):
        return int(x[0] == x[1])
    def ANDONENEG(x):
        return int(x[0] and not x[1])

    function_dict = {
        "AND" : AND,
        "OR"  : OR,
        "XOR" : XOR,
        "NAND": NAND,
        "NOR" : NOR,
        "XNOR": XNOR
    }

def crossover(chromosome_1, chromosome_2):
    return [random.choice([chromosome_1[i], chromosome_2[i]]) for i in range(len(chromosome_1))]
    output = []

def migrate(islands):
    new_islands = copy.deepcopy(islands)
    for i in range(len(islands)):
        for j in range(len(islands)):
            if i==j:
                pass
            else:
                a = random.randrange(len(islands[i]))
                b = random.randrange(len(islands[j]))
                new_islands[i][a] = islands[j][b]
                new_islands[j][b] = islands[i][a]
    return new_islands

if __name__ == "__main__":
    t = time.time()
    n_inputs = 16
    n_outputs = 9
    n_columns = 100
    n_rows = 1
    function_dict = Function_dict()
    EF = f.Error_functions()
    error_functions = EF.error_functions

    ef_1 = "MRE"
    ef_2 = "PWR"
    fitness_1 = error_functions[ef_1]
    fitness_2 = error_functions[ef_2]

    mutate = f.mutate

    pop_size_per_island = 10
    num_islands = 1
    total_iterations = 9 
    iterations_until_migration = 10

    islands = []

    exact_adder = [[7, 15, 'XOR'], [7, 15, 'AND'], [6, 14, 'XOR'], [17, 18, 'AND'], [17, 18, 'XOR'], [6, 14, 'AND'], [19, 21, 'OR'], [5, 13, 'XOR'], [0, 0, 'XOR'], [22, 23, 'AND'], [22, 23, 'XOR'], [5, 13, 'AND'], [25, 27, 'OR'], [4, 12, 'XOR'], [0, 0, 'XOR'], [28, 29, 'AND'], [28, 29, 'XOR'], [4, 12, 'AND'], [31, 33, 'OR'], [3, 11, 'XOR'], [0, 0, 'XOR'], [34, 35, 'AND'], [34, 35, 'XOR'], [3, 11, 'AND'], [37, 39, 'OR'], [2, 10, 'XOR'], [0, 0, 'XOR'], [40, 41, 'AND'], [40, 41, 'XOR'], [2, 10, 'AND'], [43, 45, 'OR'], [1, 9, 'XOR'], [0, 0, 'XOR'], [46, 47, 'AND'], [46, 47, 'XOR'], [1, 9, 'AND'], [49, 51, 'OR'], [0, 8, 'XOR'], [0, 0, 'XOR'], [52, 53, 'AND'], [52, 53, 'XOR'], [0, 8, 'AND'], [55, 57, 'OR'], [0, 0, 'XOR'], [0, 0, 'XOR']] + [[0, 0, 'XOR'] for i in range(55)] + [58, 56, 50, 44, 38, 32, 26, 20, 16]
    empty_circuit = [[0, 0, 'XOR'] for i in range(100)] + [1,1,1,1,1,1,1,1,1]
    
    for i in range(num_islands):
        chromosomes = [f.rand_chromosome_generator(n_inputs, n_outputs, n_columns, n_rows, function_dict) for i in range(pop_size_per_island-2)] + [exact_adder] + [empty_circuit]
        solutions = [[n_inputs, n_outputs, n_columns, n_rows, function_dict, chromosome, true_func] for chromosome in chromosomes]
        islands.append(solutions)

    for i in range(total_iterations // iterations_until_migration):
        print("{0}/{1}".format(i * iterations_until_migration, total_iterations))
        for j in range(iterations_until_migration):
            for k in range(num_islands):
                islands[k] = n.next_generation(islands[k], [fitness_1, fitness_2], crossover, mutate)
        islands = migrate(islands)
    for i in range(total_iterations % iterations_until_migration):
        print("{0}/{1}".format(i+iterations_until_migration*(total_iterations // iterations_until_migration), total_iterations))
        for k in range(num_islands):
            islands[k] = n.next_generation(islands[k], [fitness_1, fitness_2], crossover, mutate)
    print("{0}/{0}".format(total_iterations))
    
    # Combine all islands into one final population
    solutions = [solution for island in islands for solution in island]
    pop_size = len(solutions)

    fitness_lists = n.fitness_lists_generator(solutions, [fitness_1, fitness_2])
    fronts = n.fast_non_dominated_sort(solutions, fitness_lists)[0]
    print(time.time() - t)
    file_out_list = zip(fitness_lists[0], fitness_lists[1], solutions)
    filename = str(time.time())
    for i in file_out_list:
        file = open(filename+".txt", 'a')
        file.write(str(i)+"\n")
        file.close()

    fig = plt.figure()
    for front in fronts:
        x_vals = [fitness_lists[0][i] for i in front]
        y_vals = [fitness_lists[1][i] for i in front]
        combos = list(zip(x_vals, y_vals))
        weight_counter = Counter(combos)

        weights = [20*(weight_counter[(x_vals[i], y_vals[i])])**(1/2) for i, _ in enumerate(x_vals)]

        plt.scatter(x_vals, y_vals, s=weights)
    fig.suptitle("{0} against {1} after {2} generations".format(ef_2, ef_1, total_iterations))
    plt.xlabel(ef_1)
    plt.ylabel(ef_2)
    fig.savefig(filename + ".svg")
    plt.show()

    
