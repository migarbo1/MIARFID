from matplotlib import pyplot as plt
import os
import click
import matplotlib
import numpy as np

def read_file(path):
    timeline = []
    status = []
    i = 0
    with open(path, "r") as file:
        for line in file.readlines():
            if line.__contains__('STATUS'):
                line = line.replace('STATUS: ','')
                timeline.append(i)
                status.append(eval(line))
                i+=1
    return timeline, status

def plot_evolution(avg_timeline, avg_status, max_timeline, max_status):
    fig, (ax1, ax2) = plt.subplots(2)
    fig.suptitle("Gossip consensus 500 push")
    fig.set_layout_engine('tight')
    fig.set_size_inches(12, 6.1)
    max_value = max(max_timeline[-1], avg_timeline[-1])
    ax1.set_xticks(range(0, max_value, 1))
    ax2.set_xticks(range(0, max_value, 1))
    for ag in range(len(avg_status[0])):
        agent_value_evolution = np.array(avg_status)[:,ag]
        ax1.set_title("avg value update")
        ax1.plot(avg_timeline, agent_value_evolution)

    for ag in range(len(max_status[0])):
        agent_value_evolution = np.array(max_status)[:,ag]
        ax2.set_title("max value update")
        ax2.plot(max_timeline, agent_value_evolution)
    fig.subplots_adjust(hspace=0.4)
    fig.savefig("500_push.png")

@click.command()
@click.option('--fmax', help='file containing max results')
@click.option('--favg', help='file containing avg results')
def main(fmax, favg):
    a_t, a_s = read_file(favg)
    m_t, m_s = read_file(fmax)
    plot_evolution(a_t, a_s, m_t, m_s)
    
if __name__ == '__main__':
    main()