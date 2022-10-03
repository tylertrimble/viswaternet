import matplotlib.pyplot as plt
from PIL import Image
from wntr.epanet.util import *
import math
import matplotlib.ticker as ticker
import networkx.drawing.nx_pylab as nxp
import matplotlib.colors as mc
import matplotlib as mpl
from matplotlib.lines import Line2D
import seaborn as sns
import matplotlib.cm as cm
import wntr
import magnets as mg
import numpy as np
import networkx as nx
import scipy.sparse as sp
import pandas as pd
import random
from CTown_Error import *
import PIL
import glob
from numpy import sqrt
import matplotlib.image as mpimg
import glob
import os

# Define .INP file name
inp_file = 'test_networks/BWCN_true_INP.inp'
boundary_nodes = ['J332', 'J156', 'J421', 'J234','J251', 'J238', 'J1208', 'J87']
image_path = 'C:/Users/mst2245/Documents/Research/5. State Estimation/Python exercises/NWC/MAGNets/printed'


path = 'C:/Users/mst2245/Documents\Research/5. State Estimation/Python exercises/NWC/PNGs/'
# files = [f for f in glob.glob(path + "*.png")]
# files = [path+'Circle_around_six_radial_lines.png', path+'circle-with-diagonal-lines-icons-noun-project-699259.png']
files = [path+'pngwing.com.png', path+'circle-with-diagonal-lines-icons-noun-project-699259.png']

img = []
for f in files:
    img.append(mpimg.imread(f))
N = len(files)

# Run hydraulic simulation and store results
wn = wntr.network.WaterNetworkModel(inp_file)
sim = wntr.sim.EpanetSimulator(wn)
results = sim.run_sim()

unique_patterns = []
pattern_nodes = []
pattern_names = []
junc_list = []
dma_dict = {}
for junc_name, junction in wn.junctions():
    junc_list.append(junc_name)
    if junction.demand_timeseries_list[0].pattern != None:
        pattern_names.append(junction.demand_timeseries_list[0].pattern.name)
    else:
         pattern_names.append('None')

    if junction.demand_timeseries_list[0].pattern not in unique_patterns:
        unique_patterns.append(junction.demand_timeseries_list[0].pattern)
        pattern_nodes.append([])
        for j in range(len(unique_patterns)):
            if junction.demand_timeseries_list[0].pattern == unique_patterns[j]:
                pattern_nodes[j].append(junc_name)

# Make list of junctions in each DMA
# print(unique_patterns)
dma1 = []
dma2 = []
dma3 = []
dma4 = []
dma5 = []
dmanone = []
# print(unique_patterns)

for junc_name, junc in wn.junctions():
    if junc.demand_timeseries_list[0].pattern == unique_patterns[0]:
        dma2.append(junc_name)
    if junc.demand_timeseries_list[0].pattern == unique_patterns[1]:
        dma1.append(junc_name)  
    if junc.demand_timeseries_list[0].pattern == unique_patterns[2]:
        dmanone.append(junc_name)
    if junc.demand_timeseries_list[0].pattern == unique_patterns[3]:
        dma4.append(junc_name)
    if junc.demand_timeseries_list[0].pattern == unique_patterns[4]:
        dma5.append(junc_name)
    if junc.demand_timeseries_list[0].pattern == unique_patterns[5]:
        dma3.append(junc_name)

