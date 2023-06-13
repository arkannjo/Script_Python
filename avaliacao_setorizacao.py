# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 15:43:15 2020

@author: ength
"""


import wntr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly
import networkx as nx

# read network
inp_file = 'redes/exnet_24hThyago.inp'
network = wntr.network.WaterNetworkModel(inp_file)

frontier_links = list(np.load('saves/frontier_links_exnet_kmeans.npy'))
nodes_list = network.node_name_list
stringClusters = np.load('saves/clusters_kmeans.npy')
setorizationDict = dict()

for i in range(len(stringClusters)):
    setorizationDict[nodes_list[i]] = int(stringClusters[i]) 


# plot
# nodes, edges = wntr.graphics.plot_interactive_network(network, node_attribute=setorizationDict, node_size=10, link_attribute=frontier_links, link_width=1, add_colorbar=False, figsize=[800,800])
fig, ax = plt.subplots(figsize=(20,15))
nodes, edges = wntr.graphics.plot_network(network, node_attribute=setorizationDict, \
    link_attribute=frontier_links, ax=ax, node_size=90, link_width=5)


#  nodes elevation
# nodes, edges = wntr.graphics.plot_interactive_network(network, node_attribute='elevation', node_size=8, link_width=1, figsize=[800,800])
    
#status PSO
statusPSO = np.load('saves/status_pso_exnet_hierarquico.npy')    

# open links
# openLinks = list()
# for i in range(len(frontier_links)):
#     if statusPSO[i] == 1:
#         openLinks.append(frontier_links[i])

# fig, ax = plt.subplots(figsize=(20,15))        
# nodes, edges = wntr.graphics.plot_network(network, node_attribute=setorizationDict, \
#     link_attribute=openLinks, ax=ax, node_size=90, link_width=5)
