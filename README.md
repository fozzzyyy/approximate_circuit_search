# CGP-circuits

The purpose of this repository is to allow the user to construct circuits out of logical gates, and to get the output of these circuits whenever they are passed a given set of inputs.

It is based on [Cartesian Genetic Programming](https://en.wikipedia.org/wiki/Cartesian_genetic_programming), or CGP for short.

In this system we can represent digital circuits as a graph, and is called Cartesian because the gates are arranged in a two dimensional grid.

We can represent a given circuit using a chromosome:

Z. Vasicek and L. Sekanina, "Evolutionary Approach to Approximate Digital Circuits Design" in IEEE Transactions on Evolutionary Computation, vol. 19, no. 3, pp. 432-444, June 2015. doi: [10.1109/TEVC.2014.2336175](https://dx.doi.org/10.1109/TEVC.2014.2336175)
(pages 435-436)

## Circuit.py

This file takes defines the Gate and Circuit classes.

### Circuit parameters

* n_inputs: the number of input Gates in the Circuit, often referred to in literature as n_i
* n_outputs: the number of outputs that will be returned after executing the gate, often referred to in literature as n_o
* n_columns: the number of columns that the Gates will be arranged into, often referred to in literature as n_c
* n_rows: the number of rows that the Gates will be arranged into, often referred to in literature as n_r
* function_dict: an object that contains the functions that can be executed by the Gates and a dictionary mapping keys to these function, often referred to in literature as Γ
* chromosome: a list that tells the Circuit what Gates it is made up of, what functions they have, how they connect together, and where the outputs of the Circuit are

Note that the total number of Gates in the Circuit will be n_inputs + (n_columns \* n_rows).

#### function_dict

Circuit.py contains an example of the Function_dict class.

Each function takes a list of inputs as its parameters, and returns some value.

Inside the __init__ function define a dictionary that maps your chosen keywords to these functions.

Note: this dictionary **must** be named self.function_dict

In the body of your program, create an object of this class and pass it to the Circuit constructor

#### chromosome

The valid format for a chromosome is:

[G_1, ..., G_m, o_1, ..., o_n]

where G_k is a list and o_j is an integer.

Each G_k describes a Gate in the Circuit, and the correct format is [x_1, ..., x_n, f], where x_1, ..., x_n are integers denoting the positions of the Gates that will be the inputs of this gate,
and f is the key of a function in function_dict.

In order for Circuits to execute correctly, Gates can only take as inputs Gates that are in a previous column.

o_1, ..., o_n denote the positions of the Gates that will be used as the outputs for the Circuit.
Note that these are read in order from Most Significant Bit to Least Significant Bit.

