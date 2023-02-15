from cProfile import label
import json
import math
from time import sleep
from matplotlib.dates import SA
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

alg_imp_problems = ['outputProblem50_base', 'outputProblem50_fixing', 'outputProblem50_doomsday']

#justification for algorithm improvements
# for p in alg_imp_problems:
#     df = pd.read_json('./outputs/algorithm_adjust/{}.json'.format(p))
#     df = df.drop(['problem_size', 'mutation_prob', 'best_gen'], axis=1)
#     print('================================={}====================================='.format(p))
#     print("Convergence rate: {}".format(sum(df['conv_limit_reach'] == True)/df.shape[0]))
#     print("Best solution: {}".format(np.min(df['best_fitness'])))
#     print("Worst solution: {}".format(np.max(df['best_fitness'])))
#     print('solution median: {}'.format(np.median(df['best_fitness'])))
#     print("Solution average: {}".format(np.mean(df['best_fitness'])))
#     print('Solutions far from optimal: {}'.format(np.sum(df['best_fitness'] > np.min(df['best_fitness']) + np.min(df['best_fitness'])*0.1)))
#     print('Time Average: {}'.format(np.mean(df['time'])))
#     print('Time median: {}'.format(np.median(df['time'])))
#     print('==============================================================================')

# parameter estimation
par_est_problems = [(50, ''),(70,'orange'),(85,'green'),(100,'red')]
desc_perc = [0.2, 0.4, 0.6, 0.8, 1]
part_perc = [0.2, 0.4, 0.6, 0.8]
population = [10, 30, 50, 75]


# for p in par_est_problems:
#     df = pd.read_json('./outputs/outputProblem{}.json'.format(p))
#     df = df.drop(['problem_size', 'mutation_prob', 'best_gen'], axis=1)
    
#     df_desc_20 = df[df['descendents'] == math.floor(df['population_size']/0.2)]
#     x = df_desc_20['descendents']
#     y = df_desc_20['best_fitness']
#     plt.plot(x,y, label)
#     plt.show()
#     print(df.head(3))

#gráfica con el fitness respecto a descendientes
# plt.xlabel('\% descendents')
# plt.ylabel('Fitness')

def plot_avg_compTime_vs_population_size():
    plt.xlabel('Population size')
    plt.ylabel('Comp. time avg')
    population = [10, 30, 50, 75]
    for pair in par_est_problems:
        p = pair[0]
        c = pair[1]
        df = pd.read_json('./outputs/outputProblem{}.json'.format(p))
        df = df.drop(['problem_size', 'mutation_prob', 'best_gen'], axis=1)
        fitness_avg = []
        for pop in population:
            df_pop = df[df['population_size'] == pop]
            fitness_avg.append(np.mean(df_pop['time']))
        if c != '':
            plt.plot(population, fitness_avg, label = "prob_size:{}".format(p), color = c)
        else:
            plt.plot(population, fitness_avg, label = "prob_size:{}".format(p))
    plt.legend()
    plt.show()

def plot_fitness_median_vs_population_size():
    fig, axs = plt.subplots(2,2)
    population = [10, 30, 50, 75]
    coords = [[0,0],[0,1],[1,0],[1,1]]
    coord_index = 0
    for pair in par_est_problems:
        p = pair[0]
        c = pair[1]
        i,j = coords[coord_index]
        df = pd.read_json('./outputs/outputProblem{}.json'.format(p))
        df = df.drop(['problem_size', 'mutation_prob', 'best_gen'], axis=1)
        fitness_mean = []
        for pop in population:
            df_pop = df[df['population_size'] == pop]
            fitness_mean.append(np.median(df_pop['best_fitness']))
        if c != '':
            axs[i,j].plot(population, fitness_mean, color=c)
        else:
            axs[i,j].plot(population, fitness_mean)
        axs[i,j].set_title("prob_size:{}".format(p))
        coord_index+=1
        
    for ax in axs.flat:
        ax.set(xlabel='Population size', ylabel='Firness median')

    # Hide x labels and tick labels for top plots and y ticks for right plots.
    for ax in axs.flat:
        ax.label_outer()
    
    fig.show()
    fig.savefig('save.png')

def prove_minimum_variability():
    population = [10, 30, 50, 75]
    for pop in population:
        ratio = []
        for pair in par_est_problems:
            p = pair[0]
            df = pd.read_json('./outputs/outputProblem{}.json'.format(p))
            df = df.drop(['problem_size', 'mutation_prob', 'best_gen'], axis=1)
            df_pop = df[df['population_size'] == pop]
            pop_fit_median = (np.mean(df_pop['best_fitness']))
            pop_fit_best = (np.min(df_pop['best_fitness']))
            r = pop_fit_median/pop_fit_best
            ratio.append(r-1)
        print('Population_size: ', pop)
        print('Fitness variation: {}%'.format(np.mean(ratio)))
        result = '''Population_size:  10
Fitness variation: 0.012520110631219605%
Population_size:  30
Fitness variation: 0.011938002053152763%
Population_size:  50
Fitness variation: 0.01362869552468532%
Population_size:  75
Fitness variation: 0.010019781286105478%'''