def ctown_plot(wn, name):
    # Play with demand patterns
    # unique_patterns = []
    # pattern_nodes = []
    # pattern_names = []
    # junc_list = []
    # dma_dict = {}
    # for junc_name, junction in wn.junctions():
    #     junc_list.append(junc_name)
    #     if junction.demand_timeseries_list[0].pattern != None:
    #         pattern_names.append(junction.demand_timeseries_list[0].pattern.name)
    #     else:
    #          pattern_names.append('None')
    
    #     if junction.demand_timeseries_list[0].pattern not in unique_patterns:
    #         unique_patterns.append(junction.demand_timeseries_list[0].pattern)
    #         pattern_nodes.append([])
    #         for j in range(len(unique_patterns)):
    #             if junction.demand_timeseries_list[0].pattern == unique_patterns[j]:
    #                 pattern_nodes[j].append(junc_name)
    
    # # print(wn.get_node(wn.junction_name_list[0]).demand_timeseries_list[0].pattern.name)
    
    # def unique(list1):
     
    #     # initialize a null list
    #     unique_list = []
         
    #     # traverse for all elements
    #     for x in list1:
    #         # check if exists in unique_list or not
    #         if x not in unique_list:
    #             unique_list.append(x)
    #     return unique_list
    
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
                   
    # Make list of junctions in each DMA
    # print(unique_patterns)
    dma1 = []
    dma2 = []
    dma3 = []
    dma4 = []
    dma5 = []
    dmanone = []
    
    # print(unique_patterns)
    for junc_name, junc in wn.junctions():
        if junc.demand_timeseries_list[0].pattern == unique_patterns[0]:
            dma2.append(junc_name)
        if junc.demand_timeseries_list[0].pattern == unique_patterns[1]:
            dma1.append(junc_name)  
        if junc.demand_timeseries_list[0].pattern == unique_patterns[2]:
            dmanone.append(junc_name)
        if junc.demand_timeseries_list[0].pattern == unique_patterns[3]:
            dma4.append(junc_name)
        if junc.demand_timeseries_list[0].pattern == unique_patterns[4]:
            dma5.append(junc_name)
        if junc.demand_timeseries_list[0].pattern == unique_patterns[5]:
            dma3.append(junc_name)
        
    print(dma1)
    zones = []
    materials = []
    zones_list = [ 'DMA1_pat', 'DMA2_pat', 'DMA3_pat', 'DMA4_pat', 'None', 'DMA5_pat']
    # zones_list = ['DMA2_pat', 'DMA1_pat', 'None', 'DMA4_pat', 'DMA5_pat', 'DMA3_pat']
    cmap = mpl.cm.get_cmap('gist_rainbow')
    cmap = mpl.cm.get_cmap('Greys')
    
    zone_col_ind = []
    zone_col = []
    
    for i in range(len(wn.junction_name_list)):
        # zone_col_ind.append(zones_list.index(zones[i]))
        zone_col.append(cmap(zones_list.index(pattern_names[i])/(len(zones_list)-1)))
    
    # Node legend labels
    custom_lines = [Line2D([], [], color = 'w', marker = 'o', markersize = 15, lw = 0),
                   Line2D([], [], color = 'w', marker = 'o', markersize = 15, lw = 0),
                   Line2D([], [], color = 'lightgrey', marker = 'o', markersize = 15, lw = 0),
                   Line2D([], [], color = 'dimgrey', marker = 'o', markersize = 15, lw = 0),
                   Line2D([], [], color = 'k', marker = 'o', markersize = 15, lw = 0),
                   Line2D([], [], color = 'w', marker = 'o', markersize = 15, lw = 0),
                   Line2D([], [], color = 'w', marker = 's', markersize = 15, lw = 0),
                   Line2D([], [], color = 'w', marker = 'h', markersize = 15, lw = 0)]
        
    leg_labels = ['DMA1', 'DMA2', 'DMA3', 'DMA4', 'DMA5', 'No DMA pattern', 'Source', 'Tank']
        
    leg_labels, custom_lines = zip(*sorted(zip(leg_labels, custom_lines), key=lambda t: t[0]))
    
    # Edge legend labels
    custom_lines2 = [Line2D([0], [0], color='k', lw = 2),
                     Line2D([0], [0], color='k', lw = 2, linestyle = 'dashed'),
                     Line2D([0], [0], color='k', lw = 2, linestyle = 'dotted')]
    leg_labels2 = ['Pipe', 'Pump','Valve']
    
    fig, ax = plt.subplots(figsize=(20,25))
    nxp.draw_networkx_nodes(G, pos_dict, node_size = 0, label = None)
    nxp.draw_networkx_nodes(G, pos_dict, nodelist = wn.tank_name_list, node_size = 500, node_color = 'k', node_shape = 'h')
    nxp.draw_networkx_nodes(G, pos_dict, nodelist = wn.reservoir_name_list, node_size = 500, node_color = 'k', node_shape = 's')
    nxp.draw_networkx_nodes(G, pos_dict, nodelist = wn.tank_name_list, node_size = 100, node_color = 'w', node_shape = 'h')
    nxp.draw_networkx_nodes(G, pos_dict, nodelist = wn.reservoir_name_list, node_size = 100, node_color = 'w', node_shape = 's')
    nxp.draw_networkx_nodes(G, pos_dict, nodelist = dmanone, node_size = 400, node_color = 'k')    
    nxp.draw_networkx_nodes(G, pos_dict, nodelist = dmanone, node_size = 300, node_color = 'w')
    nxp.draw_networkx_nodes(G, pos_dict, nodelist = dma5, node_color = 'k')
    nxp.draw_networkx_nodes(G, pos_dict, nodelist = dma3, node_color = 'lightgrey')
    nxp.draw_networkx_nodes(G, pos_dict, nodelist = dma4, node_color = 'dimgrey')
    nxp.draw_networkx_edges(G, pos_dict, edgelist = G_list_pipes_only, edge_color = 'k', width = 2, edge_cmap = cmap, arrows = None)
    g2 = nxp.draw_networkx_edges(G, pos_dict, edgelist = G_list_pumps_only, style = 'dashed', edge_color = 'k', label = 'Pump', width = 2,  arrows = None)
    g3 = nxp.draw_networkx_edges(G, pos_dict, edgelist = G_list_valves_only, style = 'dotted', edge_color = 'k', label = 'Valve', width = 2, arrows = None)
    nxp.draw_networkx_nodes(G, pos_dict, nodelist = dma1, node_color = 'w')
    nxp.draw_networkx_nodes(G, pos_dict, nodelist = dma2, node_color = 'w')
    plt.axis('off')
    ax=plt.gca()
    fig=plt.gcf()
    trans = ax.transData.transform
    trans2 = fig.transFigure.inverted().transform
    imsize = 0.017 # this is the image size
    for n in G.nodes():
        if n in dma2:
            (x,y) = pos_dict[n]
            xx,yy = trans((x,y)) # figure coordinates
            xa,ya = trans2((xx,yy)) # axes coordinates
            a = plt.axes([xa-imsize/2.0,ya-imsize/2.0, imsize, imsize ])
            a.imshow(img[0])
            a.set_aspect('equal')
            a.axis('off')
        if n in dma1:
            (x,y) = pos_dict[n]
            xx,yy = trans((x,y)) # figure coordinates
            xa,ya = trans2((xx,yy)) # axes coordinates
            a = plt.axes([xa-imsize/2.0,ya-imsize/2.0, imsize, imsize ])
            a.imshow(img[1])
            a.set_aspect('equal')
            a.axis('off')
    # nxp.draw_networkx_nodes(G, pos_dict, nodelist = dma2, node_size = 400, node_color = 'k')
    # g = nxp.draw_networkx_nodes(G, pos_dict, nodelist = junc_list, node_color = zone_col)
    # legend1 = ax.legend(custom_lines, leg_labels, title = 'Node', fontsize = '20', title_fontsize = '25', loc = 2)
    # legend2 = ax.legend(custom_lines2, leg_labels2, title = 'Link', fontsize = '20', title_fontsize = '25', loc = 3)
    # ax.add_artist(legend1)
    # ax.add_artist(legend2)
    fig.savefig(image_path+'/{}.pdf'.format(name))
    return 1

