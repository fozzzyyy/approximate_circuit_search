import sys
import itertools

class Gate:
    """
    The main Gate class.

    Attributes:
        input_gates (Gate list): These Gates' outputs will be this Gate's inputs
        function (function): The function that will set the Gate's output
        position (int): The location of the Gate in the Circuit, used in __str__
        output (int): The value that is passed to other Gates in the circuit
        evaluated (bool): If the Gate has been evaluated for these inputs
    """
    def __init__(self, input_gates, function, position):
        """
        Constructor for the Gate class.

        Parameters:
            input_gates (Gate list): These Gates' outputs will be this Gate's inputs
            function (function): The function that will set the Gate's output
            position (int): The location of the Gate in the Circuit, used in __str__

        Takes in a list of gates and a function, and when evaluated
        takes the outputs of its input gates, then passes them to its
        function and sets its output as the result
        """
        self.evaluated = False
        self.input_gates = []
        self.output = 0
        self.input_gates = input_gates
        self.function = function
        self.position = position

    """
    For example, if this gate was the 7th in the circuit and was
    returning the result of gate 1 AND gate 3, this would return
    "7 = [1 AND 3]"
    """
    def __repr__(self):
        return str(self)
    def __str__(self):
        return str(self.position) + " = [" + str(self.input_gates[0].position) + " " + str(self.function.__name__) + " " + str(self.input_gates[1].position) + "]"

    """
    Will calculate and set the output of the gate
    Some gates will be used many times in one circuit, so the evaluated flag
    prevents the function from having to be executed multiple times
    """
    def evaluate(self):
        function_inputs = []
        for gate in self.input_gates:
            if gate.evaluated == False:
                gate.evaluate()
                gate.evaluated = True
            function_inputs += [gate.get_output()]
        self.set_output(self.function(function_inputs))

    #Getter and setter methods
    def set_output(self, output):
        self.output = output

    def get_output(self):
        return self.output

    """
    After a circuit is executed, the gate must have the evaluated flag
    cleared, otherwise it will not be excuted again when the circuit is
    given a new list of input values, and so may return the wrong result
    """
    def clear(self):
        self.evaluated = False



class Input(Gate):
    """
    Special type of gate that has no inputs.

    These will have their values directly assigned before executing the circuit
    The evaluated flag is always true, so this is the base case of the recursion
    in the evaluate method of the gate class
    """
    def __str__(self):
        return str(self.position) + " = [" + str(self.output) + "]"
    
    def __init__(self, position):
        self.position = position
        self.evaluated = True
        self.output = 0

    def clear(self):
        pass

    def evaluate(self):
        pass    


class Circuit:
    """Circuit class."""
    def __repr__(self):
        return str(self)
    def __str__(self):
        string = ""
        for gate in self.gates:
            string += str(gate) + "\n"
        string += "Outputs are: " + str(self.output_chromosome)
        return string
    
    def __init__(self, n_inputs, n_outputs, n_columns, n_rows, function_dict, chromosome):
        """Constructor for Circuit class."""
        main_chromosome = chromosome[:-n_outputs]
        self.output_chromosome = chromosome[-n_outputs:]
        self.n_inputs = n_inputs
        self.n_outputs = n_outputs
        self.n_columns = n_columns
        self.n_rows = n_rows
        self.function_dict = function_dict
        self.chromosome = chromosome

        #Creates the input Gates
        self.gates = []
        for i in range(n_inputs):
            self.gates += [Input(i)]

        #Creates a Gate for each gate in the chromosome   
        for gate in main_chromosome:
            #All but the last element of each list refers to another Gate in the Circuit
            input_gates = []
            for input_gate in gate[:-1]:
                #Add these Gates to a list which we will pass to the new gate
                input_gates.append(self.gates[input_gate])
            #Create a new Gate that takes a list of Gates, a function, and its position in the Circuit as arguments
            self.gates.append(Gate(input_gates, function_dict.function_dict[gate[-1]], len(self.gates)))

    def set_inputs(self, inputs):
        """
        Set the inputs of the Circuit.

        Parameters:
            inputs (int list): Assign each of the input gates to the correspodning values
        """
        for i in range(len(inputs)):
            self.gates[i].set_output(inputs[i])

    def execute(self):
        """Evaluate all needed gates and reutrn necessary outputs."""
        outputs = []
        #Evaluate each Gate that is listed in the output portion of the chromosome
        for output_gate_index in self.output_chromosome:
            output_gate = self.gates[output_gate_index]
            output_gate.evaluate()
            #Add this output to the list of outputs
            outputs += [int(output_gate.get_output())]
        self.clear()
        return outputs

    def clear(self):
        """Set the evaluated flag of each Gate to False."""
        for gate in self.gates:
            gate.clear()

if __name__ == "__main__":
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
    x = Circuit(n_inputs, n_outputs, n_columns, n_rows, function_dict, chromosome)

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

