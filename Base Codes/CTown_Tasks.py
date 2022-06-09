# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 15:07:22 2022

@author: Tyler
"""

import wntr
import networkx as nx
import numpy as np
import scipy.sparse as sp
import matplotlib.pyplot as plt
from wntr.epanet.util import *
import networkx.drawing.nx_pylab as nxp
import matplotlib.colors as mc
import matplotlib as mpl
from matplotlib.lines import Line2D
import matplotlib.cm as cm
import matplotlib.patches as mpatches
import os
import pandas as pd


# Define .INP file name
dirname = os.path.dirname(__file__)
inp_file = os.path.join(dirname, 'Networks', 'Net3.inp')
image_path = os.path.join(dirname, 'Images')
# Run hydraulic simulation and store results
wn = wntr.network.WaterNetworkModel(inp_file)
sim = wntr.sim.EpanetSimulator(wn)
results = sim.run_sim()

# Create name lists for easy reference
junc_names = wn.junction_name_list
valve_names = wn.valve_name_list
tank_names = wn.tank_name_list
node_names = wn.node_name_list
   
#find incidence matrix and A21 matrix
pipe_tp =[]
pipe_tp2 = []

for pipe_name, link in wn.pipes():
    pipe_tp.append(link.start_node_name)
    pipe_tp2.append(link.end_node_name)
pipe_list = list(zip(pipe_tp, pipe_tp2))

pipe_tp =[]
pipe_tp2 = []

for pump_name, link in wn.pumps():
    pipe_tp.append(link.start_node_name)
    pipe_tp2.append(link.end_node_name)
pump_list = list(zip(pipe_tp, pipe_tp2))

pipe_tp =[]
pipe_tp2 = []

for valve_name, link in wn.valves():
    pipe_tp.append(link.start_node_name)
    pipe_tp2.append(link.end_node_name)
valve_list = list(zip(pipe_tp, pipe_tp2))

pipe_tp =[]
pipe_tp2 = []

for link_name, link in wn.links():
    pipe_tp.append(link.start_node_name)
    pipe_tp2.append(link.end_node_name)
new_pipes_list = list(zip(pipe_tp, pipe_tp2))


# Time configuration 
x_val = len(results.node['head'].loc[:, junc_names[0]])
time_step = wn.options.time.report_timestep
mult_ts = 3600/time_step
x = np.linspace(0,(x_val-1)/mult_ts,x_val)

G = wn.get_graph()
G_edge_list = list(G.edges())
inc_mat = sp.csr_matrix.toarray(nx.incidence_matrix(G,nodelist = node_names, oriented=True))
inc_mat_no = sp.csr_matrix.toarray(nx.incidence_matrix(G,nodelist = node_names, edgelist = new_pipes_list, oriented=False))
adj_mat = sp.csr_matrix.toarray(nx.adjacency_matrix(G,nodelist = node_names))

pos_dict = {}
for i in range(len(node_names)):
    pos_dict[node_names[i]] = wn.get_node(node_names[i]).coordinates

G_pipe_name_list = []
G_list_pipes_only = []
G_list_pumps_only = []
G_list_valves_only = []
G_pipe_index = []
pipe_list_names = []
for i in range(len(G_edge_list)):
    for j in range(len(pipe_tp)):
        if (G_edge_list[i][0] == pipe_tp[j] and G_edge_list[i][1] == pipe_tp2[j]) or (G_edge_list[i][1] == pipe_tp[j] and G_edge_list[i][0] == pipe_tp2[j]):
            G_pipe_name_list.append(wn.link_name_list[j])
            G_pipe_index.append(j)
            if wn.link_name_list[j] in wn.pipe_name_list:
                G_list_pipes_only.append(G_edge_list[i])
                pipe_list_names.append(wn.link_name_list[j])
            if wn.link_name_list[j] in wn.pump_name_list:
                G_list_pumps_only.append(G_edge_list[i])
            if wn.link_name_list[j] in wn.valve_name_list:
                G_list_valves_only.append(G_edge_list[i])
                
spl_nodes = []
spl_nodes_dict = {}
for tank_name, tank in wn.tanks():
    # spl_nodes.append(tank_name)
    spl_nodes_dict[tank_name] = tank_name
    
for res_name, res in wn.reservoirs():
    # spl_nodes.append(res_name)
    spl_nodes_dict[res_name] = res_name


for i in range(len(spl_nodes)):
    spl_nodes_dict[spl_nodes[i]] = spl_nodes[i]

fig, ax = plt.subplots(figsize=(15,25))
nxp.draw_networkx_nodes(G, pos_dict, node_size = 30, node_color = 'k')
nxp.draw_networkx_nodes(G, pos_dict, nodelist = wn.reservoir_name_list, node_size = 200, node_color = 'black',linewidths=3,node_shape = 's')
nxp.draw_networkx_nodes(G, pos_dict, nodelist = wn.tank_name_list, node_size = 200, node_color = 'black',linewidths=3, node_shape = 'd')
nxp.draw_networkx_edges(G, pos_dict, arrows = False, edge_color = 'k')
plt.savefig(image_path+'/EPANET-Lookalike.png') 


# %%

import wntr
import networkx as nx
import numpy as np
import scipy.sparse as sp
import matplotlib.pyplot as plt
from wntr.epanet.util import *
import networkx.drawing.nx_pylab as nxp
import matplotlib.colors as mc
import matplotlib as mpl
from matplotlib.lines import Line2D
import matplotlib.cm as cm
import matplotlib.patches as mpatches
import os
import pandas as pd

def patternMatch(nodePattern,pattern, junc_name,demandPatternNodes):
    if nodePattern == pattern:
        demandPatternNodes[pattern][junc_name] = junc_name
    return demandPatternNodes
def createDemandPatternPlot(inp_file):
    dirname = os.path.dirname(__file__)
    inp_file = os.path.join(dirname, 'Networks', inp_file)
    image_path = os.path.join(dirname, 'Images')
    
    # Run hydraulic simulation and store results
    wn = wntr.network.WaterNetworkModel(inp_file)
    sim = wntr.sim.EpanetSimulator(wn)
    results = sim.run_sim()
    
    # Create name lists for easy reference
    junc_names = wn.junction_name_list
    valve_names = wn.valve_name_list
    tank_names = wn.tank_name_list
    node_names = wn.node_name_list
       
    #find incidence matrix and A21 matrix
    pipe_tp =[]
    pipe_tp2 = []
    
    for pipe_name, link in wn.pipes():
        pipe_tp.append(link.start_node_name)
        pipe_tp2.append(link.end_node_name)
    pipe_list = list(zip(pipe_tp, pipe_tp2))
    
    pipe_tp =[]
    pipe_tp2 = []
    
    for pump_name, link in wn.pumps():
        pipe_tp.append(link.start_node_name)
        pipe_tp2.append(link.end_node_name)
    pump_list = list(zip(pipe_tp, pipe_tp2))
    
    pipe_tp =[]
    pipe_tp2 = []
    
    for valve_name, link in wn.valves():
        pipe_tp.append(link.start_node_name)
        pipe_tp2.append(link.end_node_name)
    valve_list = list(zip(pipe_tp, pipe_tp2))
    
    pipe_tp =[]
    pipe_tp2 = []
    
    for link_name, link in wn.links():
        pipe_tp.append(link.start_node_name)
        pipe_tp2.append(link.end_node_name)
    new_pipes_list = list(zip(pipe_tp, pipe_tp2))
    
    
    # Time configuration 
    x_val = len(results.node['head'].loc[:, junc_names[0]])
    time_step = wn.options.time.report_timestep
    mult_ts = 3600/time_step
    x = np.linspace(0,(x_val-1)/mult_ts,x_val)
    
    G = wn.get_graph()
    G_edge_list = list(G.edges())
    inc_mat = sp.csr_matrix.toarray(nx.incidence_matrix(G,nodelist = node_names, oriented=True))
    inc_mat_no = sp.csr_matrix.toarray(nx.incidence_matrix(G,nodelist = node_names, edgelist = new_pipes_list, oriented=False))
    adj_mat = sp.csr_matrix.toarray(nx.adjacency_matrix(G,nodelist = node_names))
    
    pos_dict = {}
    for i in range(len(node_names)):
        pos_dict[node_names[i]] = wn.get_node(node_names[i]).coordinates
    
    G_pipe_name_list = []
    G_list_pipes_only = []
    G_list_pumps_only = []
    G_list_valves_only = []
    G_pipe_index = []
    pipe_list_names = []
    for i in range(len(G_edge_list)):
        for j in range(len(pipe_tp)):
            if (G_edge_list[i][0] == pipe_tp[j] and G_edge_list[i][1] == pipe_tp2[j]) or (G_edge_list[i][1] == pipe_tp[j] and G_edge_list[i][0] == pipe_tp2[j]):
                G_pipe_name_list.append(wn.link_name_list[j])
                G_pipe_index.append(j)
                if wn.link_name_list[j] in wn.pipe_name_list:
                    G_list_pipes_only.append(G_edge_list[i])
                    pipe_list_names.append(wn.link_name_list[j])
                if wn.link_name_list[j] in wn.pump_name_list:
                    G_list_pumps_only.append(G_edge_list[i])
                if wn.link_name_list[j] in wn.valve_name_list:
                    G_list_valves_only.append(G_edge_list[i])
                    
    spl_nodes = []
    spl_nodes_dict = {}
    for tank_name, tank in wn.tanks():
        # spl_nodes.append(tank_name)
        spl_nodes_dict[tank_name] = tank_name
        
    for res_name, res in wn.reservoirs():
        # spl_nodes.append(res_name)
        spl_nodes_dict[res_name] = res_name
    
    
    for i in range(len(spl_nodes)):
        spl_nodes_dict[spl_nodes[i]] = spl_nodes[i]
        
    cmap = mpl.cm.get_cmap('tab10')
    valve_coordinates = {}
    valveCounter = 0
    for point1, point2 in G_list_valves_only:
        midpoint = [(wn.get_node(point1).coordinates[0] + wn.get_node(point2).coordinates[0])/2,(wn.get_node(point1).coordinates[1] + wn.get_node(point2).coordinates[1])/2]
        valve_coordinates[valve_names[valveCounter]] = midpoint
        valveCounter += 1
    fig, ax = plt.subplots(figsize=(15,25))
    demandPatterns = []
    patterns = wn.pattern_name_list
    patterns = np.append(patterns, 'None')
    for junction in junc_names:
        try:
            demandPattern = wn.get_node(junction).demand_timeseries_list[0].pattern.name
            demandPatterns = np.append(demandPatterns, demandPattern)
        except AttributeError:
            demandPatterns = np.append(demandPatterns, 'None')
    demandPatternNodes = {}
    for pattern in patterns:
        demandPatternNodes[pattern] = {}
        
    for i in range(len(junc_names)):
        for pattern in patterns:
            demandPatternNodes = patternMatch(demandPatterns[i],pattern,junc_names[i],demandPatternNodes)

    if len(demandPatternNodes['None']) == 0:
        patterns = np.delete(patterns,len(patterns)-1)
        del demandPatternNodes['None']
         
    cmapValue = 1/6
    
    for pattern in patterns:
        nxp.draw_networkx_nodes(G, pos_dict, nodelist = demandPatternNodes.get(pattern).values(), node_size = 100, node_color = cmap(float(cmapValue)))
        cmapValue += 1/6
        
    nxp.draw_networkx_nodes(G, pos_dict, nodelist = wn.reservoir_name_list, node_size = 200, node_color = 'white', edgecolors='red',linewidths=3,node_shape = 's', label="Resevoir")
    nxp.draw_networkx_nodes(G, pos_dict, nodelist = wn.tank_name_list, node_size = 200, node_color = 'white', edgecolors='blue',linewidths=3, node_shape = 's', label="Tanks")
    nxp.draw_networkx_nodes(G, valve_coordinates, nodelist = valve_names, node_size = 200, node_color = 'orange', edgecolors='black',linewidths=1,node_shape = 'P', label="Valves")
    
    nxp.draw_networkx_edges(G, pos_dict, edgelist = G_list_pumps_only, node_size = 200, edge_color = 'b', width=3)
    
    patch1 = mpatches.Patch(color='blue', label='Pumps')
    patch2 = mpatches.Patch(color='black', label='Pipes')
    nxp.draw_networkx_edges(G, pos_dict, arrows = False, edge_color = 'k')
    
    handles, labels = ax.get_legend_handles_labels()
    handles.extend([patch1,patch2])
    
    legend1 = plt.legend(title='Demand Patterns',labels=patterns, loc='lower right',fontsize = '15', title_fontsize = '17')
    legend2 = plt.legend(title='Node Types', handles=handles, loc='upper right',fontsize = '15', title_fontsize = '17')
    ax.add_artist(legend1)
    ax.add_artist(legend2)
    if inp_file.endswith('.inp'):
        prefixRemove = len(image_path) + 3
        inp_file = inp_file[prefixRemove:-4]
    image_path2 = '/DemandPatterns' + inp_file + '.png'
    plt.savefig(image_path+image_path2) 
    
createDemandPatternPlot('Net3.inp')