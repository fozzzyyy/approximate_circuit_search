import circuit_search.circuit_as_func as c_f
import circuit_search.circuit_as_obj as c_o
import circuit_search.fitness as f


def true_func(a, b):
        return a + b


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
        # "NAND;": NAND,
        # "NOR;" : NOR,
        # "XNOR;": XNOR
    }


def main():
    n_inputs = 8
    n_outputs = 5
    n_columns = 8
    n_rows = 2
    function_dict = Function_dict()
    EF = f.Error_functions()
    error_functions = EF.error_functions
        
    error_function = "MSE"
    e_f = error_functions[error_function]

    lmbda = 3
    rand = 3

    best_solution = []
    chromosomes = []
    for i in range(1 + lmbda + rand):
        chromosomes += [f.rand_chromosome_generator(n_inputs, n_outputs, n_columns, n_rows, function_dict)]
    solutions = [[n_inputs, n_outputs, n_columns, n_rows, function_dict, chromosome, true_func] for chromosome in chromosomes]
    for i in range(100):
        best_solution = f.choose_best(solutions, e_f)[0]
        solution = f.mutate_into_list(best_solution, lmbda, rand)
        
    print(best_solution[5])
    print(str(c_o.Circuit(n_inputs, n_outputs, n_columns, n_rows, function_dict, best_solution[5])))
    print("{0}: {1}".format(error_function, e_f(best_solution)))


if __name__ == "__main__":
    main()
