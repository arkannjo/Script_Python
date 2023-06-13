# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 07:14:27 2020

@author: Thyago
"""

import wntr
import numpy as np
import matplotlib.pyplot as plt



# read network
inp_file = 'redes/exnet_24hThyago.inp'
network = wntr.network.WaterNetworkModel(inp_file)


frontier_links = np.load('saves/frontier_links_exnet_kmeans.npy')
status = np.load('saves/status_pso_exnet_kmeans.npy')


#demand
demand = network.query_node_attribute('base_demand', node_type=wntr.network.model.Junction)

#cota
cota= network.query_node_attribute('elevation', node_type=wntr.network.model.Junction)


#clusters
clustersKmeans = np.load('saves/clusters_kmeans.npy')


sumDemandKmeans1 = 0
sumDemandKmeans2 = 0
sumDemandKmeans3 = 0
sumCotaKmeans1 = 0
sumCotaKmeans2 = 0
sumCotaKmeans3 = 0
quantKmeans1 = 0
quantKmeans2 = 0
quantKmeans3 = 0

for i in range(len(demand)):
    if demand[i] >= 0 and clustersKmeans[i] == '0':
        sumDemandKmeans1 = sumDemandKmeans1 + demand[i]
        sumCotaKmeans1 = sumCotaKmeans1 + cota[i]
        quantKmeans1 +=1
        
    elif demand[i] >= 0 and clustersKmeans[i] == '1':
        sumDemandKmeans2 = sumDemandKmeans2 + demand[i]
        sumCotaKmeans2 = sumCotaKmeans2 + cota[i]
        quantKmeans2 +=1
    
    elif demand[i] >= 0 and clustersKmeans[i] == '2':
        sumDemandKmeans3 = sumDemandKmeans3 + demand[i]
        sumCotaKmeans3 = sumCotaKmeans3 + cota[i]
        quantKmeans3 +=1
        
        
        
#clusters
clustersKmedoids = np.load('saves/clusters_kmedoids.npy')


sumDemandKmedoids1 = 0
sumDemandKmedoids2 = 0
sumDemandKmedoids3 = 0
sumCotaKmedoids1 = 0
sumCotaKmedoids2 = 0
sumCotaKmedoids3 = 0
quantKmedoids1 = 0
quantKmedoids2 = 0
quantKmedoids3 = 0


for i in range(len(demand)):
    if demand[i] >= 0 and clustersKmedoids[i] == '0':
        sumDemandKmedoids1 = sumDemandKmedoids1 + demand[i]
        sumCotaKmedoids1 = sumCotaKmedoids1 + cota[i]
        quantKmedoids1 += 1
        
    elif demand[i] >= 0 and clustersKmedoids[i] == '1':
        sumDemandKmedoids2 = sumDemandKmedoids2 + demand[i]
        sumCotaKmedoids2 = sumCotaKmedoids2 + cota[i]
        quantKmedoids2 += 1
    
    elif demand[i] >= 0 and clustersKmedoids[i] == '2':
        sumDemandKmedoids3 = sumDemandKmedoids3 + demand[i]
        sumCotaKmedoids3 = sumCotaKmedoids3 + cota[i]
        quantKmedoids3 += 1
        
        
        
#clusters
clustersHierarquico = np.load('saves/clusters_hierarquico.npy')


sumDemandHierarquico1 = 0
sumDemandHierarquico2 = 0
sumDemandHierarquico3 = 0
sumCotaHierarquico1 = 0
sumCotaHierarquico2 = 0
sumCotaHierarquico3 = 0
quantHierarquico1 = 0
quantHierarquico2 = 0



for i in range(len(demand)):
    if demand[i] >= 0 and clustersHierarquico[i] == '0':
        sumDemandHierarquico1 = sumDemandHierarquico1 + demand[i]
        sumCotaHierarquico1 = sumCotaHierarquico1 + cota[i]
        quantHierarquico1 +=1
        
    elif demand[i] >= 0 and clustersKmedoids[i] == '1':
        sumDemandHierarquico2 = sumDemandHierarquico2 + demand[i]
        sumCotaHierarquico2 = sumCotaHierarquico2 + cota[i]
        quantHierarquico2 +=1
    


#medias
mediaDemandKmeans1 = (sumDemandKmeans1)/quantKmeans1
mediaDemandKmeans2 = (sumDemandKmeans2)/quantKmeans2
mediaDemandKmeans3 = (sumDemandKmeans3)/quantKmeans3
mediaCotaKmeans1 = (sumCotaKmeans1)/quantKmeans1
mediaCotaKmeans2 = (sumCotaKmeans2)/quantKmeans2
mediaCotaKmeans3 = (sumCotaKmeans3)/quantKmeans3


mediaDemandKmedoids1 = (sumDemandKmedoids1)/quantKmedoids1
mediaDemandKmedoids2 = (sumDemandKmedoids2)/quantKmedoids2
mediaDemandKmedoids3 = (sumDemandKmedoids3)/quantKmedoids3
mediaCotaKmedoids1 = (sumCotaKmedoids1)/quantKmedoids1
mediaCotaKmedoids2 = (sumCotaKmedoids2)/quantKmedoids2
mediaCotaKmedoids3 = (sumCotaKmedoids3)/quantKmedoids3


mediaDemandHierarquico1 = (sumDemandHierarquico1)/quantHierarquico1
mediaDemandHierarquico2 = (sumDemandHierarquico2)/quantHierarquico2
mediaCotaHierarquico1 = (sumCotaHierarquico1)/quantHierarquico1
mediaCotaHierarquico2 = (sumCotaHierarquico2)/quantHierarquico2



#plot
quantNodes = 0
for node in demand:
    if node >= 0:
        quantNodes += 1
        
        
fig = plt.figure(figsize=(20,15))
plt.bar(quantNodes,mediaDemandKmeans1)

plt.show()