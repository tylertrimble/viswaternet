# -*- coding: utf-8 -*-
"""
Created on Fri Jun  3 13:55:37 2022

@author: Tyler
"""

# Import libraries
import wntr
import networkx as nx
import numpy as np
import scipy.sparse as sp
import pandas as pd
import matplotlib.pyplot as plt
import networkx.drawing.nx_pylab as nxp
import matplotlib.colors as mc
import matplotlib as mpl
from matplotlib.lines import Line2D
import matplotlib.cm as cm

# Define .INP file name
inp_file = 'NWC_new_stations.inp'

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

image_path = "C:/Users/mst2245/Documents/Research/5. State Estimation/Python exercises/NWC/Images"

def plot_spl_elements():
    nxp.draw_networkx_nodes(G, pos_dict, nodelist = wn.reservoir_name_list, node_size = 200, node_color = 'k', node_shape = 's')
    nxp.draw_networkx_nodes(G, pos_dict, nodelist = wn.tank_name_list, node_size = 200, node_color = 'b', node_shape = 'h')
    nxp.draw_networkx_nodes(G, pos_dict, nodelist = spl_nodes, node_size = 150, node_color = 'r')
    # nxp.draw_networkx_nodes(G, pos_dict, nodelist = spl_nodes, node_size = 50, node_color = 'white')    
    plt.text(wn.get_node('AM9001').coordinates[0]-500,wn.get_node('AM9001').coordinates[1],s = 'Anderson Mill R + T + PS', bbox=dict(facecolor='mediumaquamarine', alpha=0.9, edgecolor='black'),horizontalalignment='right', fontsize = '15')
    plt.text(wn.get_node('FP9001').coordinates[0],wn.get_node('FP9001').coordinates[1]-1400,s = 'Four Points R + T + PS', bbox=dict(facecolor='mediumaquamarine', alpha=0.9, edgecolor='black'),horizontalalignment='left', fontsize = '15')
    plt.text(wn.get_node('104158').coordinates[0]-400,wn.get_node('104158').coordinates[1]-500,s = 'GL Tank', bbox=dict(facecolor='mediumaquamarine', alpha=0.9, edgecolor='black'),horizontalalignment='right', fontsize = '15')
    plt.text(wn.get_node('STC9001').coordinates[0]-400,wn.get_node('STC9001').coordinates[1]+500,s = 'STC Tank', bbox=dict(facecolor='mediumaquamarine', alpha=0.9, edgecolor='black'),horizontalalignment='right', fontsize = '15')
    plt.text(wn.get_node('PP35').coordinates[0]-300,wn.get_node('PP35').coordinates[1]-800,s = 'PP35', bbox=dict(facecolor='white', alpha=0.9, edgecolor='black'),horizontalalignment='right', fontsize = '12')
    plt.text(wn.get_node('PP48').coordinates[0]-600,wn.get_node('PP48').coordinates[1]+500,s = 'PP48', bbox=dict(facecolor='white', alpha=0.9, edgecolor='black'),horizontalalignment='right', fontsize = '12')
    plt.text(wn.get_node('SP104').coordinates[0]+1200,wn.get_node('SP104').coordinates[1]+1000,s = 'SP104', bbox=dict(facecolor='white', alpha=0.9, edgecolor='black'),horizontalalignment='right', fontsize = '12')
    plt.text(wn.get_node('SP105').coordinates[0]-100,wn.get_node('SP105').coordinates[1]+600,s = 'SP105', bbox=dict(facecolor='white', alpha=0.9, edgecolor='black'),horizontalalignment='right', fontsize = '12')
    plt.text(wn.get_node('SP106').coordinates[0]-1100,wn.get_node('SP106').coordinates[1]-300,s = 'SP106', bbox=dict(facecolor='white', alpha=0.9, edgecolor='black'),horizontalalignment='right', fontsize = '12')
    plt.text(wn.get_node('SP108').coordinates[0]+1100,wn.get_node('SP108').coordinates[1]+700,s = 'SP108', bbox=dict(facecolor='white', alpha=0.9, edgecolor='black'),horizontalalignment='right', fontsize = '12')
    plt.text(wn.get_node('SP110').coordinates[0]+700,wn.get_node('SP110').coordinates[1]+700,s = 'SP110', bbox=dict(facecolor='white', alpha=0.9, edgecolor='black'),horizontalalignment='right', fontsize = '12')
    plt.text(wn.get_node('SP111').coordinates[0]+1100,wn.get_node('SP111').coordinates[1]-800,s = 'SP111', bbox=dict(facecolor='white', alpha=0.9, edgecolor='black'),horizontalalignment='right', fontsize = '12')
    plt.text(wn.get_node('SP114').coordinates[0]-400,wn.get_node('SP114').coordinates[1]-400,s = 'SP114', bbox=dict(facecolor='white', alpha=0.9, edgecolor='black'),horizontalalignment='right', fontsize = '12')
    plt.text(wn.get_node('SP116').coordinates[0]+1100,wn.get_node('SP116').coordinates[1]-800,s = 'SP116', bbox=dict(facecolor='white', alpha=0.9, edgecolor='black'),horizontalalignment='right', fontsize = '12')
    plt.text(wn.get_node('SP115').coordinates[0]-200,wn.get_node('SP115').coordinates[1]-1200,s = 'SP115', bbox=dict(facecolor='white', alpha=0.9, edgecolor='black'),horizontalalignment='right', fontsize = '12')

