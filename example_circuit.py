import Circuit as c

def main():
    #Example Function_dict class
    class Function_dict:
        def AND(self, x):
            return x[0] and x[1]
        def OR(self, x):
            return x[0] or x[1]
        def XOR(self, x):
            return x[0] != x[1]
        def NOT(self, x):
            return not x[0]
        def NAND(self, x):
            return self.NOT([self.AND(x)])
        def NOR(self, x):
            return self.NOT([self.AND(x)])
        def XNOR(self, x):
            return self.NOT([self.AND(x)])
        def ANDONENEG(self, x):
            return self.NOT([self.AND([x[0], self.NOT(x[1])])])

        #Define the dictionary inside __init__ or functions will not be able
        #to use self, and so will not be able to call each other
        def __init__(self):
            #The keys correspond to the last element of each sublist in
            #the chromosome
            self.function_dict = {
                "AND" : self.AND,
                "OR"  : self.OR,
                "XOR" : self.XOR,
                "NAND": self.NAND,
                "NOR" : self.NOR,
                "XNOR": self.XNOR
            }

    #Example approximate adder
    n_inputs = 4
    n_outputs = 3
    n_columns = 3
    n_rows = 2
    chromosome = [[1, 1, 'AND'], [0, 0, 'OR'], [3, 1, 'OR'], [1, 2, 'OR'], [5, 2, 'OR'], [6, 0, 'AND'], 0, 2, 3]
    function_dict = Function_dict()

    #Creates a Circuit using the parameters we just defined
    #From here on, the only modification of the Circuit should be through
    #assigning the inputs and evaluating the output nodes
    x = c.Circuit(n_inputs, n_outputs, n_columns, n_rows, function_dict, chromosome)

    #Example printing the string of a Circuit
    print(str(x))

    #Example showing every input and its corresponding output

    #Iterate over every possible set of binary inputs
    for i in range(2**(n_inputs//2)):
        for j in range(2**(n_inputs//2)):
            #Converts these integers into bnary form, and converts these to lists of 1s and 0s
            input_a = [int(x) for x in list(format(i, "#0{0}b".format(2 + n_inputs//2))[2:])]
            input_b = [int(x) for x in list(format(j, "#0{0}b".format(2 + n_inputs//2))[2:])]
            #Combine the inputs so they can be passed to the Circuit
            inputs = input_a + input_b
            x.set_inputs(inputs)
            print(str(inputs) + " --> " + str(x.execute()))

if __name__ == "__main__":
    main()
