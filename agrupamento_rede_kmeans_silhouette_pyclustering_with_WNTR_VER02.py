# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 09:36:35 2019

@author: Thyago

Clustering networks with WNTR and PyClustering
"""

import wntr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pyclustering.cluster.kmeans import kmeans
from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer
from pyclustering.cluster.silhouette import silhouette



def calculate_k_from_silhouette_coefficient(data, kmin, kmax):
    # Calculate Silhouette score
    group_silhouette = []
    k_clusters = []
    for k in range(kmin, kmax + 1):
        clusters, final_centers = clustering_with_kmeans(data, k)
        score_silhouette = silhouette(data, clusters).process().get_score()
        group_silhouette.append(np.sum(score_silhouette) / len(score_silhouette))
        k_clusters.append(k)
    max_silhouette = max(group_silhouette)
    index_max_silhouette = group_silhouette.index(max_silhouette)
    optimal_k_cluster = k_clusters[index_max_silhouette]
    return optimal_k_cluster, max_silhouette


def avaliate_clustering_with_silhouette_coefficient(data, clusters):
    score_silhouette = silhouette(data, clusters).process().get_score()
    group_silhouette = np.sum(score_silhouette) / len(score_silhouette)
    return group_silhouette


def clustering_with_kmeans(data, amount_clusters, initial_centers=0):
    # Clustering wiht K-Means
    if initial_centers == 0:
        # Prepare initial centers using K-Means++ method.
        initial_centers = kmeans_plusplus_initializer(data, amount_clusters).initialize()
    else:
        initial_centers = initial_centers

    # Create instance of K-Means algorithm with prepared centers.
    kmeans_instance = kmeans(data, initial_centers)

    # Run cluster analysis and obtain results.
    kmeans_instance.process()
    clusters = kmeans_instance.get_clusters()
    final_centers = kmeans_instance.get_centers()
    return clusters, final_centers


def visualize_clustering(axix, axiy, nodes_clusters, optimal_final_centers):
    # Visualize obtained results    
    #    visualizer = cluster_visualizer_multidim()
    #    visualizer.append_clusters(clusters, listAxis)
    #    visualizer.show()
    #    colors_centers = np.zeros(len(axix))
    #    c = 0
    #    for j in optimal_clusters_kmeans:
    #        for i in j:
    #            colors_centers[i] = c
    #        c += 1
    colors_centers = nodes_clusters
    name_fig = 'imgs/rede_agrupada_kmeans_k_' + str(len(optimal_clusters_kmeans)) + '.png'    
    plt.figure(figsize=(9, 9))
    plt.title('Agrupamento da rede com K-Means e k=' + str(len(optimal_clusters_kmeans)))
    plt.scatter(axix, axiy, c=colors_centers)
    plt.xlabel('Coordenada X')
    plt.ylabel('Coordenada Y')
    plt.savefig(name_fig)    
    plt.show()

    colors_centers = list(colors_centers)
    axix = list(axix)
    axiy = list(axiy)

    for center in optimal_final_centers:
        colors_centers.append(3)
        axix.append(center[0])
        axiy.append(center[1])
#    name_fig = 'imgs/rede_agrupada_kmeans_k_' + str(len(optimal_clusters_kmeans)) + '.png'
    plt.figure(figsize=(9, 9))
    plt.title('Centroids dos Clusters com K-Means')
    plt.scatter(axix, axiy, c=colors_centers)
#    plt.savefig(name_fig)
    plt.show()


def normalize_data(coordinatesx, coordinatesy, nodes_base_demands, nodes_elevations):
    # normalize nodes atributes 0 to 1 and weight coordinates values to * 2.5
    min_coordinatex = min(coordinatesx)
    min_coordinatey = min(coordinatesy)
    max_coordinatex = max(coordinatesx)
    max_coordinatey = max(coordinatesy)
    min_base_demand = min(nodes_base_demands)
    max_base_demand = max(nodes_base_demands)
    min_elevation = min(nodes_elevations)
    max_elevation = max(nodes_elevations)
    normal_coordinatesx = []
    normal_coordinatesy = []
    normal_base_demands = []
    normal_elevations = []


    for i in coordinatesx:
        normal_coordinatesx.append(((i - min_coordinatex) / (max_coordinatex - min_coordinatex)) * 2.5)
    
    for i in coordinatesy:
        normal_coordinatesy.append(((i - min_coordinatey) / (max_coordinatey - min_coordinatey)) * 2.5)
    
    for i in nodes_base_demands:
        normal_base_demands.append((i - min_base_demand) / (max_base_demand - min_base_demand))
    
    for i in nodes_elevations:
        normal_elevations.append((i - min_elevation) / (max_elevation - min_elevation))
    
    return normal_coordinatesx, normal_coordinatesy, normal_base_demands, normal_elevations


def search_link_start_node(end_node):
    start_node = dataFrame_links[dataFrame_links['Link_end_node'] == end_node]['Link_start_node'].values
    return start_node


def search_link_end_node(start_node):
    end_node = dataFrame_links[dataFrame_links['Link_start_node'] == start_node]['Link_end_node'].values
    return end_node


def search_cluster(desire_node, array_junctions_clusters):
    for node, cluster in array_junctions_clusters:
        if desire_node == node:
            desire_cluster = cluster
    return desire_cluster



def realocate_nodes_in_clusters(array_nodes_clusters, links_names, links_start_node_name, links_end_node_name, junctions_array_normalized):
    j = 0
    for node, cluster in array_nodes_clusters:
        list_clusters = []
        for i in range(len(links_names)):
            if (node == links_start_node_name[i]):
                node_end = links_end_node_name[i]
                list_clusters.append(search_cluster(node_end, array_nodes_clusters))
            if (node == links_end_node_name[i]):           
                node_start = links_start_node_name[i]
                list_clusters.append(search_cluster(node_start, array_nodes_clusters))
    # print('\nNode {} está no cluster {} e está ligado aos clusters {}'.format(node, cluster, list_clusters))
        list_clusters = list(set(list_clusters))
        if cluster not in list_clusters:
            array_nodes_clusters[j][1] = list_clusters[0]
            print('Nó {} realocado para o cluster {}'.format(node, array_nodes_clusters[j][1]))
        j += 1
    return array_nodes_clusters



def associate_nodes_remainings(array_junctions_negative, array_junctions_clusters):
    nodes_name = []
    nodes_coordinatex = []
    nodes_coordinatey = []
    nodes_cluster = []
    
    if len(network.query_node_attribute('coordinates', node_type=wntr.network.model.Reservoir)) != 0:
        reservoir = network.query_node_attribute('coordinates', node_type=wntr.network.model.Reservoir)
        for name in reservoir.index.values:
            nodes_name.append(name)
            end_node = search_link_end_node(name)
            nodes_cluster.append(search_cluster(end_node[0], array_junctions_clusters))
        reservoir_coordinates = [coordinates for coordinates in reservoir.values]
        for coordinatex in reservoir_coordinates:
            nodes_coordinatex.append(coordinatex[0])
        for coordinatey in reservoir_coordinates:
            nodes_coordinatey.append(coordinatey[1])
    
    if len(network.query_node_attribute('coordinates', node_type=wntr.network.model.Tank)) != 0:
        tanks = network.query_node_attribute('coordinates', node_type=wntr.network.model.Tank)
        for name in tanks.index.values:
            nodes_name.append(name)
            end_node = search_link_end_node(name)
            nodes_cluster.append(search_cluster(end_node[0], array_junctions_clusters))
        tanks_coordinates = [coordinates for coordinates in tanks.values]
        for coordinatex in tanks_coordinates:
            nodes_coordinatex.append(coordinatex[0])
        for coordinatey in tanks_coordinates:
            nodes_coordinatey.append(coordinatey[1])
            
    if len(array_junctions_negative) != 0:
        for item in array_junctions_negative:
            nodes_name.append(item[0])
            nodes_coordinatex.append(item[1])
            nodes_coordinatey.append(item[2])
            start_node = search_link_start_node(item[0])
            nodes_cluster.append(search_cluster(start_node, array_junctions_clusters))
    
    print('\n\nNós remanecentes')
    i = 0
    for nodes in nodes_name:
        print('Nó {} alocado no cluster {}'.format(nodes, nodes_cluster[i]))
        i += 1
    
    array_nodes_clusters_remainings = np.array([nodes_name, nodes_cluster]).T

    array_nodes_clusters = np.append(array_junctions_clusters, array_nodes_clusters_remainings, axis=0)
    return nodes_coordinatex, nodes_coordinatey, array_nodes_clusters



# read network
inp_file = 'redes/exnet_24hThyago.inp'
network = wntr.network.WaterNetworkModel(inp_file)

# print network
wntr.graphics.plot_network(network)

# query junctions attributes

junctions_names = network.query_node_attribute('name', node_type=wntr.network.model.Junction).values
junctions_coordinates = network.query_node_attribute('coordinates', node_type=wntr.network.model.Junction).values
junctions_base_demands = network.query_node_attribute('base_demand', node_type=wntr.network.model.Junction).values
junctions_elevations = network.query_node_attribute('elevation', node_type=wntr.network.model.Junction).values


# separate coordinates x and y
coordinatesx = []
coordinatesy = []

for coordinate in junctions_coordinates:
    coordinatex, coordinatey = coordinate
    coordinatesx.append(coordinatex)
    coordinatesy.append(coordinatey)




# create a dictionary and dataframe from Junctions
dict_junctions = {'Node_name': junctions_names,
              'Coordinatex': coordinatesx,
              'Coordinatey': coordinatesy,
              'Base_demand': junctions_base_demands,
              'Elevation': junctions_elevations}

dataFrame_junctions = pd.DataFrame(dict_junctions)

# create a array with only negative base_demands Junctions
dataFrame_junctions_negative = dataFrame_junctions.loc[dataFrame_junctions['Base_demand']<0]
array_junctions_negative = dataFrame_junctions_negative[['Node_name', 'Coordinatex', 'Coordinatey']].values

# delete from dataFrame Junctions the Junctions wiht negative base_demands
dataFrame_junctions.drop(dataFrame_junctions.loc[dataFrame_junctions['Base_demand']<0].index, inplace=True)
junctions_names = dataFrame_junctions['Node_name'].values # only positive nodes

# data normalized
normal_coordinatesx, normal_coordinatesy, normal_base_demands, \
normal_elevations = normalize_data(dataFrame_junctions['Coordinatex'].values, 
                                   dataFrame_junctions['Coordinatey'].values, 
                                   dataFrame_junctions['Base_demand'].values, 
                                   dataFrame_junctions['Elevation'].values)

junctions_array_normalized = np.array([normal_coordinatesx, normal_coordinatesy, 
                                       normal_base_demands, normal_elevations]).T

# Calculate optimal number of k-clusters with o silhouette coefficient
kmin = 2
kmax = 50

k_clusters_silhouette, max_silhouette = calculate_k_from_silhouette_coefficient(junctions_array_normalized, kmin, kmax)

# Visualize obtained results
print('\nNúmero ótimo de clusters segundo Coeficiente de Silhueta: ', k_clusters_silhouette)

kAdoted = int(input("Número de clusters adotado: "))

# Clustering K-Means with optimal_k_clusters
group_silhouette = []
optimal_clusters_kmeans = []
optimal_final_centers = []
for i in range(kmin, kmax + 1):
    clusters_kmeans, final_centers = clustering_with_kmeans(junctions_array_normalized, kAdoted)
    group_silhouette.append(avaliate_clustering_with_silhouette_coefficient(junctions_array_normalized, clusters_kmeans))
    optimal_clusters_kmeans.append(clusters_kmeans)
    optimal_final_centers.append(final_centers)

best_group_silhouette = max(group_silhouette)
optimal_clusters_kmeans = optimal_clusters_kmeans[group_silhouette.index(best_group_silhouette)]
optimal_final_centers = optimal_final_centers[group_silhouette.index(best_group_silhouette)]

# create array with node names and node clusters
junctions_clusters = np.arange(len(normal_coordinatesx))
num_of_cluster = 0
for i in optimal_clusters_kmeans:
    for j in i:
        junctions_clusters[j] = num_of_cluster
    num_of_cluster += 1


array_junctions_clusters = np.array([list(junctions_names), 
                                     list(junctions_clusters)]).T.reshape(len(junctions_names),2)


# Visualize obtained results
print('\n\nK-means com k ótimo de %d clusters' % (k_clusters_silhouette))
visualize_clustering(dataFrame_junctions['Coordinatex'], dataFrame_junctions['Coordinatey'], 
                     junctions_clusters, optimal_final_centers)

print('\nCoeficiente de silhueta do grupo: ', best_group_silhouette)
# np.save('saves/silhouette_exnet_kmeans.npy', best_group_silhouette)
print('\nCentroids Finais ótimos: ')
j = 1
for i in optimal_final_centers:
    print('Centroid', j, ':', i)
    j += 1

print('\n\n')


# create dataFrame of links
links_names = network.query_link_attribute('name').values
links_start_node_name = network.query_link_attribute('start_node_name').values
links_end_node_name = network.query_link_attribute('end_node_name').values

dict_links = {'Link_name' : links_names, 'Link_start_node' : 
              links_start_node_name, 'Link_end_node' : links_end_node_name}
dataFrame_links = pd.DataFrame(dict_links)


# Associate remaining nodes with clusters
coordinatesx_remainings, coordinatesy_remainings, array_nodes_clusters = associate_nodes_remainings(array_junctions_negative, array_junctions_clusters)


# Realocate junctions that are in wrong clusters
array_nodes_clusters = realocate_nodes_in_clusters(array_nodes_clusters, links_names, links_start_node_name, links_end_node_name, junctions_array_normalized)

# save array_nodes_clusters in csv:
nodes_tocsv = []
clusters_tocsv = []
for node, cluster in array_nodes_clusters:
    nodes_tocsv.append(node)
    clusters_tocsv.append(cluster)
pd.DataFrame({'Node' : nodes_tocsv, 'Cluster' : clusters_tocsv}).to_csv('saves/setores_exnet_kmeans.csv', index=False)
np.save('saves/nodes_kmeans.npy', nodes_tocsv)
np.save('saves/clusters_kmeans.npy', clusters_tocsv)

#Frontier Links
frontier_links = list()
for i in range(len(links_names)):
    start_cluster = search_cluster(links_start_node_name[i], array_nodes_clusters)
    end_cluster = search_cluster(links_end_node_name[i], array_nodes_clusters)
    if start_cluster != end_cluster:
        frontier_links.append(links_names[i])
print('\nTubulações de Fronteira: \n', frontier_links)

#Initial Status Frontier Links
initial_status_frontier_links = list()
status_links = network.query_link_attribute('status')
diameter_links = network.query_link_attribute('diameter')
diameter_frontier_links = list()
for link in frontier_links:
    initial_status_frontier_links.append(status_links[link])
    diameter_frontier_links.append(diameter_links[link])

#Diamenter Corresponding and Cost PRV
cost_prv = list()
for i in range(len(diameter_frontier_links)):
    if diameter_frontier_links[i] <= 0.102:
        diameter_frontier_links[i] = 0.102
        cost_prv.append(315)
    elif diameter_frontier_links[i] <= 0.152:
        diameter_frontier_links[i] = 0.152
        cost_prv.append(695)    
    elif diameter_frontier_links[i] <= 0.203:
        diameter_frontier_links[i] = 0.203
        cost_prv.append(1501)
    elif diameter_frontier_links[i] <= 0.254:
        diameter_frontier_links[i] = 0.254
        cost_prv.append(2240)
    elif diameter_frontier_links[i] <= 0.305:
        diameter_frontier_links[i] = 0.305
        cost_prv.append(3711)
    elif diameter_frontier_links[i] <= 0.356:
        diameter_frontier_links[i] = 0.356
        cost_prv.append(4470)
    elif diameter_frontier_links[i] <= 0.406:
        diameter_frontier_links[i] = 0.406
        cost_prv.append(7400)
    elif diameter_frontier_links[i] <= 0.457:
        diameter_frontier_links[i] = 0.457
        cost_prv.append(7733)
    elif diameter_frontier_links[i] <= 0.508:
        diameter_frontier_links[i] = 0.508
        cost_prv.append(7750)
    elif diameter_frontier_links[i] <= 0.610:
        diameter_frontier_links[i] = 0.610
        cost_prv.append(9211)
    elif diameter_frontier_links[i] <= 0.711:
        diameter_frontier_links[i] = 0.711
        cost_prv.append(10685)
    else:
        diameter_frontier_links[i] = 0.762
        cost_prv.append(11708)

frontier_links_status_diameter_cost = np.array([frontier_links, initial_status_frontier_links, diameter_frontier_links, cost_prv]).T
np.save('saves/frontier_links_exnet_kmeans.npy',frontier_links)
np.save('saves/prvs_cost_exnet_kmeans.npy',cost_prv)

