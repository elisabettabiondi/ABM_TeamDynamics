import networkx as nx
import random
import numpy as np
from scipy.stats import skewnorm
import random
import matplotlib.pyplot as plt
#import PyCX.pycxsimulator 
# Make sure networkx, numpy, scipy, and matplotlib is installed. PyCX.pycxsimulator is not working on my laptop, so ignoring it.

G = nx.fast_gnp_random_graph(n = 20, p = 0.2)
# This is going to be our network of interactions: A random network with 20 nodes and density = 0.2 (we can change this), meaning that the probability that an edge exists between any given pair of nodes = 20%
# I have not implemented the "emotional closeness" yet.

def initialize():
    for i in G.nodes:
        G.nodes[i]['opinion'] = random.random() # Opinion of an agent is a uniform random number between 0 to 1
        G.nodes[i]['initial_opinion'] = G.nodes[i]['opinion'] # Initial opinion 
        G.nodes[i]['openness'] = skewnorm.rvs(a=-10, loc=0.9, scale=0.3, size=1)[0] # Openness of an agent is chosen randomly from a left-skewed normal distribution
        G.nodes[i]['credibility'] = random.random() # Credibility of an agent is chosen uniformly at random between 0 and 1
        if G.nodes[i]['opinion'] >= 0.5: # State of an agent is either 0 or 1, depending on its opinion value
            G.nodes[i]['state'] = 1
        else:
            G.nodes[i]['state'] = 0

def observe():
    plt.cla() # Clears the current plot
    nx.draw(G, cmap = plt.cm.Spectral, vmin = 0, vmax = 1,
            node_color = [G.nodes[i]['state'] for i in G.nodes],
            edge_cmap = plt.cm.binary, edge_vmin = 0, edge_vmax = 1,
            #edge_color = [G.edges[i, j]['weight'] for i, j in G.edges],
            pos = G.pos)
    plt.show()

def update():
    for i in G.nodes:
        Sum_neighbours_credibility = 0
        for j in G.neighbors(i):
            Sum_neighbours_credibility += G.nodes[j]['credibility'] # Obtaining sum of credibility of i's neighbours
        
        sigma_i = 0
        for j in G.neighbors(i):
            sigma_i += G.nodes[j]['credibility']/Sum_neighbours_credibility*G.nodes[j]['opinion'] # This is obtaining the summation part of our update equation
            
        # Now using our full update equation, we will calculate the new opinion of node i        
        open_i = G.nodes[i]['openness']
        initial_opi_i = G.nodes[i]['initial_opinion']
        G.nodes[i]['opinion'] = (1 - open_i)*initial_opi_i + open_i*sigma_i # sigma_i was computed just above
        
        if G.nodes[i]['opinion'] < 0.5: # Now we update the state of the agent i depending on its new opinion
            G.nodes[i]['state'] = 0
        else:
            G.nodes[i]['state'] = 1    

#PyCX.pycxsimulator.GUI().start(func=[initialize, observe, update]) 
#The above line of code throws error in my laptop, please uncomment it and check if it runs on yours!

def run_sumulation(total_timestep):
    average_opinion = []
    time = []
    t = 0
    while t < total_timestep:
        update()
        n = G.number_of_nodes()
        avg_op = sum([G.nodes[i]['opinion'] for i in G.nodes()])/n # Calculating average opinion of all agents after each update
        average_opinion.append(avg_op)
        time.append(t)
        t += 1
        
    return average_opinion, time

def plot_avgOp_vs_time():
    initialize()
    average_opinion, time = run_sumulation(50) # Get values over 50 timesteps
    plt.figure(figsize=(10, 5))
    plt.plot(time, average_opinion, "ro-", markersize = 4)
    plt.xlabel("Timestamp", fontsize=18, color = "black")
    plt.ylabel("Average opinion in team", fontsize=18, color = "black")
    plt.xticks(fontsize=18, color = "black")
    plt.yticks(fontsize=18, color = "black")
    plt.show()
    
plot_avgOp_vs_time() # This will output a plot showing how the average opinion of team members is changing over time.