name = 'original'
# ctown_plot(wn, name)

inp_file3 = 'test_networks/ctown branches dma1dma3dma5 together.inp'
wn3 = wntr.network.WaterNetworkModel(inp_file3)
ctown_plot(wn3, 'dma1dma3dma5')
four_error(wn,wn3)
        

# In[] Branches removal + DMA1 and DMA3 k = 2 removal

wn2 = mg.reduction.reduce_model(inp_file, op_pt = 122, nodes_to_keep = boundary_nodes, max_nodal_degree = 1)
wn2.write_inpfile('test_networks/ctown branches.inp')
# ctown_plot(wn2, 'branched')
# four_error(wn,wn2)

sim2 = wntr.sim.EpanetSimulator(wn2)
results2 = sim2.run_sim()

# Determine which nodes remain in the reduced model
junc_names = wn2.junction_name_list
num_junc = len(junc_names)

# Plot percentage deviation of node heads in reduced model from original model over entire simulation duration
x_val = len(results2.node['head'].loc[:, junc_names[0]])
time_step = wn.options.time.report_timestep
mult_ts = 3600/time_step
x_old = np.linspace(0,(x_val-1)/mult_ts,x_val)
error = []
fig, ax = plt.subplots(figsize=(8,6))
error= []
for i in range(num_junc):
    error.append(((results2.node['head'].loc[:,junc_names[i]]
-results.node['head'].loc[:,junc_names[i]])/results.node['head'].loc[:,junc_names[i]])*100)
    ax.plot(x_old,error[i],label='Error Node {}'.format(junc_names[i]))
    ax.set_ylabel('Relative error [%]', fontsize = 14)
    ax.set_xlabel('Time [$hr$]', fontsize = 14)
