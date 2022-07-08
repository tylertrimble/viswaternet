# -*- coding: utf-8 -*-
"""
Example with CTown.inp showing first few functions
"""
import wdn_viz_003 as wdn
import matplotlib.pyplot as plt
model = wdn.initialize_model('CTown.inp')
#%%
# wdn.create_basic_plot(model, savefig=True, saveName = 'Basic')
# wdn.create_demand_pattern_plot(model, savefig=True, saveName = 'DemandPatterns')
# wdn.plot_distinct_nodes(model,parameter='elevation',binEdgeNum=5,savefig=True, legendTitle= 'Elevation Groups', saveName = 'ElevationMap')

# wdn.plot_distinct_nodes(model,parameter='elevation',bins=[25,50,75,100,125,150],binSizeList = [100,125,150,175,200,225], binShapeList = ['.','v','8','D','1','p'], binBorderList=['b','k','y','b','k','y'],binBorderWidthList=[1,1.1,0.5,0.9,1,3],cmap=None,colorList=['#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'],savefig=True, legendTitle= 'Elevation Groups', saveName = 'ElevationMap2')
# wdn.plot_continuous_links(model,parameter='flowrate',timestep=11,pumps=False,colorBarTitle="Flowrate", saveName="ContinuousFlowrate")
# wdn.plot_distinct_nodes(model,parameter='pressure', timestep=3, binEdgeNum=5,savefig=True, legendTitle= 'Pressure at T', saveName = 'PressureMap')
# wdn.plot_continuous_nodes(model,parameter='elevation',colorBarTitle="Elevation", saveName="ContinuousElevation")
# wdn.plot_continuous_nodes(model,parameter='pressure',timestep=5,colorBarTitle="Elevation", saveName="ContinuousPressure")
# wdn.plot_distinct_links(model,parameter='flowrate',timestep=5,pumps=False,bins=[-0.2,0.1,0.4,0.7,100],binEdgeNum=5,saveName="FlowRates")

#%%
#Animates pressure at all timesteps

wdn.animate_plot(model, wdn.plot_distinct_nodes,figsize=[24,14],parameter='pressure',bins=[-25,0,25,50,75], binSizeList = [300,300,300,300,300,300],legendTitle= 'Pressure Groups', saveName = 'PresMap',savefig=False)

#%%

#Plots red square with black outline at specific squares
wdn.plot_distinct_nodes(model,parameter='elevation',binEdgeNum=5,savefig=True, legendTitle= 'Elevation Groups', saveName = 'ElevationMap')
wdn.draw_nodes(model,['J511','J411'],nodeSize=300,nodeColor='r',nodeShape='s',edgeColors='k',lineWidths=2)

#%%
#Subplots. Plots pressure at two different timesteps

fig, (ax1,ax2) = plt.subplots(nrows=1, ncols=2,figsize=(15,25),sharex=True,sharey=True)
parameterResults, nodeList = wdn.get_parameter(model,'Node','pressure',timestep=5)

binnedResults,binNames = wdn.bin_parameter(model,parameterResults, 5) 

wdn.draw_distinct_nodes(model,ax1,binnedResults,binNames,cmap='tab10')

wdn.draw_base_elements(model,ax1)

wdn.draw_legend(ax1,binNames)



parameterResults2, nodeList2 = wdn.get_parameter(model,'Node','pressure',timestep=55)

binnedResults2,binNames2 = wdn.bin_parameter(model,parameterResults2, 5) 

wdn.draw_distinct_nodes(model,ax2,binnedResults2,binNames2,cmap='tab10')

wdn.draw_base_elements(model,ax2)

wdn.draw_legend(ax2,binNames)

plt.show()