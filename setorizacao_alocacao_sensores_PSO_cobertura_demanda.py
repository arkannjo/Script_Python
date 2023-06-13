# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 16:25:10 2020

@author: ength

Setorização em conjunto com alocação de sensores por cobertura de demanda
"""

import numpy as np
import wntr
import pyswarms as ps


def verify_pression(WDS, status):
    # wn = wntr.network.WaterNetworkModel('redes/exnet_0hThyago.inp')
    links = np.load('saves/frontier_links_exnet_kmeans.npy')
    for i in range(len(status)):
        if status[i] == 0:
            pipe = WDS.get_link(links[i]) 
            pipe.initial_status = 'Closed'

    
    # simulate network and penalize with pressures below minimum pressure
    simulation = wntr.sim.EpanetSimulator(WDS)
    # simulation =  wntr.sim.WNTRSimulator(wn, mode='DD')
    # file_prefix impede erro 305 (salvador da patria) ----------
    results = simulation.run_sim(file_prefix='tempPSO0', save_hyd=True, hydfile='temphyd0.hyd')
    pressures = results.node['pressure']
    minimun_pressure = 8.0
    sum_penalize = 0

    '''for column in pressures.columns:
        query_node = WDS.get_node(column)
        if (query_node.node_type == 'Junction') and (query_node.base_demand > 0) and (pressures[column].values[0] < minimun_pressure):
            penalize = pressures[column].values[0] - minimun_pressure
            sum_penalize += abs(penalize).sum() 
        if (query_node.node_type == 'Junction') and (query_node.base_demand == 0) and (pressures[column].values[0] < 0): 
            penalize = pressures[column].values[0]
            sum_penalize += abs(penalize.sum())'''
            
    for column in pressures.columns:
        query_node = WDS.get_node(column)
        if query_node.node_type == 'Junction' and query_node.base_demand >= 0:
            if query_node.base_demand > 0:
                penalize = pressures[pressures[column]<minimun_pressure][column].values - minimun_pressure
                sum_penalize += abs(penalize).sum() 
            else: 
                penalize = pressures[pressures[column]<0][column].values
                sum_penalize += abs(penalize.sum())

    # for control in controls_:
    #     wn.remove_control(control)
    return sum_penalize
    

def prv_cost(WDS, x_, costs):
    ''' Calcula o custo de setorização
        x_: é uma das n partículas do PSO na iteração atual
        costs: o custo associado a cada diametro de tubulação
        sum_prv_cost: retorna um vetor com o custo penalizado de cada particula n da iteração i
        
    '''
    penalization = verify_pression(WDS, x_)
    cost = np.dot(x_, costs) 

    return cost, penalization


def calculate_cover_matrix(WDS, sensors=None):
    sim = wntr.sim.EpanetSimulator(WDS)
    resuts = sim.run_sim(file_prefix='tempPSO1', save_hyd=True, hydfile='temphyd1.hyd')
    
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
    # timesCoverFee = list()
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
    '''sensors = sensors.tolist()
    # vectorSensors = [1, 1, 1, 1, 1, 1, 1]
    
    
    # vetor binario indicando a presenca ou nao de sensor no node
    vectorSensors = np.zeros((ND_positive))
    # vectorSensors = np.ones((ND_positive)) # todos os nós monitorados
    indexSensors = list()
    
    for key, value in sensors.items():
        index = nodes_list.index(key)
        indexSensors.append(index)
        vectorSensors[index] = 1'''
    
    
    # for i in range(len(sensors)):
    #     if sensors[i] == 1:
    #         vectorSensors[i] = 1
    
    vectorSensors = sensors
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
    
    Aux = np.concatenate((ff, np.zeros((ND_positive,1))), axis=1)
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
    # timesCoverFee.append(coverFee)
            
    # Time += 1

    np.save('saves/cobertura_demanda_kmeans.npy', coverFee)
    return coverFee



def combine_objective_functions(x, WDS, costs, frontier_links, cost_max):
    num_frontier_links = len(frontier_links)
    combined_values = []
    cost_values = []
    cover_demands = []
    cost_min = 0
    cover_fee_min = 0
    cover_fee_max = 100
    
    num_sensors_min = 0
    num_sensors_max = len(WDS.query_node_attribute('base_demand', np.greater_equal, 0.0, node_type=wntr.network.model.Junction))
    
    actual_cost = 10000000
    
    for x_ in x:
        a, pen = prv_cost(WDS, x_[:num_frontier_links], costs)
        # a = prv_cost(np.ones((num_frontier_links)), costs) # todos os tubos abertos
        cost_values.append(a)
        a = (np.sqrt(((a - cost_min) / (cost_max - cost_min)) ** 2)) / 3 + pen
        
        b = calculate_cover_matrix(WDS, x_[num_frontier_links:])
        cover_demands.append(b)
        b = (np.sqrt(((b - cover_fee_max) / (cover_fee_max - cover_fee_min)) ** 2)) / 3 
        
        c = np.sum(x_[num_frontier_links:])
        c = (np.sqrt(((c - num_sensors_min) / (num_sensors_max - num_sensors_min)) ** 2)) / 3
        
        cost_pso = a + b + c
        combined_values.append(cost_pso)   
    
        
        if cost_pso < actual_cost:
            actual_cost = cost_pso
            np.save('saves/cost_partial_combined_kmeans.npy', cost_pso)
            np.save('saves/particle_partial_combined_kmeans.npy', x_)

        
    # combined_values = np.array(combined_values)
    return combined_values



# network
WDS = wntr.network.WaterNetworkModel('redes/exnet_0hThyago.inp')

reservoirs = ['3001', '3002']
for reservoir in reservoirs:
    node = WDS.get_node(reservoir)
    node.base_head = 80

ND_positive = len(WDS.query_node_attribute('base_demand', np.greater_equal, 0.0, node_type=wntr.network.model.Junction))
frontier_links = np.load('saves/frontier_links_exnet_kmeans.npy')

# import prv costs
prv_costs = np.load('saves/prvs_cost_exnet_kmeans.npy')

# cost max
cost_max = np.dot(np.ones(len(frontier_links)), prv_costs)

# dimensions PSO
dimensions = prv_costs.shape[0] + ND_positive
init_particle = np.load('saves/particle_partial_combined_kmeans.npy').reshape(1,dimensions) 
# init_particle = np.ones((1,dimensions)) # particula inicial tudo 1
# PSO constants values
consts = [4, 4, 1]

# hyperparamters PSO
options = {'c1' : consts[0], 'c2' : consts[1], 'w' : consts[2], 'k' : 250, 'p' : 2}

# instance PSO
optimizer_discrete = ps.discrete.BinaryPSO(n_particles=250, dimensions=dimensions, options=options,  init_pos=init_particle)

# realize optimization
cost, pos = optimizer_discrete.optimize(combine_objective_functions, iters=500, WDS=WDS, costs=prv_costs, frontier_links=frontier_links, cost_max=cost_max)

