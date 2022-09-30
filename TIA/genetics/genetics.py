import json
import math
import random
import time
import numpy as np
import sys

_data = []
roles = ["J", "S", "C"]
prices_hour = {"J": 19000/8760.0, "S":29615/8760.0, "C":37953/8760.0} #€/h
role_modifier = {#(task_p, worker_p) : modifier
    ("J","J"):1,
    ("J","S"):0.85,
    ("J","C"):0.7,
    ("S","J"):1.3,
    ("S","S"):1,
    ("S","C"):0.85,
    ("C","J"):1000,
    ("C","S"):1.3,
    ("C","C"):1,
}
seed = random.seed(0)
sum_fitness = 0

def gen_starting_population(pop_size):
    population = []
    while len(population) < pop_size:
        genotype = []
        for _ in range(len(_data)):
            role_index =  random.randint(0,len(roles)-1)
            genotype.append(roles[role_index])
        population.append(genotype)
    return population

def compute_fitness(alpha, genotype):
    global sum_fitness
    fitness = 0
    performing_time = 0
    cost = 0

    for index, gen in enumerate(genotype):
        task = _data[index]
        task_real_time = task['t'] * role_modifier[(task['r'], gen)]
        performing_time += task_real_time
        cost += task_real_time * prices_hour[gen]

    fitness = (alpha * performing_time + (1-alpha) * cost)
    fitness = 1/fitness #1/fitness because we want to minimize fitness
    sum_fitness += fitness
    return fitness
        
def select_specimens(population, weights):
    return random.choices(population, weights, k=2)

def crossover(parent_one, parent_two, n, muration_prob):

    parent_one_split = np.array_split(parent_one, n)
    parent_two_split = np.array_split(parent_two, n)
    son_one = []
    son_two = []
    for i in range(len(parent_one_split)):
        son_one += list(parent_one_split[i] if i%2==0 else parent_two_split[i])
        son_two += list(parent_two_split[i] if i%2==0 else parent_one_split[i])
    
    if(random.random() < muration_prob):
        son_one = mutation(son_one)
    
    if(random.random() < muration_prob):
        son_two = mutation(son_two)

    return son_one, son_two

def mutation(son):
    source = random.randint(0, len(son)-1)
    dest = random.randint(0, len(son)-1)
    son[source],son[dest] = son[dest],son[source]
    return son

def replacement(population, newborns, weights):
    for newborn in newborns:
        index = np.argmin(weights)
        weights.pop(index)
        population[index] = newborn
    return population

def load_problem(path):
    f = open(path, "r")
    data = json.loads(f.read())
    f.close()
    return data

def get_weights_array(fitness_array):
    weights = []
    for fit_value in fitness_array:
        weights.append(fit_value/sum_fitness)
    return weights

if __name__ == '__main__':
    t_0 = time.perf_counter()
    population_size = int(sys.argv[1])   #30
    descendents = int(sys.argv[2])      #10
    partitions = int(sys.argv[3])        #3
    mutation_prob = float(sys.argv[4])     #0.05 
    alpha = 0.65
    iterations = 10000

    _data = load_problem("./problem{}.json".format(sys.argv[5]))
    population = gen_starting_population(population_size)
    best_sol = (0.0,[])
    iter = 0
    conv_limit = False
    for i in range(iterations):
        
        if(i-iter > 1500):
            conv_limit = True
            break
        
        fitness_array = []
        sum_fitness = 0

        for gen in population:
            fit = compute_fitness(alpha,gen)
            if(fit > best_sol[0]):
                best_sol = (fit, gen)
                iter = i
            fitness_array.append(fit)

        weights = get_weights_array(fitness_array)
        new_population = []
        for i in range(math.floor(descendents/2)):
            parent_one, parent_two = select_specimens(population, weights)
            son_one, son_two = crossover(parent_one, parent_two, partitions, mutation_prob)
            new_population.append(son_one)
            new_population.append(son_two)
        population = replacement(population, new_population, weights)
    t_1 = time.perf_counter()
    timelapse = t_1-t_0
    print(json.dumps({"problem_size": sys.argv[5],"population_size":population_size, "descendents": descendents, "partitions": partitions, "mutation_prob": mutation_prob, "best_fitness": 1/best_sol[0], "iteration": iter, "conv_limit_reach": conv_limit, "time": timelapse}))


