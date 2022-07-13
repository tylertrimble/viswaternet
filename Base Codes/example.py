# -*- coding: utf-8 -*-
"""
Example with CTown.inp showing first few functions
"""
import wdn_viz_003 as wdn
import matplotlib.pyplot as plt
import random
import numpy as np
import pandas as pd

#%%
#General Examples
model = wdn.initialize_model('CTown.inp')

wdn.create_basic_plot(model, savefig=True, saveName = 'Basic')

wdn.plot_distinct_nodes(model,parameter='elevation',binEdgeNum=5,savefig=True, legendTitle= 'Elevation Groups', saveName = 'ElevationMap')
wdn.plot_distinct_nodes(model,parameter='elevation',bins=[25,50,75,100,125,150],binSizeList = [100,125,150,175,200,225], binShapeList = ['.','v','8','D','1','p'], binBorderList=['b','k','y','b','k','y'],binBorderWidthList=[1,1.1,0.5,0.9,1,3],cmap=None,colorList=['#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'],savefig=True, legendTitle= 'Elevation Groups', saveName = 'ElevationMap2')
wdn.plot_distinct_nodes(model,parameter='pressure', timestep=3, binEdgeNum=5,savefig=True, legendTitle= 'Pressure at T', saveName = 'PressureMap')

wdn.plot_distinct_links(model,parameter='flowrate',timestep=5,pumps=False,bins=[-0.2,0.1,0.4,0.7,100],binEdgeNum=5,saveName="FlowRates")

wdn.plot_continuous_nodes(model,parameter='elevation',colorBarTitle="Elevation", saveName="ContinuousElevation")
wdn.plot_continuous_nodes(model,parameter='pressure',timestep=5,colorBarTitle="Elevation", saveName="ContinuousPressure")

wdn.plot_continuous_links(model,parameter='flowrate',timestep=11,pumps=False,cmap='bwr',colorBarTitle="Flowrate", saveName="ContinuousFlowrate")
#%%
#Special Labels
wdn.plot_distinct_nodes(model,parameter='elevation',binEdgeNum=5,savefig=True, legendTitle= 'Elevation Groups', saveName = 'ElevationMap')

wdn.draw_label(model,['label','not a label'],[-50,-70],[70,45],nodes=['J511','J411'])

#%%
#Plots red square with black outline at specific squares
wdn.plot_distinct_nodes(model,parameter='elevation',binEdgeNum=5,savefig=True, legendTitle= 'Elevation Groups', saveName = 'ElevationMapSpecial')

wdn.draw_nodes(model,['J511','J411'],nodeSize=300,nodeColor='r',nodeShape='s',edgeColors='k',lineWidths=2)

#%%
#Combination of distinct nodes + continuous links
fig, ax = plt.subplots(figsize=(15,25))

ax.set_facecolor((0.1, 0.1, 0.1))

parameterResults, nodeList = wdn.get_parameter(model, 'Node', 'demand', timestep=22)

binnedParameter, binNames = wdn.bin_parameter(model,parameterResults,5)

wdn.draw_distinct_nodes(model,ax,binnedParameter,binNames)

wdn.draw_base_elements(model,ax,links=False,pumps=False)

wdn.draw_legend(ax,binNames,'Demand')


parameterResults, linkList = wdn.get_parameter(model, 'Link', 'flowrate', timestep=22)

g = wdn.draw_links(model,linkList,parameterResults=parameterResults,cmap='bwr')

wdn.draw_color_bar(ax,g,'bwr',colorBarTitle='Flowrate')

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

wdn.save_fig(model, "Subplot")

#%%#Special data plotting with excel
model = wdn.initialize_model('NWC_old_stations.inp')

edge_list, bins = wdn.convert_excel(model,'NWC Pipes.xlsx',0,1)

wdn.plot_distinct_links(model,specialData=[edge_list,bins],savefig=True, legendTitle= 'Pipe Material', saveName = 'PipeMaterialMap')

edge_list, bins = wdn.convert_excel(model,'NWC Pipes.xlsx',0,2)

wdn.plot_distinct_links(model,specialData=[edge_list,bins],savefig=True, legendTitle= 'Pressure Zone', saveName = 'PressureZonesMap')

#%%
#Special numerical data

data = []
index = []

for node in model['node_names']:
    data.append(random.randint(0,100))
    index.append(node)
    
dataSeries = pd.Series(data=data, index=index)

binnedParameter, binNames = wdn.bin_parameter(model,dataSeries,5,binList='Automatic')

wdn.plot_distinct_nodes(model,specialData=[binnedParameter,binNames],savefig=True, legendTitle= 'Data', saveName = 'DataMap')

wdn.plot_continuous_nodes(model,specialData=[data,index],savefig=True, saveName = 'DataContMap')

#%%
#Animates pressure at all timesteps

#wdn.animate_plot(model, wdn.plot_distinct_nodes,figsize=[24,14],parameter='pressure',bins=[-25,0,25,50,75], binSizeList = [300,300,300,300,300,300],legendTitle= 'Pressure Groups', saveName = 'PresMap',savefig=False)