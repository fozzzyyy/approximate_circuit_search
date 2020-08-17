import math
import random

known_solutions = []
known_fitness = []

def fitness_lists_generator(solutions, fitness_functions):
    fitness_lists = []
    """
    for fitness_function in fitness_functions:
        fitness_lists.append([fitness_function(p) for p in solutions])
    """
    for i in range(len(fitness_functions)):
        fitness_lists.append([get_fitness(p, fitness_functions, i) for p in solutions])
    
    return fitness_lists

def get_fitness(solution, fitness_functions, i):
    try:
        return known_fitness[known_solutions.index(solution)][i]
    except:
        x = [fitness_function(solution) for fitness_function in fitness_functions]
        known_solutions.append(solution)
        known_fitness.append(x)
        return x[i]        

def fast_non_dominated_sort(solutions, fitness_lists):
    # Takes in list of solutions, and the fitness functions they are solving,
    # and outputs a list of Pareto fronts, a partition of the input solutions
    # fronts[0] is a list of solutions that aren't dominated by any other solutions
    # fronts[i] is a list of solutions that are only dominated by solutions
    # in fronts[j] where j < i

    # Pre calculate each dominance relation:
    # dominate_matrix[p][q] = 1 if p dominates q
    #                        -1 if q dominates p
    #                         0 if neither dominates
    # For solution p to dominate solution q, p must at most equal q in all
    # fitness functions, and must also beat q in at least one fitness function
    dominate_matrix = []

    for p in range(len(solutions)):
        row = []
        for q in range(len(solutions)):
            # p at most equals q in all fitness functions
            leq = all([fitness_list[p] <= fitness_list[q] for fitness_list in fitness_lists])
            # p beats q in at least one fitness function
            lt = any([fitness_list[p] < fitness_list[q] for fitness_list in fitness_lists])
            if leq and lt:
                row.append(1)
            else:
                # q at most equals p in all fitness functions
                geq = all([fitness_list[p] >= fitness_list[q] for fitness_list in fitness_lists])
                # q beats p in at least one fitness function
                gt = any([fitness_list[p] > fitness_list[q] for fitness_list in fitness_lists])
                if geq and gt:
                    row.append(-1)
                else:
                    row.append(0)
        dominate_matrix.append(row)

    # S[i] is the list of solutions that are dominated by solutions[i]
    S = []
    # n[i] is the number of solutions that dominate solutions[i]
    n = []
    # rank[i] is the index of the front containing solutions[i]
    # eg solutions[i] is in fronts[rank[i]]
    rank = []
    fronts = [[]]
    for p in range(len(solutions)):
        S_p = []
        n_p = 0
        p_rank = 0
        for q in range(len(solutions)):
            if dominate_matrix[p][q] == 1:
                S_p.append(q)
            elif dominate_matrix[p][q] == -1:
                n_p += 1
        # If solution p is non dominated by anything, put it in the first front
        if n_p == 0:
            p_rank = 0
            fronts[0].append(p)

        S.append(S_p)
        n.append(n_p)
        rank.append(p_rank)
    i = 0
    # Iterate over fronts until all solutions have been assigned to a front
    while fronts[-1] != []:
        # Q is what will be the next front
        Q = []
        # Iterate over each solution in this already defined front
        for p in fronts[i]:
            # Iterate over solutions that are dominated by solution p
            for q in S[p]:
                # If we have already iterated through all p such that p dominates
                # q, then q must be in the next front, so has rank i+1
                n[q] -= 1
                if n[q] == 0:
                    rank[q] = i + 1
                    if q not in Q:
                        Q.append(q)
        i += 1
        fronts.append(Q)
        
    return [fronts[:-1], rank]

def crowding_distance_assignment(front, fitness_lists):
    distance = [0 for i in range(len(front))]
    fitness_sorted_lists = []
    for fitness_list in fitness_lists:
        fitness_sorted_lists.append(sorted(range(len(fitness_list)), key=lambda k: fitness_list[k]))
    for [fitness_list, fitness_sorted] in zip(fitness_lists, fitness_sorted_lists):
        distance[fitness_sorted[0]] = math.inf
        distance[fitness_sorted[-1]] = math.inf
        for i in range(1, len(fitness_list)-1):
            if max(fitness_list) == min(fitness_list):
                distance[i] = math.inf
            else:
                distance[i] = distance[i] + (fitness_list[fitness_sorted[i+1]] - fitness_list[fitness_sorted[i-1]]) / (max(fitness_list) - min(fitness_list))
    return distance

def next_generation(previous_generation, fitness_functions, crossover, mutate):
    fitness_lists = fitness_lists_generator(previous_generation, fitness_functions)
    [fronts, rank] = fast_non_dominated_sort(previous_generation, fitness_lists)
    N = len(previous_generation)

    # Generate P_(t+1)
    P = []
    i = 0
    # Combine as many of the best fronts as possible while staying below N//2
    while len(P) + len(fronts[i]) < N//2:
        P += [previous_generation[j] for j in fronts[i]]
        i += 1
    # Fill up the remaining part of P_(t+1) by choosing the elements of the next front with the greatest crowding distance
    distance = crowding_distance_assignment(fronts[i], [[fitness_list[i] for i in fronts[i]] for fitness_list in fitness_lists])
    # The [::-1] is needed as otherwise it sorts by lowest crowding distance first
    sorted_front = [x for _,x in sorted(zip(distance, fronts[i]), key=lambda pair: pair[0])][::-1]
    for i in range(N//2 - len(P)):
        P.append(previous_generation[sorted_front[i]])

    # Generate Q_(t+1)
    Q = []
    for i in range(N - len(P)):
        [parent_1, parent_2] = random.sample(P, k=2)
        Q.append(crossover(parent_1, parent_2))
        probability = 0.5
        if random.random() <= probability:
            Q[-1] = mutate(Q[-1])
    return P + Q

if __name__ == "__main__":
    def crossover(a,b):
        r = random.random()
        return [a[i] + r*(b[i]-a[i]) for i in range(len(a))]
    def mutate(a):
        r = random.random()
        return [a[i] * (0.875 + r**3) for i in range(len(a))]

    def fitness_1(x):
        A_1 = 0.5*math.sin(1) - 2*math.cos(1) + math.sin(2) - 1.5*math.cos(2)
        A_2 = 1.5*math.sin(1) - math.cos(1) + 2*math.sin(2) - 0.5*math.cos(2)
        B_1 = 0.5*math.sin(x[0]) - 2*math.cos(x[0]) + math.sin(x[1]) - 1.5*math.cos(x[1])
        B_2 = 1.5*math.sin(x[0]) - math.cos(x[0]) + 2*math.sin(x[1]) - 0.5*math.cos(x[1])
        return 1 + (A_1 - B_1)**2 + (A_2 - B_2)**2

    def fitness_2(x):
        return (x[0]+3)**2 + (x[1]+1)**2
    
    import itertools
    solutions = random.sample(list(itertools.product(range(-4,5), repeat=2)), k=30)
    for i in range(100):
        solutions = next_generation(solutions, [fitness_1, fitness_2], crossover, mutate)
    print(solutions)