def legend_without_duplicate_labels(ax):
    handles, labels = ax.get_legend_handles_labels()
    unique = [(h, l) for i, (h, l) in enumerate(zip(handles, labels)) if l not in labels[:i]]
    ax.legend(*zip(*unique))

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
            
# Special nodes list
spl_nodes = []
spl_nodes_dict = {}
for tank_name, tank in wn.tanks():
    # spl_nodes.append(tank_name)
    spl_nodes_dict[tank_name] = tank_name
    
for res_name, res in wn.reservoirs():
    # spl_nodes.append(res_name)
    spl_nodes_dict[res_name] = res_name

spl_nodes = ['PP35', 'PP48', 'SP110', 'SP108', 'SP116', 'SP114', 'SP106', 'SP105', 'SP115', 'SP104', 'SP111']

for i in range(len(spl_nodes)):
    spl_nodes_dict[spl_nodes[i]] = spl_nodes[i]

# In[] Diameters (continuous)

# Extract diams etc
# num_links = len(wn.link_name_list)
num_pipes = len(wn.pipe_name_list)
pipe_diams = []
pipe_diams_col = []

for i in range(len(pipe_list_names)):
    pipe_diams.append(39.3701*wn.get_link(pipe_list_names[i]).diameter)

output = set()
for x in pipe_diams:
    output.add(x)
sorted_diams = sorted(output)
print(sorted_diams)
print(min(sorted_diams)/39.3701)

for i in range(len(pipe_list_names)):
    pipe_diams_col.append(sorted_diams.index(pipe_diams[i]))


fig, ax = plt.subplots(figsize=(15,25))
nxp.draw_networkx_nodes(G, pos_dict, node_size = 0, label = None)
nxp.draw_networkx_nodes(G, pos_dict, nodelist = wn.tank_name_list, node_size = 200, node_color = 'k', node_shape = 'h')
nxp.draw_networkx_nodes(G, pos_dict, nodelist = wn.reservoir_name_list, node_size = 300, node_color = 'k', node_shape = 's')
nxp.draw_networkx_nodes(G, pos_dict, nodelist = spl_nodes, node_size = 200, node_color = 'r')

g = nxp.draw_networkx_edges(G, pos_dict, edgelist = G_list_pipes_only, edge_color = pipe_diams, width = 2, edge_cmap = mpl.cm.gnuplot, arrows = False)
nxp.draw_networkx_edges(G, pos_dict, edgelist = G_list_pumps_only, edge_color = 'k', label = 'Pump', width = 2,  arrows = False)
nxp.draw_networkx_edges(G, pos_dict, edgelist = G_list_valves_only, edge_color = 'k', label = 'Valve', width = 2, arrows = False)
nxp.draw_networkx_labels(G,pos_dict, labels = spl_nodes_dict, bbox = dict(facecolor = 'white', alpha = 0.9), verticalalignment = 'top')
cbar = plt.colorbar(g)
cbar.set_label('Pipe Diameter [in]')
fig.savefig(image_path+'/diameters.png')