fig.savefig(image_path+'/relative error only branches.pdf')

x = np.arange(125,152)
t7_head = results.node['head'].loc[125*time_step:151*time_step,'T2']
t7_head2 = results2.node['head'].loc[125*time_step:151*time_step,'T2']
pu2_flow = results.link['flowrate'].loc[125*time_step:151*time_step,'V2']
pu2_flow2 = results2.link['flowrate'].loc[125*time_step:151*time_step,'V2']

fig, ax = plt.subplots(2,1 , figsize=(8,10))
ax[0].plot(x, t7_head, 'k', label = 'Original model: T7')
ax[0].plot(x, t7_head2, 'k--', label = 'Reduced model: T7')
ax[0].axhline(y =  65+0.5, color = 'k', linewidth = 0.5)
ax[0].axhline(y = 65+5.5, color = 'k', linewidth = 0.5)
ax[0].set_ylabel('Node head [m]',fontsize = 14)
ax[0].text(130, 71, 'V2 closed above this level', fontsize = 14)
ax[0].text(130, 64.5, 'V2 open below this level', fontsize = 14)
ax[0].set_ylabel('Node head [$m$]', fontsize = 14)
ax[0].set_ylim([64, 72])
ax[1].plot(x,pu2_flow, color = 'k', label = 'Pump 9 original model')
ax[1].plot(x,pu2_flow2, 'k--', label = 'Pump 9 reduced model')
ax[1].set_ylabel('Flowrate [$m^3/s$]',fontsize=14)
ax[1].set_xlabel('Time [$hr$]',fontsize = 14)
fig.savefig(image_path+'/tank pump ctown branches.pdf')


# In[]

# Remove DMA1 and DMA3 k = 2
# inp_file2 = 'test_networks/ctown branches.inp'
# wn3 = mg.reduction.reduce_model(inp_file2, op_pt = 122, nodes_to_keep = dma4 + dma2 + dmanone + boundary_nodes, max_nodal_degree = 2)
# wn3.write_inpfile('test_networks/ctown branches dma1dma3dma5 together.inp')
# ctown_plot(wn3, 'dma1dma3dma5')
# four_error(wn,wn3)

# Identify errors
sim2 = wntr.sim.EpanetSimulator(wn3)
results2 = sim2.run_sim()

# Determine which nodes remain in the reduced model
junc_names = wn3.junction_name_list
num_junc = len(junc_names)

# Plot percentage deviation of node heads in reduced model from original model over entire simulation duration
x_val = len(results2.node['head'].loc[:, junc_names[0]])
time_step = wn.options.time.report_timestep
mult_ts = 3600/time_step
x_old = np.linspace(0,(x_val-1)/mult_ts,x_val)
error = []

max_error = []
prob_nodes = []
prob_nodes_g = []
nodes_error = []

plt.figure(figsize=(10,6))
for i in range(num_junc):
    error.append(abs((results.node['head'].loc[:,junc_names[i]]
-results2.node['head'].loc[:,junc_names[i]])/results.node['head'].loc[:,junc_names[i]])*100)
    max_error.append(np.amax(np.array(error)))
    nodes_error.append(np.max(np.array(error[i])))
                            
