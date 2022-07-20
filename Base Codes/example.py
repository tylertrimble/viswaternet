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
model = wdn.initialize_model('NWC_old_stations.inp')

#%%
fig, ax = plt.subplots(figsize=(15,25))
aaa = wdn.plot_unique_data(model,fig,ax,parameter='diameter',cmap='tab20')
#%%
fig, ax = plt.subplots(figsize=(15,25))
wdn.plot_continuous_links(model,fig,ax,parameter='flowrate',value='MEAN',minWidth=1,maxWidth=3,pumps=False,saveName="FlowRates",cmap='BuGn')
#%%

#%%
#Special Labels
fig, ax = plt.subplots(figsize=(15,25))

wdn.plot_distinct_nodes(model,fig,ax,parameter='elevation',binEdgeNum=5,savefig=True, legendTitle= 'Elevation Groups', saveName = 'ElevationMap')
print(model['wn'].get_node('100019').coordinates[1])
wdn.draw_label(model,ax,['label','not a label'],[0.5,0.3],[0.1,0.7])

#%%
#Plots red square with black outline at specific squares
wdn.plot_distinct_nodes(model,parameter='elevation',binEdgeNum=5,savefig=True, legendTitle= 'Elevation Groups', saveName = 'ElevationMapSpecial')

wdn.draw_nodes(model,['J511','J411'],nodeSize=300,nodeColor='r',nodeShape='s',edgeColors='k',lineWidths=2)

#%%
#Combination of distinct nodes + continuous links
fig, ax = plt.subplots(figsize=(15,25))

wdn.plot_distinct_nodes(model,fig,ax,parameter='elevation',binEdgeNum=5,savefig=True, legendTitle= 'Elevation Groups', saveName = 'ElevationMap')

wdn.plot_continuous_links(model,fig,ax,parameter='flowrate',timestep=11,pumps=False,cmap='bwr',colorBarTitle="Flowrate", saveName="ContinuousFlowrate")

#%%
#Subplots. Plots pressure at two different timesteps

fig, (ax1,ax2) = plt.subplots(nrows=1, ncols=2,figsize=(15,25),sharex=True,sharey=True)

wdn.plot_distinct_nodes(model,fig,ax1,parameter='elevation',binEdgeNum=5,savefig=True, legendTitle= 'Elevation Groups', saveName = 'ElevationMap')

wdn.plot_continuous_links(model,fig,ax2,parameter='flowrate',value=11,pumps=False,cmap='bwr',colorBarTitle="Flowrate", saveName="ContinuousFlowrate")
#%%#Special data plotting with excel
model = wdn.initialize_model('NWC_old_stations.inp')
#%%
fig, ax = plt.subplots(figsize=(15,25))
wdn.plot_unique_data(model,ax,parameter='NWC Pipes.xlsx',parameterType='Link',dataType='Continuous',value=[0,3],cmap='autumn')

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
fig, ax = plt.subplots(figsize=(15,25))
#Plots demand patterns
wdn.plot_unique_data(model,ax,parameter='demand patterns')
#%%
#Animates pressure at all timesteps

#wdn.animate_plot(model, wdn.plot_distinct_nodes,figsize=[24,14],parameter='pressure',bins=[-25,0,25,50,75], binSizeList = [300,300,300,300,300,300],legendTitle= 'Pressure Groups', saveName = 'PresMap',savefig=False)