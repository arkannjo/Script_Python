# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 10:08:58 2020

@author: ength

Criação de funções para cálculo de centralidade em redes

"""

import networkx as nx
import numpy as np
import wntr
import matplotlib.pyplot as plt

def calculate_degree_centrality(graph):
    '''Calcula a centralidade de grau dos nós de um grafo'''
    degree = graph.degree()
    degree_centrality = list()
    
    for i in degree:
         degree_centrality.append(i)
    return degree_centrality 

WDS = wntr.network.WaterNetworkModel('redes/exnet_24hThyago.inp')
graph_WDS = WDS.get_graph()

degree_centrality = calculate_degree_centrality(graph_WDS)


# simula a rede para retirar a velocidade e calcular o tempo de transporte
sim = wntr.sim.EpanetSimulator(WDS)
results = sim.run_sim()

velocity = results.link['velocity']
velocity_12h = velocity.loc[43200, :]

times_travel = list()
links = list()
for link_name, link in WDS.links():
    if link.link_type == 'Pipe':
        if velocity_12h[link_name] != 0:
            time_travel = link.length/velocity_12h[link_name]
        else: 
            time_travel = 99999999999
        times_travel.append(time_travel)
        links.append((link.start_node_name, link.end_node_name,time_travel))
        # links.append((link.start_node_name, link.end_node_name))
    else:
        links.append((link.start_node_name, link.end_node_name, 0))
        
graph_WDS = nx.MultiDiGraph()
graph_WDS.add_weighted_edges_from(links)
    
closeness_centrality = nx.closeness_centrality(graph_WDS)
closeness_centrality

graph = WDS.get_graph(link_weight=velocity_12h)
fig, ax = plt.subplots(figsize=(30, 30))
nx.draw(graph_WDS)
plt.show()