def plot_best_desc_number():
    plt.xlabel('% descendents')
    plt.ylabel('Std. Iterations')
    desc_perc = [0.2, 0.4, 0.6, 0.8, 1]
    for pair in par_est_problems:
        p = pair[0]
        c = pair[1]
        df = pd.read_json('./outputs/outputProblem{}.json'.format(p))
        df = df.drop(['problem_size', 'mutation_prob', 'best_gen'], axis=1)
        iter_avg = []
        trust_int = []
        for desc in desc_perc:
            df_pop = df#[df['population_size'] == 10]
            aux = df_pop.loc[:,'population_size'] * desc #seems to prevent SettingWithCopyWarning 
            aux = aux.apply(np.floor)
            df_desc = df_pop[df_pop['descendents'] == aux]
            iter_avg.append(np.std(df_desc['iteration']))
            trust_int.append((np.max(df_desc['iteration']) - np.min(df_desc['iteration']))/2)
        if c != '':
            plt.plot(desc_perc, iter_avg, label = "prob_size:{}".format(p), color = c)
            # plt.errorbar(desc_perc,iter_avg,yerr=trust_int,linestyle='None')

        else:
            plt.plot(desc_perc, iter_avg, label = "prob_size:{}".format(p))
            # plt.errorbar(desc_perc,iter_avg,yerr=trust_int,linestyle='None')

    plt.legend()
    plt.show()
        
def plot_best_partition_number():
    
    plt.xlabel('% Partitions')
    plt.ylabel('Mean Std. fitness')
    part_perc = [0.2, 0.4, 0.6, 0.8]
    means_mean = []
    for desc in desc_perc:
        iter_avg = []
        for pair in par_est_problems:
            p = pair[0]
            c = pair[1]
            df = pd.read_json('./outputs/outputProblem{}.json'.format(p))
            df = df.drop(['problem_size', 'mutation_prob', 'best_gen'], axis=1)
            df_pop = df[df['population_size'] == 10]
            df_desc = df_pop[df_pop['partitions'] == math.floor(p*desc)]
            iter_avg.append(np.std(df_desc['best_fitness']))
        means_mean.append(np.mean(iter_avg))

    plt.plot(desc_perc, means_mean)

    plt.show()

def stuff():
        
    plt.xlabel('% Descendents')
    plt.ylabel('Mean Std. Iteration')
    part_perc = [0.2, 0.4, 0.6, 0.8]
    means_mean = []
    for desc in desc_perc:
        iter_avg = []
        for pair in par_est_problems:
            p = pair[0]
            c = pair[1]
            df = pd.read_json('./outputs/outputProblem{}.json'.format(p))
            df = df.drop(['problem_size', 'mutation_prob', 'best_gen'], axis=1)
            df_pop = df[df['population_size'] == 10]
            aux = df_pop.loc[:,'population_size'] * desc #seems to prevent SettingWithCopyWarning 
            aux = aux.apply(np.floor)
            df_desc = df_pop[df_pop['descendents'] == aux]
            #df_desc = df_pop[df_pop['partitions'] == math.floor(p*desc)]
            iter_avg.append(np.std(df_desc['iteration']))
        means_mean.append(np.mean(iter_avg))

    plt.plot(desc_perc, means_mean)

    plt.show()

