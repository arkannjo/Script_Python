# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 15:42:33 2020

@author: ength

Algoritmo de Cobertura de Demanda - SUSE 2014
"""
import numpy as np
import wntr 
import matplotlib.pyplot as plt
import matplotlib as mlp

mlp.rcParams['font.size'] = 40



WDS = wntr.network.WaterNetworkModel('redes/exnet_24hThyago.inp')

def calculate_cover_matrix(WDS, sensors):
    sim = wntr.sim.EpanetSimulator(WDS)
    resuts = sim.run_sim()
    
    Q = resuts.link['flowrate']
    DEM = resuts.node['demand']
    
    nodes_list = WDS.node_name_list
    ND = WDS.num_nodes
    ND_positive = len(WDS.query_node_attribute('base_demand', np.greater_equal, 0.0))
    num_links = WDS.num_links
    num_reservoirs = WDS.num_reservoirs
    
    
    links_names = WDS.query_link_attribute('name').values
    links_start_node_name = WDS.query_link_attribute('start_node_name').values
    links_end_node_name = WDS.query_link_attribute('end_node_name').values
    links_conections = np.array([links_names, links_start_node_name, links_end_node_name]).T
    
    N11_1 = links_conections
    N11 = links_start_node_name
    N22 = links_end_node_name
    
    
    
    # Per = 12*3600
    # Per = 0
    Time = 0
    timesCoverFee = list()
    while Time <= 24:
        Per = Time * 3600
        MQ = np.zeros((ND, ND))
        
        for i in range(num_links):
            Naa = nodes_list.index(N11[i])
            Nbb = nodes_list.index(N22[i])
            if Q.loc[Per, links_names[i]] > 0.0:
                MQ[Nbb,Naa] = abs(Q.loc[Per, links_names[i]])
            else:
                MQ[Naa, Nbb] = abs(Q.loc[Per, links_names[i]])
                 
        
        # Matriz de fração de água
        f = MQ.copy()
        Vsoma = np.zeros((ND))
        
        for L in range(ND):
            for C in range(ND):
                Vsoma[L] = Vsoma[L] + MQ[L, C]
            if Vsoma[L] == 0:
                Vsoma[L] = 1
        
        
        # fim totalizacao de vazoes aos nos
                
        # cria a matriz de fracao de agua
            
        for L in range(ND):
            for C in range(ND):
                f[L,C] = MQ[L,C] / Vsoma[L]
        
        # Da primeira parte (contribuicao direta)
        f = f.T # Traspõe a matriz de fração para forma usual - vide texto
        
        # Obtençao das contribuiçoes de nós indiretamente contribuintes
        for i in range(ND):
            f[i,i] = 1 # fixa o valor 1 na diagonal da matriz de fração
            
        # Inicio do calculo das contribições e armazenamento na matriz de fração
        for C in range(1, ND, 1):
            for L in range(C):
                if f[L,C] != 0:
                    ID = L
                    MUL = f[L,C]
                    for k in range(ID):
                        f[k,C] = f[k,C] + f[k,ID]*MUL
                        
        # Matriz cobertura 0 ou 1
        criterio = 0.5
        
        for L in range(ND):
            for C in range(ND):
                if f[L,C] >= criterio:
                    f[L,C] = 1
                else:
                    f[L,C] = 0
        
        
        # Calculo da taxa de cobertura 
        # sensors = np.load('saves/sensors_exnet_kmeans.npy', allow_pickle=True)
        # sensors = np.array({'462':0, '1915': 0,'480':1, '840':1, '94':1, '101':0})
        sensors = sensors.tolist()
        # vectorSensors = [1, 1, 1, 1, 1, 1, 1]
        
        
        # vetor binario indicando a presenca ou nao de sensor no node
        vectorSensors = np.zeros((ND_positive))
        # vectorSensors = np.ones((ND_positive)) # todos os nós monitorados
        indexSensors = list()
        
        for key, value in sensors.items():
            index = nodes_list.index(key)
            indexSensors.append(index)
            vectorSensors[index] = 1
        
        
        # for i in range(len(sensors)):
        #     if sensors[i] == 1:
        #         vectorSensors[i] = 1
        
        
        # demandas não negativas e somente Junctions
        vectorDemands = DEM.loc[Per, :].values
        positiveDemands = list()    
        for i in range(len(vectorDemands)):
            if (WDS.get_node(nodes_list[i]).node_type == 'Junction') and (WDS.get_node(nodes_list[i]).base_demand >= 0):
                positiveDemands.append(vectorDemands[i])
        
        columnsSensors = list()
        for i in range(len(vectorSensors)):
            if vectorSensors[i] == 1:
                columnsSensors.append(i)
        
        
        ff = f[:ND_positive, columnsSensors].copy()
        '''
        for i in range(ff.shape[0]):
            for j in range(ff.shape[1]):
                ff[i,j] = ff[i,j] * positiveDemands[i]
                
        coverFee = ff.sum() / np.sum(positiveDemands) * 100'''
        
        Aux = np.concatenate((ff, np.zeros((ND_positive,1))), axis=1)
        soma = len(columnsSensors)
        soma_Aux = sum(Aux.T)
        Vetcob = soma_Aux
        Aux22 = list()
        for i in range(len(Vetcob)):
            if Vetcob[i] > 0.0:
                Aux22.append(i)
        Vetcob[Aux22] = 1
        VCD = Vetcob * positiveDemands
        
        sum_VCD = sum(VCD.T)
        sum_positiveDemands = sum(positiveDemands) 
        coverFee = sum_VCD /sum_positiveDemands * 100
        
        sensorsNames = list()
        for i in range(len(vectorSensors)):
            if vectorSensors[i] ==1:
                sensorsNames.append(nodes_list[i])
        # print('Taxa de cobertura de demanda no tempo {}h para os nós {}: {} %'.format(Per/3600,sensorsNames, coverFee))
        timesCoverFee.append(coverFee)
        Time += 1
    
    np.save('saves/cobertura_demanda_kmeans.npy', timesCoverFee)
    return timesCoverFee

def plot_cover_fee(num_sensors, timesCoverFee):
    hours = np.arange(0, 25)
    fig, ax = plt.subplots(figsize=(50,20))
    ax.plot(hours,timesCoverFee)
    title = 'Cobertura de demanda EXNET com kmeans e ' + str(num_sensors) + ' sensores'
    ax.set(xlabel = 'horas', ylabel = 'Taxa de cobertura', title = title)
    name_fig = 'evolucao_cobertura_demanda_exnet_kmeans_' + str(num_sensors) + '_sensores.png'
    # plt.savefig('imgs/' + name_fig)
    plt.show()
    
    return 'Plotagem com sucesso'

