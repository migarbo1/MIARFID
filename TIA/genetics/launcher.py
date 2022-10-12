from asyncio import subprocess
import math
import sys, os, subprocess
import threading
def fun(problem, population_size, partitions, descendents):
    subprocess.run("python genetics.py {} {} {} 0.05 {}".format(population_size, descendents, partitions, problem))

def funnier(problem, temp, k, conv_time):
    subprocess.run("python simulatedAnnealing.py {} {} {} {}".format(temp, k, conv_time, problem))

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
        for k in [0.05, 0.01, 0.005, 0.001, 0.0005]:
            threads = []
            for conv_time in [10, 15, 20, 25]:

                x = threading.Thread(target=funnier, args=(problem, temp, k, conv_time))
                threads.append(x)
                x.start()
            for thread in threads:
                thread.join()

if __name__ == '__main__':
    problem = int(sys.argv[1])
    alg = int(sys.argv[2])
    if alg == 1:
        run_genetics(problem)
    else:
        run_sim_ann(problem)