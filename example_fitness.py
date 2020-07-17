import cgp_circuit.circuit as c
import cgp_circuit.fitness as f

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
        #"NAND;": NAND,
        #"NOR;" : NOR,
        #"XNOR;": XNOR
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

    lmbda = 7

    best_chromosome = []
    chromosomes = []
    for i in range(1+lmbda):
        chromosomes += [f.rand_chromosome_generator(n_inputs, n_outputs, n_columns, n_rows, function_dict)]
    for i in range(100):
        best_chromosome = f.choose_best(n_inputs, n_outputs, n_columns, n_rows, function_dict, chromosomes, e_f, true_func)
        chromosomes = f.mutate(n_inputs, n_outputs, n_columns, n_rows, function_dict, best_chromosome, lmbda)
        
    print(best_chromosome)
    print(str(c.Circuit(n_inputs, n_outputs, n_columns, n_rows, function_dict, best_chromosome)))
    print("{0}: {1}".format(error_function, e_f(n_inputs, n_outputs, n_columns, n_rows, function_dict, best_chromosome, true_func)))

if __name__ == "__main__":
    main()
