input_lengths = 8

chromosome = []

for i in range(input_lengths):
    chromosome.append([input_lengths - i - 1, 2 * input_lengths - i - 1, "XOR"])
    chromosome.append([input_lengths - i - 1, 2 * input_lengths - i - 1, "AND"])

for i in range(input_lengths):
    if i == 0:
        continue
    
    if i == 1:
        chromosome.append([2 * input_lengths + 1, 2 * input_lengths + 2, "XOR"])
        chromosome.append([2 * input_lengths + 1, 2 * input_lengths + 2, "AND"])
        
    else:
        chromosome.append([2 * input_lengths + (2 * i), 2 * input_lengths + (4 * i) + 2, "XOR"])
        chromosome.append([2 * input_lengths + (2 * i), 2 * input_lengths + (4 * i) + 2, "AND"])
        
    chromosome.append([2 * input_lengths + (2 * i) + 1, 4 * (input_lengths + i - 1), "OR"])
    chromosome.append([0, 0, "XOR"])

l = len(chromosome)
chromosome.append(l + 2 * input_lengths - 2)
for i in range(input_lengths - 1):
    chromosome.append(l + (2 * input_lengths) - 3 - (4 * i))
chromosome.append(2 * input_lengths)

print(chromosome)

        