# In[] 2. Diameters (distinct)

num_pipes = len(wn.pipe_name_list)
pipe_diams = []
pipe_diams_col = []
pipe_diams_ind = []
pipe_diams_width = []

for i in range(len(pipe_list_names)):
    pipe_diams.append(39.3701*wn.get_link(pipe_list_names[i]).diameter) #convert to inches

output = set()
for x in pipe_diams:
    output.add(x)
sorted_diams = sorted(output)
line_widths = list(np.arange(1,len(sorted_diams)+1))
diam_nos = [0] * len(sorted_diams)

cmap = mpl.cm.get_cmap('Blues')

# Sort diams and build color and width list
for i in range(len(pipe_list_names)):
    pipe_diams_col.append(sorted_diams.index(pipe_diams[i]))
    pipe_diams_ind.append(cmap(sorted_diams.index(pipe_diams[i])/(len(sorted_diams)-1)))
    pipe_diams_width.append(line_widths[sorted_diams.index(pipe_diams[i])])
    for j in range(len(sorted_diams)):
        if pipe_diams[i] == sorted_diams[j]:
            diam_nos[j] = diam_nos[j] + 1

# Build legend
custom_lines = []
leg_labels = []
for i in range(len(sorted_diams)):
    custom_lines.append(Line2D([0], [0], color=cmap(i/(len(sorted_diams)-1)), lw = i))
    leg_labels.append(int(sorted_diams[i]))
leg_labels[0] = 1.5

# Plot
fig, ax = plt.subplots(figsize=(15,25))
nxp.draw_networkx_nodes(G, pos_dict, node_size = 0, label = None)
nxp.draw_networkx_nodes(G, pos_dict, nodelist = wn.tank_name_list, node_size = 200, node_color = 'b', node_shape = 'h')
nxp.draw_networkx_nodes(G, pos_dict, nodelist = wn.reservoir_name_list, node_size = 200, node_color = 'k', node_shape = 's')
nxp.draw_networkx_nodes(G, pos_dict, nodelist = spl_nodes, node_size = 200, node_color = 'r')

g = nxp.draw_networkx_edges(G, pos_dict, edgelist = G_list_pipes_only, edge_color = pipe_diams_ind, width = pipe_diams_width, edge_cmap = mpl.cm.gnuplot, arrows = False)
nxp.draw_networkx_edges(G, pos_dict, edgelist = G_list_pumps_only, edge_color = 'k', label = 'Pump', width = 2,  arrows = False)
nxp.draw_networkx_edges(G, pos_dict, edgelist = G_list_valves_only, edge_color = 'k', label = 'Valve', width = 2, arrows = False)
plot_spl_elements()
plt.axis('off')
ax.legend(custom_lines, leg_labels, title = 'Pipe Diameters [inches]', fontsize = '15', title_fontsize = '17')
fig.savefig(image_path+'/diameters.png')

# In[] 3. Pressure Zones
df = pd.read_excel('NWC Pipes.xlsx')
pipes_list = df['ID'].astype(str)
zones = []
materials = []
zones_list = list(df['Zone'].unique())
materials_list = list(df['Material'].unique())

for i in range(len(pipe_list_names)):
    ind = np.where(pipes_list == pipe_list_names[i])[0][0]
    zones.append(df['Zone'][ind])
    materials.append(df['Material'][ind])
    
cmap = mpl.cm.get_cmap('gist_rainbow')

zone_col_ind = []
material_col_ind = []
zone_col = []
material_col = []

for i in range(len(pipes_list)):
    zone_col_ind.append(zones_list.index(zones[i]))
    material_col_ind.append(materials_list.index(materials[i]))
    zone_col.append(cmap(zones_list.index(zones[i])/(len(zones_list)-1)))
    material_col.append(cmap(materials_list.index(materials[i])/(len(materials_list)-1)))

custom_lines = []
leg_labels = []
for i in range(len(zones_list)):
    custom_lines.append(Line2D([0], [0], color=cmap(i/(len(zones_list)-1)), lw = 4))
    leg_labels.append(zones_list[i])
    
leg_labels, custom_lines = zip(*sorted(zip(leg_labels, custom_lines), key=lambda t: t[0]))

