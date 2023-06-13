# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 10:25:33 2020

@author: ength

Algoritmo de alocação de sensores através da centralidade de nó
"""

import numpy as np
import wntr
import matplotlib.pyplot as plt
import networkx as nx


def alocate_sensor(nodes, clusters, sortedCentrality):
    sensors = dict()
    for i in sortedCentrality:
        indexNode = nodes.index(i[0])
        nodeSensorSector = sectorsNetwork[indexNode]
        if nodeSensorSector not in sensors.values():
            sensors.update({i[0]:nodeSensorSector})
        
        if len(sensors) == len(set(clusters)):
            break
            
    return sensors
    

WDS = wntr.network.WaterNetworkModel('redes/exnet_links_closed_kmeans.inp')

# grafo ponderado pela velocidade
sim = wntr.sim.EpanetSimulator(WDS)
results = sim.run_sim()

velocitys = results.link['velocity']
vectorSensorsWeighted = list()

for t in range(len(velocitys)):
    times_travel = list()
    links = list()
    velocity = velocitys.loc[t*3600]
    for link_name, link in WDS.links():
        if link.link_type == 'Pipe':
            if velocity[link_name] != 0:
                time_travel = link.length/velocity[link_name]
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
    closeness_centrality_weighted = nx.closeness_centrality(graph_WDS, distance='weight')
    
    sortedCloseness_centrality = sorted(closeness_centrality.items(), key=lambda x: x[1], reverse=True)
    sortedCloseness_centrality_weighted = sorted(closeness_centrality_weighted.items(), key=lambda x: x[1], reverse=True)
    
    sectorsNetwork = np.load('saves/clusters_kmeans.npy')
    nodesNetwork = WDS.node_name_list
    
    sensors_normal = alocate_sensor(nodesNetwork, sectorsNetwork, sortedCloseness_centrality)
    sensors_weighted = alocate_sensor(nodesNetwork, sectorsNetwork, sortedCloseness_centrality_weighted)
    vectorSensorsWeighted.append(sensors_weighted)
    
    
    # plot
    frontier_links = list(np.load('saves/frontier_links_exnet_kmeans.npy'))
    nodes_list = WDS.node_name_list
    stringClusters = np.load('saves/clusters_kmeans.npy')
    
    sensors_keys = list(sensors_weighted)
    
    for i in sensors_keys:
        index = nodes_list.index(i)
        stringClusters[index] = len(sensors_keys) +  1
    
    sensorsDict = list()
    for i in range(len(stringClusters)):
        sensorsDict.append((nodes_list[i],int(stringClusters[i])))

   
    sensorsDict = dict(sensorsDict)
    
    
    # wntr.graphics.plot_interactive_network(WDS, node_attribute=sensorsDict, node_size=8, link_width=1, figsize=[800,800])
    
    
# np.save('saves/sensors_exnet_kmeans.npy', sensors_weighted)


'''num_sensors = 6
sensorsA = list()
for i in range(num_sensors):
    sensorsA.append(sortedCloseness_centrality_weighted[i])
np.save('saves/sensors_exnet_kmeans.npy', sensorsA)'''






  