error_op_pt = np.argmax(max_error)

# Find nodes with largest error so we can retain them in the model
indices = np.argsort(nodes_error)
indlen = len(indices)
l1, l2, l3 = junc_names[indlen-1], junc_names[indlen-2], junc_names[indlen-3]
print(l1,l2,l3)

# Tank 7 flow
x = np.arange(50,77)
t7_head = results.node['head'].loc[50*time_step:76*time_step,'T1']
t7_head2 = results2.node['head'].loc[50*time_step:76*time_step,'T1']
pu2_flow = results.link['flowrate'].loc[50*time_step:76*time_step,'V2']
pu2_flow2 = results2.link['flowrate'].loc[50*time_step:76*time_step,'V2']
# fig, ax=plt.subplots(figsize = (10,12))
# plt.figure(2)
# plt.subplot(211)
# plt.plot(x, t7_head, label = 'Original model: T1')
# plt.plot(x, t7_head2, '--', label = 'Reduced model: T1')
# plt.axhline(y = 71.5 + 1, color = 'g')
# plt.axhline(y = 71.5 + 4.5, color = 'g')
# plt.ylabel('Head [m]')
# plt.legend()
# plt.title('CTown Model: Tank and Pump Comparison')
# plt.subplot(212)
# plt.plot(x, pu2_flow, label = 'Original model: PU2')
# plt.plot(x, pu2_flow2, '--', label = 'Reduced model: PU2')
# # plt.axhline(y = 102+1)
# # plt.axhline(y=102+3)
# plt.ylabel('Flow rate [m3/s]')
# plt.xlabel('Time [hr]')
# plt.legend()

# HEY THIS IS USEFUL FOR THE FUTURE WHEN YOU WANNA PLOT MULTIPLE PLOTS IN ONE

# fig = plt.figure(figsize=(18, 12))

# ax1 = plt.subplot2grid((2, 2), (0, 0), colspan=1, rowspan = 2)
# error = []
# for i in range(num_junc):
#     error.append(((results.node['head'].loc[:,junc_names[i]]
# -results2.node['head'].loc[:,junc_names[i]])/results.node['head'].loc[:,junc_names[i]])*100)
#     ax1.plot(x_old,error[i],label='Error Node {}'.format(junc_names[i]))
# ax1.set_ylabel('Relative error [%]', fontsize = 14)
# ax1.set_xlabel('Time [$hr$]', fontsize = 14)
# ax1.text(62, 5, 'Spike 1', fontsize = 14)
# ax1.text(40, -5, 'Spike 2', fontsize = 14)

fig, ax = plt.subplots(figsize=(8,6))
error= []
for i in range(num_junc):
    error.append(((results2.node['head'].loc[:,junc_names[i]]
-results.node['head'].loc[:,junc_names[i]])/results.node['head'].loc[:,junc_names[i]])*100)
    ax.plot(x_old,error[i],label='Error Node {}'.format(junc_names[i]))
    ax.set_ylabel('Relative error [%]', fontsize = 14)
    ax.set_xlabel('Time [$hr$]', fontsize = 14)
ax.text(70, 5, 'Spike 2', fontsize = 14)
ax.text(32, -6, 'Spike 1', fontsize = 14)
fig.savefig(image_path+'/relative error only.pdf')

fig, ax = plt.subplots(2,1 , figsize=(8,10))
ax[0].plot(x, t7_head, 'k', label = 'Original model: T7')
ax[0].plot(x, t7_head2, 'k--', label = 'Reduced model: T7')
ax[0].axhline(y =  65+0.5, color = 'k', linewidth = 0.5)
ax[0].axhline(y = 65+5.5, color = 'k', linewidth = 0.5)
ax[0].set_ylabel('Node head [m]',fontsize = 14)
ax[0].text(130, 71, 'V2 closed above this level', fontsize = 14)
ax[0].text(130, 65, 'V2 open below this level', fontsize = 14)
ax[0].set_ylabel('Node head [$m$]', fontsize = 14)
ax[0].set_ylim([64, 72])

