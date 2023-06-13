# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 20:45:46 2019

@author: ength
Algoritmo Mestrado
Otimização do fechamento de tubuluação para a setorização de SDAs
Utilização do algoritmo PSO
"""

import time
import numpy as np
import wntr
import wntr.network.controls as controls
import pyswarms as ps
import matplotlib.pyplot as plt
from IPython.display import Image 
from pyswarms.utils.plotters import (plot_cost_history, plot_contour, plot_surface)
from pyswarms.utils.plotters.formatters import Mesher, Designer


def verify_pression(status):
    wn = wntr.network.WaterNetworkModel('redes/exnet_24hThyago.inp')
    links = np.load('saves/frontier_links_exnet_kmeans.npy')
    '''controls_ = list()
    # add controls to change links status with PSO particles
    for i in range(len(status)):
        pipe = wn.get_link(links[i])    
        act1 = controls.ControlAction(pipe, 'status', status[i])
        cond = controls.SimTimeCondition(wn, '=', '00:00:00')
        control = controls.Control(cond, act1, name='mudaStatus')
        name='control'+str(i)
        controls_.append(name)
        wn.add_control(name, control)'''
    for i in range(len(status)):
        if status[i] == 0:
            pipe = wn.get_link(links[i]) 
            pipe.initial_status = 'Closed'

    
    # simulate network and penalize with pressures below minimum pressure
    simulation = wntr.sim.EpanetSimulator(wn)
#    simulation =  wntr.sim.WNTRSimulator(wn, mode='DD')
    # file_prefix impede erro 505 (salvador da patria)
    results = simulation.run_sim(file_prefix='tempPSO')
    pressures = results.node['pressure']
    minimun_pressure = 20.0
    sum_penalize = 0

    for column in pressures.columns:
        query_node = wn.get_node(column)
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
    

def prv_cost(x, costs):
    sum_prv_cost = list()
    i = 1
    for x_ in x:
        penalization = verify_pression(x_)
        cost = np.dot(x_, costs) + penalization
        sum_prv_cost.append(cost)
        print('Particle: ', i)
        print('\nCusto: ', cost)
        global actual_cost, actual_particle
        if cost < actual_cost:
            actual_cost = cost
            actual_particle = x_
            np.save('saves/cost_parcial01_kmeans.npy', cost)
            np.save('saves/particle_parcial01_kmeans.npy', x_)
        i += 1
    return np.array(sum_prv_cost)


# import prv costs
prv_costs = np.load('saves/prvs_cost_exnet_kmeans.npy')

# dimensions PSO
dimensions = prv_costs.shape[0]
# init_particle = np.load('saves/particle_parcial01_kmeans.npy').reshape(1,dimensions) 
init_particle = None

consts = 1
best_cost = 10000000
actual_cost = 10000000

for i in range(1):
    print('Hiperparametros atuais: ', consts)
    
    # hyperparamters PSO
    options = {'c1' : consts, 'c2' : consts, 'w' : consts, 'k' : 250, 'p' : 2}
    
    # instance PSO
    optimizer_discrete = ps.discrete.BinaryPSO(n_particles=250, dimensions=dimensions, options=options,  init_pos=init_particle)
    
    # realize optimization
    time_start = time.time()
    cost, pos = optimizer_discrete.optimize(prv_cost, iters=500, costs=prv_costs)
    
    '''# for test:
    particles = list()
    for i in range(1000):
        particle = [np.random.randint(0,2) for x in range(dimensions)]
        particles.append(np.array(particle))
    particles = np.array(particles)
    prv_cost(particles, prv_costs)'''
    time_end = time.time()
    print('Tempo de execução: ', time_end-time_start)
    if cost < best_cost:
        best_consts = consts
        best_cost = cost
    consts += 0.1 

np.save('saves/cost_pso_exnet_kmeans10.npy', cost)
np.save('saves/status_pso_exnet_kmeans10.npy', pos)

#particle_error = np.array([1,1,0,1,1,0,0,0,1,1,1,1,1,0,1,0,1,0,0,0,0,1,1,1,0,0,0,1,1,0,1,1,0,1,0,1,1,1,0,1,0,1,0,0,0,0,1,1,1,1,0,0,1,1,1,1,1,1,0,1,0,1])
#prv_cost(particle_error, prv_costs)
#for i in range(1000):
#    verify_pression(particle_error)
#    print(i+1)
