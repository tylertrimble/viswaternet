# -*- coding: utf-8 -*-
"""
Example with CTown.inp showing first few functions
"""
import wdn_viz_003 as wdn

model = wdn.initialize_model('CTown.inp')

wdn.create_basic_plot(model, savefig=True, saveName = 'Basic')
wdn.create_demand_pattern_plot(model, savefig=True, saveName = 'DemandPatterns')
wdn.plot_distinct_nodes(model,parameter='elevation',binNum=5,savefig=True, legendTitle= 'Elevation Groups', saveName = 'ElevationMap')
wdn.plot_distinct_nodes(model,parameter='elevation',bins=[25,50,75,100,125,150],binSizeList = [100,125,150,175,200,225], binShapeList = ['.','v','8','D','1','p'], cmap=None,colorList=['#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'],savefig=True, legendTitle= 'Elevation Groups', saveName = 'ElevationMap2')
wdn.plot_distinct_nodes(model,parameter='pressure', timestep=3, binNum=5,savefig=True, legendTitle= 'Pressure at T', saveName = 'PressureMap')
wdn.plot_continuous_nodes(model,parameter='elevation',colorBarTitle="Elevation", saveName="ContinuousElevation")
wdn.plot_continuous_nodes(model,parameter='pressure',timestep=55,colorBarTitle="Elevation", saveName="ContinuousPressure")
wdn.plot_distinct_links(model,parameter='flowrate',timestep=5,pumps=False,binWidthList=[2,2.5,3,3.5,4],cmap='Blues',binNum=5,saveName="FlowRates")
#%%
#model = wdn.initializeModel('NWC_old_stations.inp')
#wdn.plotDistinctNodes(model,specialData='Nodes_Pressure_Zones.xlsx',specialLegendTitle='Pressure Zones',savefig=True, saveName = 'Pressure Zones')