def fit_vs_time():

    fig, axs = plt.subplots(2,2, sharex=True)
    fig.suptitle('Fitness evolution by time')
    coords = [[0,0],[0,1],[1,0],[1,1]]
    for ind in range(4):    
        SA_data = []    # [[best, best_in_iter, time]] 
        SA_final_res = []
        GA_data = []    # [[best, best_in_iter, time]] 
        GA_final_res = [] 
        with open('outputSA-{}.txt'.format(ind+1)) as file:
            for line in file.readlines():
                line = line.replace(' ','')
                if line.__contains__('{'):
                    pass
                    #SA_final_res.append(json.load(line))
                else:
                    SA_data.append(line.split(','))

        with open('./outputGA-{}.txt'.format(ind+1)) as file:
            for line in file.readlines():
                line = line.replace(' ','')
                line = line
                if line.__contains__('{'):
                    pass
                    #GA_final_res.append(json.load(line))
                else:
                    GA_data.append(line.split(','))

        #plot y = fitness, x time, 
        i,j = coords[ind]
        x_sa = np.array([float(sol[0]) for sol in SA_data])
        y_sa = np.array([float(sol[-1]) for sol in SA_data])
        sa_argsort = np.argsort(y_sa)
        if(i == 1):
            axs[i,j].plot(y_sa,x_sa[sa_argsort], '.',label='Sim. Annealing')
        else:
            axs[i,j].plot(y_sa,x_sa[sa_argsort], '.')

        x_ga = np.array([float(sol[0]) for sol in GA_data])
        y_ga = np.array([float(sol[-1]) for sol in GA_data])
        ga_argsort = np.argsort(y_ga)
        if(i == 1):
            axs[i,j].plot(y_ga,x_ga[ga_argsort], '.',label='Genetics')
        else:
            axs[i,j].plot(y_ga,x_ga[ga_argsort], '.')

    for ax in axs.flat:
        ax.set(xlabel='Time in sec', ylabel='Fitness')

    fig.tight_layout()
    fig.legend()
    fig.show()
    fig.savefig('./fig1.png')

    plt.clf()
    plt.close()


    fig2, axs2 = plt.subplots(2,2, sharex=True)
    fig2.suptitle('Fitness evolution by time')
    coords = [[0,0],[0,1],[1,0],[1,1]]
    for ind in range(4):    
        SA_data = []    # [[best, best_in_iter, time]] 
        SA_final_res = []
        GA_data = []    # [[best, best_in_iter, time]] 
        GA_final_res = [] 
        with open('outputSA-{}.txt'.format(ind+5)) as file:
            for line in file.readlines():
                line = line.replace(' ','')
                if line.__contains__('{'):
                    pass
                    #SA_final_res.append(json.load(line))
                else:
                    SA_data.append(line.split(','))

        with open('./outputGA-{}.txt'.format(ind+5)) as file:
            for line in file.readlines():
                line = line.replace(' ','')
                line = line
                if line.__contains__('{'):
                    pass
                    #GA_final_res.append(json.load(line))
                else:
                    GA_data.append(line.split(','))

        #plot y = fitness, x time, 
        i,j = coords[ind]
        x_sa = np.array([float(sol[0]) for sol in SA_data])
        y_sa = np.array([float(sol[-1]) for sol in SA_data])
        sa_argsort = np.argsort(y_sa)
        if(i == 0):
            axs2[i,j].plot(y_sa,x_sa[sa_argsort], '.',label='Sim. Annealing')
        else:
            axs2[i,j].plot(y_sa,x_sa[sa_argsort], '.')

        x_ga = np.array([float(sol[0]) for sol in GA_data])
        y_ga = np.array([float(sol[-1]) for sol in GA_data])
        ga_argsort = np.argsort(y_ga)
        if(i == 0):
            axs2[i,j].plot(y_ga,x_ga[ga_argsort], '.',label='Genetics')
        else:
            axs2[i,j].plot(y_ga,x_ga[ga_argsort], '.')

    for ax in axs2.flat:
        ax.set(xlabel='Time in sec', ylabel='Fitness')

    fig2.tight_layout()
    fig2.legend()
    fig2.show()
    fig2.savefig('./fig2.png')

    plt.clf()
    plt.close()

def coses():
    SA_final_res = []
    GA_final_res = [] 
    for ind in range(8):
        with open('outputSA-{}.txt'.format(ind+1)) as file:
            for line in file.readlines():
                line = line.replace(' ','')
                if line.__contains__('{'):
                    pass
                    SA_final_res.append(json.loads(line))

        with open('./outputGA-{}.txt'.format(ind+1)) as file:
            for line in file.readlines():
                line = line.replace(' ','')
                line = line
                if line.__contains__('{'):
                    pass
                    GA_final_res.append(json.loads(line))


    ga_fitness = [a['best_fitness'] for a in GA_final_res]
    sa_fitness = [a['best_fitness'] for a in SA_final_res]
    trivial_fit = [3330.0026483050847,3330.0026483050847,3330.0026483050847,3330.0026483050847,3330.0026483050847,3330.0026483050847,3330.0026483050847,3330.0026483050847]

    plt.title('Fitness comparison')
    plt.xlabel('Iteration')
    plt.ylabel('Fitness')

    plt.plot([1,2,3,4,5,6,7,8], trivial_fit, label='Trivial Assign')
    plt.plot([1,2,3,4,5,6,7,8], ga_fitness, label='Genetics')
    plt.plot([1,2,3,4,5,6,7,8], sa_fitness, label='Sim. Annealing')

    plt.legend()
    plt.show()

    # print('GA fitness std = {}'.format(np.std(ga_fitness)))
    # print('SA fitness std = {}'.format(np.std(sa_fitness)))

fit_vs_time()