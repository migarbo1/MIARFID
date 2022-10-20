import json, math, random, numpy as np
import sys
import time

_data = []
roles = ["J", "S", "C"]
prices_hour = {"J": 19000/1888.0, "S":29615/1888.0, "C":37953/1888.0} #€/h
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

def create_initial_gen():
    genotype = []
    for i in range(len(_data)):
        role_index =  random.randint(0,len(roles)-1)
        if _data[i]['t'] == 'C' and role_index == 0:
                ch = random.choice([1, 2])
                role_index = ch
        genotype.append(roles[role_index])
    return genotype

def create_descendent(gen):
    new_gen = []
    prob = 0.15
    one_changed = False
    times_failed = 0
    for index, g in enumerate(gen):
        if random.random() < prob:
            other_roles = [r for r in roles if r != g]
            new_gen.append(random.choice(other_roles))
            prob = 0.15
            one_changed = True
            times_failed =0
        else:
            times_failed +=1
            new_gen.append(g)
            prob += 0.05*times_failed
            if index == len(gen) and not one_changed:
                prob = 1
    return new_gen

def compute_fitness(alpha, gen):
    fitness = 0
    performing_time = 0
    cost = 0

    for index, g in enumerate(gen):
        task = _data[index]

        #correct specimen
        if(task['r']) == 'C' and g == 'J':
            cs = random.choice(['S', 'C'])
            gen[index] = cs
            g = cs

        task_real_time = task['t'] * role_modifier[(task['r'], g)]
        performing_time += task_real_time
        cost += task_real_time * prices_hour[g]

    fitness = (alpha * performing_time + (1-alpha) * cost)
    return fitness, performing_time, cost

def load_problem(path):
    f = open(path, "r")
    data = json.loads(f.read())
    f.close()
    return data

if __name__ == '__main__':
    alpha = 0.65
    initial_temp = float(sys.argv[1]) #50
    temp = initial_temp
    k = float(sys.argv[2]) #0.001
    neighbours = int(sys.argv[4])
    initial_time = time.perf_counter()

    _data = load_problem("./problem{}.json".format(sys.argv[3]))

    best_gen = create_initial_gen()
    actual_gen = best_gen
    best_fitness,_,_ = compute_fitness(alpha, actual_gen)
    actual_fitness = best_fitness

    iter = 0
    t_0 = time.perf_counter()
    i = 0
    while True:
        act_fit = []
        for j in range(neighbours):
            new_gen = create_descendent(actual_gen)
            new_gen_fitness,_,_ = compute_fitness(alpha, new_gen)
            act_fit.append(new_gen_fitness)
            dif = actual_fitness - new_gen_fitness
            if dif > 0:
                actual_gen = new_gen
                actual_fitness = new_gen_fitness
                if new_gen_fitness < best_fitness:
                    best_gen = actual_gen
                    best_fitness = actual_fitness
                    iter = i
            else:
                exp = dif/temp
                prob = math.pow(math.e, exp)
                if random.random() < prob:
                    actual_gen = new_gen
                    actual_fitness = new_gen_fitness
        if i > 0:
            print('{},{},{}'.format(best_fitness, np.max(act_fit), time.perf_counter()-t_0))

        if i-iter > 15000:
            conv_limit = True
            break

        temp = temp/(1+k*temp)
        i+=1

    tup = compute_fitness(alpha,best_gen)
    print(json.dumps({"problem_size": sys.argv[3],"temperature": initial_temp,"k": k, "num_neighbours": neighbours, "best_fitness": tup[0], "task_time":  tup[1], "task_cost":  tup[2], "iteration": iter, "conv_limit_reach": conv_limit, "time": time.perf_counter() - initial_time, "best_gen": best_gen}))
