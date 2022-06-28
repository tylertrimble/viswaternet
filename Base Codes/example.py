# -*- coding: utf-8 -*-
"""
Example with CTown.inp showing first few functions
"""
import wdn_viz_003 as wdn

model = wdn.initializeModel('CTown.inp')

wdn.createBasicPlot(model, savefig=True, saveName = 'Basic')
wdn.createDemandPatternPlot(model, savefig=True, saveName = 'DemandPatterns')
wdn.plotDistinctNodes(model,parameter='elevation',binNum=5,savefig=True, legendTitle= 'Elevation Groups', saveName = 'ElevationMap')
wdn.plotDistinctNodes(model,parameter='elevation',bins=[25,50,75,100,125,150],binSizeList = [100,125,150,175,200,225], binShapeList = ['.','v','8','D','1','p'], cmap=None,colorList=['#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'],savefig=True, legendTitle= 'Elevation Groups', saveName = 'ElevationMap2')
wdn.plotDistinctNodes(model,parameter='pressure', timestep=3, binNum=5,savefig=True, legendTitle= 'Pressure at T', saveName = 'PressureMap')
wdn.plotContinuousNodes(model,parameter='elevation',colorBarTitle="Elevation", saveName="ContinuousElevation")
wdn.plotContinuousNodes(model,parameter='pressure',timestep=55,colorBarTitle="Elevation", saveName="ContinuousPressure")
wdn.plotDistinctLinks(model,parameter='flowrate',timestep=5,pumps=False,binWidthList=[2,2.5,3,3.5,4],cmap='Blues',binNum=5,saveName="FlowRates")
#%%
#model = wdn.initializeModel('NWC_old_stations.inp')
#wdn.plotDistinctNodes(model,specialData='Nodes_Pressure_Zones.xlsx',specialLegendTitle='Pressure Zones',savefig=True, saveName = 'Pressure Zones')