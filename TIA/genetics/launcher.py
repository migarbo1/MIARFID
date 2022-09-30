from asyncio import subprocess
import math
import sys, os, subprocess
import threading
def fun(problem, population_size, partitions, descendents):
    subprocess.run("python genetics.py {} {} {} 0.05 {}".format(population_size, descendents, partitions, problem))

if __name__ == '__main__':
    problem = sys.argv[1]
    for population_size in [10, 30, 50, 75]:
        for proportion in [0.2, 0.4, 0.6, 0.8, 1]:
            threads = []
            for partitions in [0.2, 0.4, 0.6, 0.8]:

                descendents = math.floor(population_size*proportion)
                parts = math.floor(population_size*partitions)

                x = threading.Thread(target=fun, args=(problem, population_size, parts, descendents))
                threads.append(x)
                x.start()
            for thread in threads:
                thread.join()