from asyncio import subprocess
import math
import sys, os, subprocess
import threading
def fun(problem, population_size, partitions, descendents, name):
    subprocess.run("python genetics.py {} {} {} 0.05 {} > output{}.txt".format(population_size, descendents, partitions, problem, name))

def funnier(problem, temp, k, n, name):
    subprocess.run("python simulatedAnnealing.py {} {} {} {} > output{}.txt".format(temp, k, problem, n, name))

def run_genetics(problem):
    for population_size in [10, 30, 50, 75]:
        for proportion in [0.2, 0.4, 0.6, 0.8, 1]:
            threads = []
            for partitions in [0.2, 0.4, 0.6, 0.8]:

                descendents = math.floor(population_size*proportion)
                parts = math.floor(problem*partitions)

                x = threading.Thread(target=fun, args=(problem, population_size, parts, descendents))
                threads.append(x)
                x.start()
            for thread in threads:
                thread.join()

def run_sim_ann(problem):
    for temp in [100, 75, 50, 20, 5]:
        threads = []
        for k in [0.05, 0.01, 0.005, 0.001, 0.0005]:
            for n in [1,5,10,20]:
                x = threading.Thread(target=funnier, args=(problem, temp, k, n))
                threads.append(x)
                x.start()
            for thread in threads:
                thread.join()

def run_both(problem):
    threads = []
    for i in range(4):
        x = threading.Thread(target=funnier, args=(problem, 50, 0.001, 20, 'SA-'+str(i)))
        y = threading.Thread(target=fun, args=(problem, 10, 0.6, 0.4, 'GA-'+str(i)))
        threads.append(x)
        x.start()
        threads.append(y)
        y.start()
    for thread in threads:
        thread.join()
    for i in range(4):
        x = threading.Thread(target=funnier, args=(problem, 50, 0.001, 20, 'SA-'+str(i+4)))
        y = threading.Thread(target=fun, args=(problem, 10, 0.6, 0.4, 'GA'+str(i+4)))
        threads.append(x)
        x.start()
        threads.append(y)
        y.start()
    for thread in threads:
        thread.join()

if __name__ == '__main__':
    problem = int(sys.argv[1])
    alg = int(sys.argv[2])
    if alg == 1:
        run_genetics(problem)
    if alg == 2:
        run_sim_ann(problem)
    if alg == 3:
        run_both(problem)