fig, ax = plt.subplots(figsize=(15,25))
nxp.draw_networkx_nodes(G, pos_dict, node_size = 0, label = None)
nxp.draw_networkx_nodes(G, pos_dict, nodelist = wn.tank_name_list, node_size = 200, node_color = 'b', node_shape = 'h')
nxp.draw_networkx_nodes(G, pos_dict, nodelist = wn.reservoir_name_list, node_size = 200, node_color = 'k', node_shape = 's')
nxp.draw_networkx_nodes(G, pos_dict, nodelist = spl_nodes, node_size = 200, node_color = 'r')

g = nxp.draw_networkx_edges(G, pos_dict, edgelist = G_list_pipes_only, edge_color = zone_col, width = 3, edge_cmap = cmap, arrows = False)
nxp.draw_networkx_edges(G, pos_dict, edgelist = G_list_pumps_only, edge_color = 'k', label = 'Pump', width = 2,  arrows = False)
nxp.draw_networkx_edges(G, pos_dict, edgelist = G_list_valves_only, edge_color = 'k', label = 'Valve', width = 2, arrows = False)
plot_spl_elements()
plt.axis('off')
ax.legend(custom_lines, leg_labels, title = 'Pressure Zone', fontsize = '15', title_fontsize = '17')
# cbar = plt.colorbar(g)
cbar.set_label('Pressure Zone')
fig.savefig(image_path+'/zones.png')

# In[] 4. Pipe Materials
custom_lines = []
leg_labels = []

for i in range(len(materials_list)):
    custom_lines.append(Line2D([0], [0], color=cmap(i/(len(materials_list)-1)), lw = 4))
    leg_labels.append(materials_list[i])
    
leg_labels, custom_lines = zip(*sorted(zip(leg_labels, custom_lines), key=lambda t: t[0]))


fig, ax = plt.subplots(figsize=(15,25))
nxp.draw_networkx_nodes(G, pos_dict, node_size = 0, label = None)
nxp.draw_networkx_nodes(G, pos_dict, nodelist = wn.tank_name_list, node_size = 200, node_color = 'b', node_shape = 'h')
nxp.draw_networkx_nodes(G, pos_dict, nodelist = wn.reservoir_name_list, node_size = 200, node_color = 'k', node_shape = 's')
nxp.draw_networkx_nodes(G, pos_dict, nodelist = spl_nodes, node_size = 200, node_color = 'r')

g = nxp.draw_networkx_edges(G, pos_dict, edgelist = G_list_pipes_only, edge_color = material_col, width = 3, edge_cmap = cmap, arrows = False)
nxp.draw_networkx_edges(G, pos_dict, edgelist = G_list_pumps_only, edge_color = 'k', label = 'Pump', width = 2,  arrows = False)
nxp.draw_networkx_edges(G, pos_dict, edgelist = G_list_valves_only, edge_color = 'k', label = 'Valve', width = 2, arrows = False)
plt.axis('off')
ax.legend(custom_lines, leg_labels, title = 'Material', fontsize = '15', title_fontsize = '17')
plot_spl_elements()
cbar.set_label('Material')
fig.savefig(image_path+'/materials.png')


        
# In[]
# Basic plot
fig, ax = plt.subplots(figsize=(15,25))
nxp.draw_networkx_nodes(G, pos_dict, node_size = 0, label = None)
nxp.draw_networkx_nodes(G, pos_dict, nodelist = wn.reservoir_name_list, node_size = 200, node_color = 'k', node_shape = 's')
nxp.draw_networkx_nodes(G, pos_dict, nodelist = wn.tank_name_list, node_size = 200, node_color = 'b', node_shape = 'h')
nxp.draw_networkx_nodes(G, pos_dict, nodelist = spl_nodes, node_size = 200, node_color = 'r')
nxp.draw_networkx_edges(G, pos_dict, arrows = False, edge_color = 'k', width = 1.5)
plot_spl_elements()
# add valves
valve_list = []
for valve_name, valve in wn.valves():
    valve_list.append(valve.start_node_name)
nxp.draw_networkx_nodes(G, pos_dict, nodelist = valve_list, node_size = 200, node_color = 'orange', node_shape = 'P')
plt.axis('off')
fig.savefig(image_path+'/barebones.png')