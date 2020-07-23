input_lengths = 4

chromosome = []

if input_lengths == 1:
    chromosome = [[0, 1, "XOR"], [0, 1, "AND"], [0, 0, "XOR"], 3, 2]
else:
    for i in range(input_lengths - 1):
        if i == 0:
            chromosome.append([input_lengths - 1, 2 * input_lengths - 1, "XOR"])
            chromosome.append([input_lengths - 1, 2 * input_lengths - 1, "AND"])
            chromosome.append([input_lengths - 2, 2 * input_lengths - 2, "XOR"])
            chromosome.append([2 * input_lengths + 1, 2 * input_lengths + 2, "AND"])
            chromosome.append([2 * input_lengths + 1, 2 * input_lengths + 2, "XOR"])
            chromosome.append([input_lengths - 2, 2 * input_lengths - 2, "AND"])
        else:
            chromosome.append([2 * input_lengths + 6 * i - 3, 2 * input_lengths + 6 * i - 1, "OR"])
            chromosome.append([input_lengths - i - 2, 2 * input_lengths - i - 2, "XOR"])
            chromosome.append([0, 0, "XOR"])
            chromosome.append([2 * input_lengths + 6 * i, 2 * input_lengths + 6 * i + 1, "AND"])
            chromosome.append([2 * input_lengths + 6 * i, 2 * input_lengths + 6 * i + 1, "XOR"])
            chromosome.append([input_lengths - i - 2, 2 * input_lengths - i - 2, "AND"])

    chromosome.append([2 * input_lengths + 6 * (input_lengths - 1) - 3, 2 * input_lengths + 6 * (input_lengths - 1) - 1, "OR"])
    chromosome.append([0, 0, "XOR"])
    chromosome.append([0, 0, "XOR"])

    length = len(chromosome)
    chromosome.append(2 * input_lengths + length - 3)
    for i in range(input_lengths - 1):
        chromosome.append(length + 2 * input_lengths - 5 - i * 6)
    chromosome.append(2 * input_lengths)

print("n_inputs = {0}".format(2 * input_lengths))
print("n_outputs = {0}".format(1 + input_lengths))
print("n_columns = {0}".format(2 * input_lengths - 1))
print("n_rows = 3")

print(chromosome)

        