ax[1].plot(x,pu2_flow, color = 'k', label = 'Pump 9 original model')
ax[1].plot(x,pu2_flow2, 'k--', label = 'Pump 9 reduced model')
ax[1].set_ylabel('Flowrate [$m^3/s$]',fontsize=14)
ax[1].set_xlabel('Time [$hr$]',fontsize = 14)
fig.savefig(image_path+'/tank pump ctown.pdf')


# fig, ax = plt.subplots(2,1,figsize = (10,6))
# ax2= plt.subplot2grid((2, 2), (0, 1), colspan=1)
# ax2.plot(x, t7_head, label = 'Original model: T7', color = 'k')
# ax2.plot(x, t7_head2, '--', label = 'Reduced model: T7', color = 'k')
# ax2.axhline(y = 71.5 + 1, color = 'k')
# ax2.axhline(y = 71.5 + 4.5, color = 'k')
# ax2.set_ylabel('Node head [$m$]', fontsize = 14)
# ax2.set_ylim([71, 77])
# ax2.text(60, 76.5, 'PU2 closed above this level', fontsize = 14)
# ax2.text(60, 71.5, 'PU2 open below this level', fontsize = 14)

# ax3 = plt.subplot2grid((2, 2), (1, 1), colspan=1)
# ax3.plot(x, pu2_flow, label = 'Original model: PU10', color = 'k')
# ax3.plot(x, pu2_flow2, '--', label = 'Reduced model: PU10', color = 'k')
# ax3.set_ylabel('Flowrate [$m^3/s$]', fontsize = 14)
# ax3.set_xlabel('Time [$hr$]', fontsize = 14)
# fig.savefig(image_path+'/tank pump ctown.pdf')


# In[] Branches removal + DMA1 + DMA3 k = 2 removal

# Remove DMA1 and DMA3 k = 2
# inp_file2 = 'test_networks/ctown branches.inp'
# wn3 = mg.reduction.reduce_model(inp_file2, op_pt = 122, nodes_to_keep = dma2 + dma3 + dma4 + dma5 + dmanone + boundary_nodes, max_nodal_degree = 2)
# wn3.write_inpfile('test_networks/ctown branches dma1.inp')
# ctown_plot(wn3)
# four_error(wn,wn3)

wn2 = mg.reduction.reduce_model(inp_file, op_pt = 122, nodes_to_keep = dma1 + dma3 + dma4 + dma5 + dmanone + boundary_nodes, max_nodal_degree = None)
# wn2.write_inpfile('test_networks/ctown dma2.inp')

ctown_plot(wn2, 'dma2only')
# four_error(wn,wn2)
sim2 = wntr.sim.EpanetSimulator(wn2)
results2 = sim2.run_sim()
junc_names = wn2.junction_name_list
num_junc = len(junc_names)

fig, ax = plt.subplots(figsize=(8,6))
error= []
for i in range(num_junc):
    error.append(((results2.node['head'].loc[:,junc_names[i]]
-results.node['head'].loc[:,junc_names[i]])/results.node['head'].loc[:,junc_names[i]])*100)
    ax.plot(x_old,error[i],label='Error Node {}'.format(junc_names[i]))
    ax.set_ylabel('Relative error [%]', fontsize = 14)
    ax.set_xlabel('Time [$hr$]', fontsize = 14)
# ax.text(70, 5, 'Spike 2', fontsize = 14)
# ax.text(32, -6, 'Spike 1', fontsize = 14)
fig.savefig(image_path+'/relative error only dma2.pdf')
# In[] Use existing dma 1 inp!!!

# # Remove DMA3 k = 2
# inp_file3 = 'test_networks/ctown branches dma1 ed.inp'
# wn4 = mg.reduction.reduce_model(inp_file3, op_pt = 122, nodes_to_keep = dma2 + dma4 + dma3 + dma1 + dmanone + boundary_nodes, max_nodal_degree = 2)
# wn4.write_inpfile('test_networks/ctown branches dma1 dma5.inp')
# ctown_plot(wn4)
# four_error(wn,wn4)

