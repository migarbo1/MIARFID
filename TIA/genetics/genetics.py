from glob import glob
import json
import math
import random
import numpy as np

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
    ("C","J"):10000000,
    ("C","S"):1.3,
    ("C","C"):1,
}
seed = random.seed(6)

def gen_starting_population(pop_size):
    print("generating starting population...")
    population = []
    while len(population) < pop_size:
        genotype = []
        for _ in range(len(_data)):
            role_index =  random.randint(0,len(roles)-1)
            genotype.append(roles[role_index])
        population.append(genotype)
    print("population generated successfully")
    return population

def compute_fitness(alpha, genotype):
    fitness = 0
    performing_time = 0
    cost = 0

    for index, gen in enumerate(genotype):
        task = _data[index]
        task_real_time = task['t'] * role_modifier[(task['r'], gen)]
        performing_time += task_real_time
        cost += task_real_time * prices_hour[gen]

    fitness = (alpha * performing_time + (1-alpha) * cost)
    return fitness
        
def select_specimens():
    pass

def crossover():
    pass

def mutation():
    pass

def replacement():
    pass

def load_problem(path):
    f = open(path, "r")
    data = json.loads(f.read())
    f.close()
    return data

if __name__ == '__main__':
    _data = load_problem("./simplifiedProblem.json")
    population = gen_starting_population(5)
    for gen in population:
        print(gen)
        print(compute_fitness(0.5,gen))
    
