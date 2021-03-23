import random
import matplotlib.pyplot as plt
import numpy as np
# import pandas as pd
# generate random demands for a graph G(N,E)
def initialize_demands(I,T):
    '''
        Inputs:
            I number of regions
            T number of time node, thus T-1 time period, 1-indexed
        Output:
            g: dictionarys with the key as tuple: t_o,t_d,z_o,z_d, and value as 0
    '''
    g = {} #key:(t_o,t_d,z_o,z_d), value = 0

    #valid pairs satisfy the condition: t_d > t_o
    for t_o in range(1,T):
        for z_o in range(1,I+1):
            for t_d in range(t_o+1,T+1):
                for z_d in range(1,I+1):
                    g[str(t_o)+"_"+str(t_d)+"_"+str(z_o)+"_"+str(z_d)]=0
    return g

def carlo_monte(demands,I,T):
    '''
         Inputs:
            g: output of function initialize_demands
            r: number of random simulations, usually >=1000
        Output:
            g: updated g with the r simulations
        Process:
            In each random sample, a valid pairs is repeatedly selected
            from the set of valid pairs with probability p
    '''
    g = initialize_demands(I,T)
    #choose random pairs
    demands = round(demands)
    while demands:
        pair = random.choice(list(g.keys()))
        g[pair]+=1
        demands-=1

    plt.plot(list(g.values()))
    return g

def generate_samples(type_of_dist, average_trip,std,S,I,T):
    '''
         Inputs:
            n: number of scenarios
        Output:
            g: n scenarios of g
        Process:
            In each random sample, a valid pairs is repeatedly selected
            from the set of valid pairs with probability p
    '''
    g = {} #g1,g2...,g_s (1-indexed)
    if type_of_dist == 'normal':
        samples_demands = np.random.normal(average_trip,std,S)
    elif type_of_dist == 'gamma':
#         mean = alpha*beta
#         std**2 = alpha*(beta**2)
        beta=std**2/average_trip
        alpha = average_trip/beta
        samples_demands = np.random.gamma(alpha,beta,S)

    count, bins, ignored=plt.hist(samples_demands,20,density=False)
    plt.show()

    for i,demands in enumerate(samples_demands):
        g[i+1]=carlo_monte(demands=demands,I=I,T=T)

    return g
