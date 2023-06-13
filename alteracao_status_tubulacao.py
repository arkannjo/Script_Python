# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 12:50:45 2020

@author: ength

Alteração dos status da tubulação
"""

import wntr
import numpy as np

WDS = wntr.network.WaterNetworkModel('redes/exnet_24hThyago.inp')
frontier_links = np.load('saves/frontier_links_exnet_kmedoids.npy')
status_frontier_links = np.load('saves/status_pso_exnet_kmedoids.npy')


for i in range(len(status_frontier_links)):
    if status_frontier_links[i] == 0:
       pipe = WDS.get_link(frontier_links[i]) 
       pipe.initial_status = 'Closed'
       
WDS.write_inpfile('redes/exnet_links_closed_kmedoids.inp')

