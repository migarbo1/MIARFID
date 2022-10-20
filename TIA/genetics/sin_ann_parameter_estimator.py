from cProfile import label
import math
from matplotlib.lines import lineStyles
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

problems = [50, 70, 85, 100]

def estimate_temperature_StartingValue():
    temps = [100.0, 75.0, 50.0, 20.0, 5.0]
    temps = np.sort(temps)
    plt.title('Fitness std by temperature')
    colors = ['teal', 'darkgray', 'wheat', 'plum']
    for i,problem in enumerate(problems):
        problems_std = []
        print(problem)
        for temp in temps:
            df = pd.read_json('./outputs/simulatedAnnealing/output{}.json'.format(problem))
            df_temp = df[df['temperature'] == temp]
            problems_std.append(np.std(df_temp['best_fitness']))
        plt.plot(temps, problems_std, label='problem: {}'.format(problem), color = colors[i], linestyle='dashdot')

    temp_std_mean = []
    for temp in temps:
        problems_std = []
        for problem in problems:
            df = pd.read_json('./outputs/simulatedAnnealing/output{}.json'.format(problem))
            df_temp = df[df['temperature'] == temp]
            problems_std.append(np.std(df_temp['best_fitness']))
        temp_std_mean.append(np.mean(problems_std))
    plt.plot(temps, temp_std_mean, label='mean', linewidth=3.5, color = 'red')

    plt.ylabel('Fitness std')
    plt.xlabel('Initial temperature')
    plt.xticks([10,20,30,40,50,60,70,80,90,100,110])
    plt.legend()
    plt.show()


def estimate_best_k_value():
    #temp_values = [50, 100]
    k_values = [0.0005, 0.001, 0.005, 0.01, 0.05]
    temp_dict = {50:[], 100:[]}

    plt.title('Iterations until convergence for each K')
    plt.xlabel('K value')
    plt.xticks(np.arange(5),['0.0005','0.001','0.005','0.01','0.05'])
    k_values_str = ['0.0005','0.001','0.005','0.01','0.05']
    plt.ylabel('Iterations')
    for p in problems:
        df = pd.read_json('./outputs/simulatedAnnealing/output{}.json'.format(p))
        iter_mean = []
        for k in k_values:
            df_k = df[df['k'] == k]
            #for t in temp_values:
            #   df_temp = df_k[df_k['temperature'] == t]
            #   temp_dict[t].append(np.mean(df_temp['iteration']))
            iter_mean.append(np.mean(df_k['iteration']))
        plt.plot(k_values_str,iter_mean, label='problem: {}'.format(p))
    plt.legend()
    plt.show()

def best_k_with_temp(): #iterUntilConverGroupedByProblem -> t=50, k=0.001
    #temp_values = [50, 100]
    k_values = [0.0005, 0.001, 0.005, 0.01, 0.05]
    temp_dict = {50:[], 100:[]}

    plt.title('Iterations until convergence for each K')
    plt.xlabel('K value')
    plt.xticks(np.arange(5),['0.0005','0.001','0.005','0.01','0.05'])
    k_values_str = ['0.0005','0.001','0.005','0.01','0.05']
    plt.ylabel('Iterations')
    for t in temp_dict.keys():
        problem_means = []
        for k in k_values:
            iter_mean = []
            for p in problems:
                df = pd.read_json('./outputs/simulatedAnnealing/output{}.json'.format(p))
                df = df[df['temperature'] == t]
                df_k = df[df['k'] == k]
                iter_mean.append(np.mean(df_k['iteration']))
            problem_means.append(np.mean(iter_mean))
        plt.plot(k_values_str,problem_means, label='temperature= {}'.format(t))
    plt.legend()
    plt.show()

def best_neigbour_value_old():
    #for the selected t and k, get num_neigh that minimizes the fitness value over all problems
    t = 50
    k = 0.001

    fig, axs = plt.subplots(2,2, sharex=True)
    coords = [[0,0],[0,1],[1,0],[1,1]]
    # plt.xticks(np.arange(4),['1','5','10','20'])
    neigbors = [1,5,10,20]
    res = []
    plt.ion()
    for index, p in enumerate(problems):
        i,j = coords[index]
        df = pd.read_json('./outputs/simulatedAnnealing/output{}.json'.format(p))
        df = df[df['temperature'] == t]
        df = df[df['k'] == k]
        problem_means = []
        problem_medians = []
        for n in neigbors:
            df_n = df[df['num_neighbours'] == n]
            problem_means.append(np.mean(df_n['best_fitness']))
            problem_medians.append(np.median(df_n['best_fitness']))
        axs[i,j].plot(neigbors, problem_means)
        axs[i,j].set_title('Problem Size: {}'.format(p))

    for ax in axs.flat:
        ax.set(xlabel='Neighbourhood size', ylabel='Fitness')

    fig.tight_layout()
    fig.show()
    fig.savefig('patata.png')

def best_neigbour_value():
    #for the selected t and k, get num_neigh that minimizes the fitness value over all problems
    t = 50
    k = 0.001

    fig, axs = plt.subplots(2,2, sharex=True)
    coords = [[0,0],[0,1],[1,0],[1,1]]
    # plt.xticks(np.arange(4),['1','5','10','20'])
    neigbors = [1,5,10,20]
    res = []
    plt.ion()
    for index, p in enumerate(problems):
        i,j = coords[index]
        df = pd.read_json('./outputs/simulatedAnnealing/output{}.json'.format(p))
        df = df[df['temperature'] == t]
        df = df[df['k'] == k]
        problem_means = []
        problem_medians = []
        for n in neigbors:
            df_n = df[df['num_neighbours'] == n]
            problem_means.append(np.mean(df_n['best_fitness']))
            problem_medians.append(np.median(df_n['best_fitness']))
        axs[i,j].plot(neigbors, problem_means)
        axs[i,j].set_title('Problem Size: {}'.format(p))

    for ax in axs.flat:
        ax.set(xlabel='Neighbourhood size', ylabel='Fitness')

    fig.tight_layout()
    fig.show()
    fig.savefig('patata.png')

best_neigbour_value()

# plt.xlabel('Time without better solution for convergence')
# plt.ylabel('Time (s)')
# for i,p in enumerate(time_plots):
#     plt.plot(conv_times, p, color=colors[i], label=time_labels[i])
# plt.legend()
# plt.show()

# plt.xlabel('Time without better solution for convergence')
# plt.ylabel('Fitness')
# for i,p in enumerate(fitness_plots):
#     plt.plot(conv_times, p, color=colors[i], label=fitness_labels[i])
# plt.legend()
# plt.show()