# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 15:18:02 2020

@author: ength

Perfomance indices for WDS sectorization 
"""

import wntr
import numpy as np


def pressure_uniformity(junctions, pressure):
    # index Pressure Uniformity
    time = pressure.index
    requiredPressure = 20
    sumPressures1= 0
    sumPressures2= 0
    pressureUniformity = 0
    
    for j in time:
        averagePressure = pressure.loc[j].mean()
        for i in junctions:
            sumPressures1 = sumPressures1 + ((pressure.loc[j][i] - requiredPressure) / requiredPressure)
            sumPressures2 = sumPressures2 + ((pressure.loc[j][i] - averagePressure) ** 2 / len(junctions))
        pressureUniformity = pressureUniformity + (sumPressures1 / len(junctions)) + (np.sqrt(sumPressures2) / averagePressure)
    return pressureUniformity
    


# read original WDS
inpOriginal = 'redes/exnet_24hThyago.inp'
networkOriginal = wntr.network.WaterNetworkModel(inpOriginal)

#simulate original WDS
simulationOriginal = wntr.sim.EpanetSimulator(networkOriginal)
resultsOriginal = simulationOriginal.run_sim()

headOriginal = resultsOriginal.node['head']
pressureOriginal = resultsOriginal.node['pressure']
demandOriginal = resultsOriginal.node['demand']
flowrateOriginal = resultsOriginal.link['flowrate']

# read sectorized WDS
inpSectorized = 'redes/exnet_24hThyago_controls_hierarquico.inp'
networkSectorized= wntr.network.WaterNetworkModel(inpSectorized)

#simulate sectorized WDS
simulationSectorized = wntr.sim.EpanetSimulator(networkSectorized)
resultsSectorized = simulationSectorized.run_sim()

headSectorized = resultsSectorized.node['head']
pressureSectorized = resultsSectorized.node['pressure']
demandSectorized = resultsSectorized.node['demand']
flowrateSectorized = resultsSectorized.link['flowrate']

# performances index original WDS
resilience_indexOriginal = wntr.metrics.todini_index(headOriginal,pressureOriginal,
                                                     demandOriginal,flowrateOriginal,networkOriginal, 20)

# performances index sectorized WDS
resilience_indexSectorized = wntr.metrics.todini_index(headSectorized,pressureSectorized,
                                                     demandSectorized,flowrateSectorized,networkSectorized, 20)

# Junctions with positive demand original network
positiveDemandJunctionsOriginal = networkOriginal.query_node_attribute('base_demand', np.greater, 0,
                                                               node_type=wntr.network.model.Junction)
namesPositiveDemandJunctionsOriginal = positiveDemandJunctionsOriginal.keys().values

pressureUniformityOriginal = pressure_uniformity(namesPositiveDemandJunctionsOriginal, pressureOriginal)

# Junctions with positive demand sectorized network
positiveDemandJunctionsSectorized = networkSectorized.query_node_attribute('base_demand', np.greater, 0,
                                                               node_type=wntr.network.model.Junction)
namesPositiveDemandJunctionsSectorized = positiveDemandJunctionsSectorized.keys().values

pressureUniformitySectorized = pressure_uniformity(namesPositiveDemandJunctionsSectorized, pressureSectorized)