# # Remove DMA3 k = 2
# inp_file4 = 'test_networks/ctown branches dma1 dma3.inp'
# wn5 = mg.reduction.reduce_model(inp_file4, op_pt = 122, nodes_to_keep = dma2 + dma4 + dmanone + boundary_nodes, max_nodal_degree = 2)
# wn5.write_inpfile('test_networks/ctown branches dma1 dma3 dma5.inp')
# ctown_plot(wn5)
# four_error(wn,wn5)

# # Identify errors
# sim2 = wntr.sim.EpanetSimulator(wn4)
# results2 = sim2.run_sim()

# # Determine which nodes remain in the reduced model
# junc_names = wn4.junction_name_list
# num_junc = len(junc_names)

# x = np.arange(50,77)
# t7_head = results.node['head'].loc[50*time_step:76*time_step,'T1']
# t7_head2 = results2.node['head'].loc[50*time_step:76*time_step,'T1']
# pu2_flow = results.link['flowrate'].loc[50*time_step:76*time_step,'PU2']
# pu2_flow2 = results2.link['flowrate'].loc[50*time_step:76*time_step,'PU2']
# fig, ax=plt.subplots(figsize = (10,12))
# # plt.figure(2)
# plt.subplot(211)
# plt.plot(x, t7_head, label = 'Original model: T1')
# plt.plot(x, t7_head2, '--', label = 'Reduced model: T1')
# plt.axhline(y = 71.5 + 1, color = 'g')
# plt.axhline(y = 71.5 + 4.5, color = 'g')
# plt.ylabel('Head [m]')
# plt.legend()
# plt.title('CTown Model: Tank and Pump Comparison')
# plt.subplot(212)
# plt.plot(x, pu2_flow, label = 'Original model: PU2')
# plt.plot(x, pu2_flow2, '--', label = 'Reduced model: PU2')
# # plt.axhline(y = 102+1)
# # plt.axhline(y=102+3)
# plt.ylabel('Flow rate [m3/s]')
# plt.xlabel('Time [hr]')
# plt.legend()

# # In[] Analysis of weird results

# sim2 = wntr.sim.EpanetSimulator(wn4)
# results2 = sim2.run_sim()

# # Determine which nodes remain in the reduced model
# junc_names = wn4.junction_name_list
# num_junc = len(junc_names)

# # Plot percentage deviation of node heads in reduced model from original model over entire simulation duration
# x_val = len(results2.node['head'].loc[:, junc_names[0]])
# time_step = wn.options.time.report_timestep
# mult_ts = 3600/time_step
# x = np.linspace(0,(x_val-1)/mult_ts,x_val)
# error = []

# max_error = []
# prob_nodes = []
# prob_nodes_g = []
# nodes_error = []

# plt.figure(figsize=(10,6))
# for i in range(num_junc):
#     error.append(abs((results.node['head'].loc[:,junc_names[i]]
# -results2.node['head'].loc[:,junc_names[i]])/results.node['head'].loc[:,junc_names[i]])*100)
#     max_error.append(np.amax(np.array(error)))
#     nodes_error.append(np.max(np.array(error[i])))
                            
# error_op_pt = np.argmax(max_error)

# # Find nodes with largest error so we can retain them in the model
# indices = np.argsort(nodes_error)
# print(nodes_error)
# print(results2.node['head'].loc[:,'J511'])
# indlen = len(indices)
# l1, l2, l3 = junc_names[indlen-1], junc_names[indlen-2], junc_names[indlen-3]
# print(l1,l2,l3)

# error_org = []
# error_red = []
# fig7, ax7 = plt.subplots(figsize=(10,6))
# error_org.append(results.node['head'].loc[:,'J511'])
# error_red.append(results2.node['head'].loc[:,'J511'])
# plt.plot(x,error_org[0],label='Original model')
# plt.plot(x,error_red[0],'--', label='Reduced model')
# plt.legend()
# plt.title('Comparison of heads for node J511 in C-Town')
# plt.xlabel('Time [hours]')
# plt.ylabel('Head [m]')

# # In[] Compare dma1dma3 and dma1 dma3

