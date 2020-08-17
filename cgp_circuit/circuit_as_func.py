import itertools
import importlib

func_dict = {
    "AND" : "w_{0} & w_{1}",
    "OR" : "w_{0} | w_{1}",
    "XOR" : "w_{0} ^ w_{1}",
    "NAND" : "~(w_{0} & w_{1})",
    "NOR" : "~(w_{0} & w_{1})",
    "XNOR" : "~(w_{0} & w_{1})"
    }

def chrom_to_func_string(chromosome, n_inputs, n_outputs):
    main_chromosome = chromosome[:-n_outputs]
    output_list = chromosome[-n_outputs:]
    func_name = function_namer(chromosome, n_inputs, n_outputs)
    
    # Declare function definition
    func_string = """def {0}(a, b):\n""".format(func_name)

    # Assign input bits
    for i in range(n_inputs//2):
        func_string += "    w_{0} = (a >> {1}) & 0x01\n".format(i, n_inputs//2 - i - 1)
    for i in range(n_inputs//2):
        func_string += "    w_{0} = (b >> {1}) & 0x01\n".format(n_inputs//2 + i, n_inputs//2 - i - 1)

    # Slightly slower method of assigning input bits
    """func_string += ("    a_list = [1 if digit=='1' else 0 for digit in bin(a)[2:]]\n"
                    "    a_list = ({0} * [0] + a_list)[-{0}:]\n"
                    "    b_list = [1 if digit=='1' else 0 for digit in bin(b)[2:]]\n"
                    "    b_list = ({0} * [0] + b_list)[-{0}:]\n"
                    ).format(n_inputs//2)
    a_list_string = "    ["
    b_list_string = "    ["
    for i in range(n_inputs//2):
        a_list_string += "w_{0},".format(i)
        b_list_string += "w_{0},".format(i + n_inputs//2)
    a_list_string = a_list_string[:-1] + "] = a_list\n"
    b_list_string = b_list_string[:-1] + "] = b_list\n"
    func_string += a_list_string + b_list_string"""

    # Perform each logical operation
    for i in range(len(main_chromosome)):
        func_string += "    w_{0} = {1}\n".format(n_inputs + i, func_dict[main_chromosome[i][2]]).format(main_chromosome[i][0], main_chromosome[i][1])

    # Calculate and return output
    func_string += "    y = 0\n"
    for i in range(len(output_list)):
        func_string += "    y |= (w_{0} & 0x01) << {1}\n".format(output_list[i], n_outputs - i - 1)
    func_string += "    return y\n"
    return func_string

def chrom_to_file(chromosome, n_inputs, n_outputs):
    f = open("temp_circuit_file.py", "w")
    f.write(chrom_to_func_string(chromosome, n_inputs, n_outputs))
    f.close()

def function_namer(chromosome, n_inputs, n_outputs):
    main_chromosome = chromosome[:-n_outputs]
    output_list = chromosome[-n_outputs:]
    return 'circuit_' + '_'.join([''.join(map(str,i)) for i in main_chromosome]) + '_' + '_'.join(map(str, output_list))

"""def chrom_to_func(chromosome, n_inputs, n_outputs):
    chrom_to_file(chromosome, n_inputs, n_outputs)
    import temp_circuit_file
    importlib.reload(temp_circuit_file)
    return temp_circuit_file.circuit_function"""

def chrom_to_func(chromosome, n_inputs, n_outputs):
    exec(chrom_to_func_string(chromosome, n_inputs, n_outputs))
    return locals()[function_namer(chromosome, n_inputs, n_outputs)]