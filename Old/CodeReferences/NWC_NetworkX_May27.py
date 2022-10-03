# Import libraries
import wntr
import networkx as nx
import numpy as np
import scipy.sparse as sp
import pandas as pd
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

# Define .INP file name
# inp_file = 'NWC_2020_Calibration_EPANET_edited_Aug28.inp'
inp_file = 'NWC_old_stations.inp'

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

# In[] BUILD EDGE COLOR LISTS

    # # Extract diams etc
    # # num_links = len(wn.link_name_list)
    # num_pipes = len(wn.pipe_name_list)
    # pipe_diams = []
    # pipe_diams_col = []
    
    # for i in range(len(pipe_list_names)):
    #     pipe_diams.append(39.3701*wn.get_link(pipe_list_names[i]).diameter)
    
    # output = set()
    # for x in pipe_diams:
    #     output.add(x)
    # sorted_diams = sorted(output)
    # print(sorted_diams)
    # print(min(sorted_diams)/39.3701)
    
    # for i in range(len(pipe_list_names)):
    #     pipe_diams_col.append(sorted_diams.index(pipe_diams[i]))
    
    # # Plot histogram
    # fig = plt.plot(figsize=(8,12))
    # plt.hist(pipe_diams)
    # plt.xlabel('Diameter [inches]')
    # plt.ylabel('Number of pipes')
    # plt.savefig(image_path+'/diameters histogram.png') #, bins = 51, range = (0,50))
    
    # fig, ax = plt.subplots(figsize=(15,25))
    # nxp.draw_networkx_nodes(G, pos_dict, node_size = 0, label = None)
    # nxp.draw_networkx_nodes(G, pos_dict, nodelist = wn.tank_name_list, node_size = 200, node_color = 'k', node_shape = 'h')
    # nxp.draw_networkx_nodes(G, pos_dict, nodelist = wn.reservoir_name_list, node_size = 300, node_color = 'k', node_shape = 's')
    # nxp.draw_networkx_nodes(G, pos_dict, nodelist = spl_nodes, node_size = 200, node_color = 'r')
    
    # g = nxp.draw_networkx_edges(G, pos_dict, edgelist = G_list_pipes_only, edge_color = pipe_diams, width = 2, edge_cmap = mpl.cm.gnuplot, arrows = None)
    # nxp.draw_networkx_edges(G, pos_dict, edgelist = G_list_pumps_only, edge_color = 'k', label = 'Pump', width = 2,  arrows = None)
    # nxp.draw_networkx_edges(G, pos_dict, edgelist = G_list_valves_only, edge_color = 'k', label = 'Valve', width = 2, arrows = None)
    # nxp.draw_networkx_labels(G,pos_dict, labels = spl_nodes_dict, bbox = dict(facecolor = 'white', alpha = 0.9), verticalalignment = 'top')
    # cbar = plt.colorbar(g)
    # cbar.set_label('Pipe Diameter [in]')
    # fig.savefig(image_path+'/diameters.png')

# In[] BUILD EDGE COLOR LISTS - DIAM 2!

# Extract diams etc
num_pipes = len(wn.pipe_name_list)
pipe_diams = []
pipe_diams_col = []
pipe_diams_ind = []
pipe_diams_width = []

for i in range(len(pipe_list_names)):
    pipe_diams.append(39.3701*wn.get_link(pipe_list_names[i]).diameter)

output = set()
for x in pipe_diams:
    output.add(x)
sorted_diams = sorted(output)
line_widths = list(np.arange(1,len(sorted_diams)+1))
diam_nos = [0] * len(sorted_diams)

# cmap = mpl.cm.get_cmap('YlOrRd')
cmap = mpl.cm.get_cmap('Blues')

for i in range(len(pipe_list_names)):
    pipe_diams_col.append(sorted_diams.index(pipe_diams[i]))
    pipe_diams_ind.append(cmap(sorted_diams.index(pipe_diams[i])/(len(sorted_diams)-1)))
    pipe_diams_width.append(line_widths[sorted_diams.index(pipe_diams[i])])
    for j in range(len(sorted_diams)):
        if pipe_diams[i] == sorted_diams[j]:
            diam_nos[j] = diam_nos[j] + 1

custom_lines = []
leg_labels = []
for i in range(len(sorted_diams)):
    custom_lines.append(Line2D([0], [0], color=cmap(i/(len(sorted_diams)-1)), lw = i))
    leg_labels.append(int(sorted_diams[i]))
leg_labels[0] = 1.5
print(leg_labels)

# Plot histogram
fig = plt.plot(figsize=(12,8))
plt.bar(np.arange(len(sorted_diams)), diam_nos, color = 'darkorange', tick_label = leg_labels) #, bins = 61)
plt.xlabel('Diameter [inches]')
plt.ylabel('Number of Pipes')
plt.savefig(image_path+'/diameters histogram.png')

fig, ax = plt.subplots(figsize=(15,25))
nxp.draw_networkx_nodes(G, pos_dict, node_size = 0, label = None)
nxp.draw_networkx_nodes(G, pos_dict, nodelist = wn.tank_name_list, node_size = 200, node_color = 'b', node_shape = 'h')
nxp.draw_networkx_nodes(G, pos_dict, nodelist = wn.reservoir_name_list, node_size = 200, node_color = 'k', node_shape = 's')
nxp.draw_networkx_nodes(G, pos_dict, nodelist = spl_nodes, node_size = 200, node_color = 'r')

g = nxp.draw_networkx_edges(G, pos_dict, edgelist = G_list_pipes_only, edge_color = pipe_diams_ind, width = pipe_diams_width, edge_cmap = mpl.cm.gnuplot, arrows = None)
nxp.draw_networkx_edges(G, pos_dict, edgelist = G_list_pumps_only, edge_color = 'k', label = 'Pump', width = 2,  arrows = None)
nxp.draw_networkx_edges(G, pos_dict, edgelist = G_list_valves_only, edge_color = 'k', label = 'Valve', width = 2, arrows = None)
plot_spl_elements()
plt.axis('off')
ax.legend(custom_lines, leg_labels, title = 'Pipe Diameters [inches]', fontsize = '15', title_fontsize = '17')
cbar.set_label('Pipe Diameter [in]')
fig.savefig(image_path+'/diameters.png')

# Pressure Zones
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

# Plot histogram
fig = plt.plot(figsize=(30,8))
sns.set(rc = {'figure.figsize':(30, 8)})
sns.countplot(x=df['Zone'])
sns.set_style("whitegrid", {'axes.grid' : False})
plt.xlabel('Zone')
plt.ylabel('Number of Pipes')
plt.savefig(image_path+'/zones histogram.png')

fig, ax = plt.subplots(figsize=(15,25))
nxp.draw_networkx_nodes(G, pos_dict, node_size = 0, label = None)
nxp.draw_networkx_nodes(G, pos_dict, nodelist = wn.tank_name_list, node_size = 200, node_color = 'b', node_shape = 'h')
nxp.draw_networkx_nodes(G, pos_dict, nodelist = wn.reservoir_name_list, node_size = 200, node_color = 'k', node_shape = 's')
nxp.draw_networkx_nodes(G, pos_dict, nodelist = spl_nodes, node_size = 200, node_color = 'r')

g = nxp.draw_networkx_edges(G, pos_dict, edgelist = G_list_pipes_only, edge_color = zone_col, width = 3, edge_cmap = cmap, arrows = None)
nxp.draw_networkx_edges(G, pos_dict, edgelist = G_list_pumps_only, edge_color = 'k', label = 'Pump', width = 2,  arrows = None)
nxp.draw_networkx_edges(G, pos_dict, edgelist = G_list_valves_only, edge_color = 'k', label = 'Valve', width = 2, arrows = None)
plot_spl_elements()
plt.axis('off')
ax.legend(custom_lines, leg_labels, title = 'Pressure Zone', fontsize = '15', title_fontsize = '17')
cbar.set_label('Pressure Zone')
fig.savefig(image_path+'/zones.png')

# Pipe Materials
custom_lines = []
leg_labels = []

for i in range(len(materials_list)):
    custom_lines.append(Line2D([0], [0], color=cmap(i/(len(materials_list)-1)), lw = 4))
    leg_labels.append(materials_list[i])
    
leg_labels, custom_lines = zip(*sorted(zip(leg_labels, custom_lines), key=lambda t: t[0]))

# Plot histogram
fig = plt.plot(figsize=(12,8))
sns.set(rc = {'figure.figsize':(12, 8)})
sns.countplot(x=df['Material'])
sns.set_style("whitegrid", {'axes.grid' : False})
plt.xlabel('Material')
plt.ylabel('Number of Pipes')
plt.savefig(image_path+'/materials histogram.png')

fig, ax = plt.subplots(figsize=(15,25))
nxp.draw_networkx_nodes(G, pos_dict, node_size = 0, label = None)
nxp.draw_networkx_nodes(G, pos_dict, nodelist = wn.tank_name_list, node_size = 200, node_color = 'b', node_shape = 'h')
nxp.draw_networkx_nodes(G, pos_dict, nodelist = wn.reservoir_name_list, node_size = 200, node_color = 'k', node_shape = 's')
nxp.draw_networkx_nodes(G, pos_dict, nodelist = spl_nodes, node_size = 200, node_color = 'r')

g = nxp.draw_networkx_edges(G, pos_dict, edgelist = G_list_pipes_only, edge_color = material_col, width = 3, edge_cmap = cmap, arrows = None)
nxp.draw_networkx_edges(G, pos_dict, edgelist = G_list_pumps_only, edge_color = 'k', label = 'Pump', width = 2,  arrows = None)
nxp.draw_networkx_edges(G, pos_dict, edgelist = G_list_valves_only, edge_color = 'k', label = 'Valve', width = 2, arrows = None)
plt.axis('off')
ax.legend(custom_lines, leg_labels, title = 'Material', fontsize = '15', title_fontsize = '17')
plot_spl_elements()
cbar.set_label('Material')
fig.savefig(image_path+'/materials.png')


# In[] BUILD NODE COLOR LISTS

cmap = mpl.cm.get_cmap('YlOrRd')
# cmap = mc.LinearSegmentedColormap.from_list("MyCmapName",["b","r"])

# NODE DEMANDS
alldems = []
demzero = []
dem0 = []
dem10 = []
dem20 = []
dem30 = []
dem40 = []
dem50 = []
dem60 = []
demother = []

for i in range(len(junc_names)):
    dem = from_si(FlowUnits.GPM, wn.get_node(junc_names[i]).base_demand, HydParam.Flow)
    alldems.append(dem)
    if dem != 0:
        demzero.append(dem)
    
    if dem == 0:
        dem0.append(junc_names[i])
        
    elif dem > 0 and dem <= 2:
        dem10.append(junc_names[i])

    elif dem > 2 and dem <= 4:
        dem20.append(junc_names[i])

    elif dem > 4 and dem <= 10:
        dem30.append(junc_names[i])
        
    elif dem > 10 and dem <= 20:
        dem40.append(junc_names[i])
        
    elif dem > 20 and dem <= 40:
        dem50.append(junc_names[i])
        
    elif dem > 40:
        dem60.append(junc_names[i])
        
    else:
        demother.append(junc_names[i])

# Plot histogram

fig2 = plt.plot(figsize=(8,12))
plt.hist(demzero , bins = 121, range = (0,60), color = 'darkorange')
sns.set_style("whitegrid", {'axes.grid' : False})
plt.xlabel('Demand at nodes with non-zero demand [GPM]')
plt.ylabel('Number of Junctions')
plt.savefig(image_path+'/demands histogram.png')

fig, ax=plt.subplots(figsize = (12,8))
plt.figure(1)
plt.subplot(211)
plt.hist(alldems , bins = 121, range = (0,60))
plt.ylabel('Number of Junctions')
plt.legend()
plt.subplot(212)
plt.hist(demzero , bins = 121, range = (0,60))
plt.xlabel('Demand [GPM]')
plt.ylabel('Number of Junctions')
plt.legend()
fig.savefig(image_path + 'demands histogram.png')

fig, ax = plt.subplots(figsize=(15,25))
nxp.draw_networkx_nodes(G, pos_dict, nodelist = dem10, node_size = 30, node_color = cmap(float(1/6)), label = '0 - 2')
nxp.draw_networkx_nodes(G, pos_dict, nodelist = dem20, node_size = 50, node_color = cmap(float(2/6)), label = '2 - 4')
nxp.draw_networkx_nodes(G, pos_dict, nodelist = dem30, node_size = 70, node_color = cmap(float(3/6)), label = '4 - 10')
nxp.draw_networkx_nodes(G, pos_dict, nodelist = dem40, node_size = 90, node_color = cmap(float(4/6)), label = '10 - 20')
nxp.draw_networkx_nodes(G, pos_dict, nodelist = dem50, node_size = 120, node_color = cmap(float(5/6)), label = '20 - 40')
nxp.draw_networkx_nodes(G, pos_dict, nodelist = dem60, node_size = 200, node_color = cmap(1.0), label = '> 40')

nxp.draw_networkx_edges(G, pos_dict, arrows = None, edge_color = 'k')
plot_spl_elements()

plt.axis('off')
plt.legend(scatterpoints = 1, title = 'Demand [GPM]', loc = 'lower right', fontsize = '15', title_fontsize = '17')
fig.savefig(image_path+'/demands.png')


# NODE ELEVATIONS
junc_list = []
elevations = []

for junc_name, junc in wn.junctions():
    elevations.append(3.28084*junc.elevation)
    junc_list.append(junc_name)
    
fig2 = plt.plot(figsize=(8,12))
plt.hist(elevations, bins = 101, color = 'darkorange') #, range = (0,50))
plt.xlabel('Elevation [ft]')
plt.ylabel('Number of Junctions')
plt.savefig(image_path+'/elevations histogram.png')
#sns.displot(elevations, kind = "kde") #, x="Elevations [ft]", kind="kde")
    
fig, ax = plt.subplots(figsize=(15,25))
nodes = nxp.draw_networkx_nodes(G, pos_dict, nodelist = junc_list, node_size = 40, node_color = elevations, cmap = cmap)
nxp.draw_networkx_edges(G, pos_dict, arrows = None, edge_color = 'k')
plot_spl_elements()

valve_list = []
for valve_name, valve in wn.valves():
    valve_list.append(valve.start_node_name)
nxp.draw_networkx_nodes(G, pos_dict, nodelist = valve_list, node_size = 200, node_color = 'orange', node_shape = 'P')

cbar = plt.colorbar(nodes)
cbar.set_label('Junction elevation [ft]', fontsize = 15)
plt.axis('off')
plt.savefig(image_path+'/elevations.png') 


# AVERAGE PRESSURE
#cmap = mpl.cm.get_cmap('YlOrRd')
cmap = mc.LinearSegmentedColormap.from_list("MyCmapName",["yellow","orangered"])
junc_list = []
avg_pres = []
pres_90 = []
pres_90_nodes = []
all_pres = []

for junc_name, junc in wn.junctions():
    pres = from_si(FlowUnits.GPM, results.node['pressure'].loc[:, junc_name], HydParam.Pressure)
    all_pres.append(np.mean(pres))
    if np.mean(pres) < 90:
        avg_pres.append(np.mean(pres))
        junc_list.append(junc_name)
    if np.mean(pres) >= 90:
        pres_90.append(np.mean(pres))
        pres_90_nodes.append(junc_name)
    
fig2 = plt.plot(figsize=(8,12))
plt.hist(all_pres, bins = 51, color = 'darkorange') #, range = (0,50))
plt.xlabel('Average Pressure [GPM]')
plt.ylabel('Number of Junctions')
plt.savefig(image_path+'/avg pressures histogram.png')    

fig, ax = plt.subplots(figsize=(15,25))
nodes = nxp.draw_networkx_nodes(G, pos_dict, nodelist = junc_list, node_size = 40, node_color = avg_pres, cmap = cmap)
nxp.draw_networkx_nodes(G, pos_dict, nodelist = pres_90_nodes, node_size = 80, node_color = 'k')
nxp.draw_networkx_nodes(G, pos_dict, nodelist = pres_90_nodes, node_size = 40, node_color = 'crimson')
nxp.draw_networkx_edges(G, pos_dict, arrows = None, edge_color = 'k')
plot_spl_elements()
# plt.text(0,0, s = 'Nodes in red have an average pressure > 90 GPM', bbox=dict(facecolor='white', alpha=0.9, edgecolor='black'),horizontalalignment='right', fontsize = '12')

valve_list = []
for valve_name, valve in wn.valves():
    valve_list.append(valve.start_node_name)
nxp.draw_networkx_nodes(G, pos_dict, nodelist = valve_list, node_size = 200, node_color = 'black', node_shape = 'P')

cbar = plt.colorbar(nodes)
cbar.set_label('Average pressure at each junction [ft]', fontsize = 15)
plt.axis('off')
plt.savefig(image_path+'/avg pressures.png') 


# WATER AGE AVERAGE
cmap = mpl.cm.get_cmap('YlOrRd')
junc_list = []
water_age = []
wn.options.quality.parameter = 'AGE'
sim_age = wntr.sim.EpanetSimulator(wn)
results_age = sim_age.run_sim()
age = results_age.node['quality']

for junc_name, junc in wn.junctions():
    water_age.append(np.mean(age.loc[:,junc_name])/3600)
    junc_list.append(junc_name)
    
fig2 = plt.plot(figsize=(8,12))
plt.hist(water_age, color = 'darkorange') #, bins = 51) #, range = (0,50))
plt.xlabel('Average Water Age over 24 Hr Period')
plt.ylabel('Number of Junctions')
plt.savefig(image_path+'/avg water age histogram.png')    

fig, ax = plt.subplots(figsize=(15,25))
nodes = nxp.draw_networkx_nodes(G, pos_dict, nodelist = junc_list, node_size = 40, node_color = water_age, cmap = cmap)
nxp.draw_networkx_edges(G, pos_dict, arrows = None, edge_color = 'k')
plot_spl_elements()

cbar = plt.colorbar(nodes)
cbar.set_label('Average water age at each junction [hr]', fontsize = 15)
plt.axis('off')
plt.savefig(image_path+'/avg water age.png') 

# WATER AGE MAX
junc_list = []
water_age = []
wn.options.quality.parameter = 'AGE'
sim_age = wntr.sim.EpanetSimulator(wn)
results_age = sim_age.run_sim()
age = results_age.node['quality']

for junc_name, junc in wn.junctions():
    water_age.append(np.max(age.loc[:,junc_name])/3600)
    junc_list.append(junc_name)
    
fig2 = plt.plot(figsize=(8,12))
plt.hist(water_age, color = 'darkorange') #, bins = 51) #, range = (0,50))
plt.xlabel('Maximum Water Age over 24 Hr Period')
plt.ylabel('Number of Junctions')
plt.savefig(image_path+'/max water age histogram.png')    

fig, ax = plt.subplots(figsize=(15,25))
nodes = nxp.draw_networkx_nodes(G, pos_dict, nodelist = junc_list, node_size = 40, node_color = water_age, cmap = cmap)
nxp.draw_networkx_edges(G, pos_dict, arrows = None, edge_color = 'k')
plot_spl_elements()

cbar = plt.colorbar(nodes)
cbar.set_label('Maximum water age at each junction [hr]', fontsize = 15)
plt.axis('off')
plt.savefig(image_path+'/max water age.png') 

# In[]  NODE COLOR LISTS FOR TRACER STUDY FOR 24 HOURS
cmap = mpl.cm.get_cmap('YlOrRd')

for res_name, res in wn.reservoirs():
    trace_node = res_name
    wn.options.quality.parameter = 'TRACE'
    wn.options.quality.trace_node = trace_node
    sim_am9001 = wntr.sim.EpanetSimulator(wn)
    results_am9001 = sim_am9001.run_sim()
    tracer_am9001 = results_am9001.node['quality']
    tr_am9001 = {}
    junc_list = []
    tracer = []
    tracer_tot = []
    
    for junc_name, junc in wn.junctions():
        if wn.get_node(junc_name).base_demand != 0:
            t_r = tracer_am9001.loc[:,junc_name]
            tr_am9001[junc_name] = np.max(t_r)
            tracer_tot.append(np.max(t_r))
            if np.max(t_r) != 0:
                junc_list.append(junc_name)
                tracer.append(np.max(t_r))
        
    fig, ax = plt.subplots(figsize=(15,25))
    nodes = nxp.draw_networkx_nodes(G, pos_dict, nodelist = junc_list, node_size = 40, node_color = tracer, cmap = cmap)
    nxp.draw_networkx_edges(G, pos_dict, arrows = None, edge_color = 'k')
    
    plot_spl_elements()
    cbar = plt.colorbar(nodes)
    cbar.set_label('Maximum daily percentage of water sourced from Reservoir {} for 24 hr duration'.format(res_name), fontsize = 15)
    plt.axis('off')
    plt.savefig(image_path+'/Tracer plots/res {} tracer 24 hrs.png'.format(res_name))
    
    fig, ax=plt.subplots(figsize = (8,12))
    plt.figure(res_name)    
    plt.hist(tracer_tot, bins = 101, color = 'darkorange')
    plt.xlabel('Maximum % of Water Sourced from Res {} [GPM]'.format(res_name))
    plt.ylabel('Number of Junctions')
    plt.savefig(image_path+'/Tracer plots/tracer histogram res {}.png'.format(res_name))

# Tanks
for tank_name, tank in wn.tanks():
    trace_node = tank_name
    wn.options.quality.parameter = 'TRACE'
    wn.options.quality.trace_node = trace_node
    sim_am9001 = wntr.sim.EpanetSimulator(wn)
    results_am9001 = sim_am9001.run_sim()
    tracer_am9001 = results_am9001.node['quality']
    tr_am9001 = {}
    junc_list = []
    tracer = []
    tracer_tot = []

    for junc_name, junc in wn.junctions():
        if wn.get_node(junc_name).base_demand != 0:
            t_r = tracer_am9001.loc[:,junc_name]
            tr_am9001[junc_name] = np.max(t_r)
            tracer_tot.append(np.max(t_r))
            if np.max(t_r) != 0:
                junc_list.append(junc_name)
                tracer.append(np.max(t_r))
        
    fig, ax = plt.subplots(figsize=(15,25))
    nodes = nxp.draw_networkx_nodes(G, pos_dict, nodelist = junc_list, node_size = 40, node_color = tracer, cmap = cmap)
    nxp.draw_networkx_edges(G, pos_dict, arrows = None, edge_color = 'k')
    
    plot_spl_elements()
    cbar = plt.colorbar(nodes)
    cbar.set_label('Maximum daily percentage of water sourced from Tank {} for 24 hr duration'.format(tank_name), fontsize = 15)
    plt.axis('off')
    plt.savefig(image_path+'/Tracer plots/tank {} tracer 24 hrs.png'.format(tank_name))
    
    fig, ax=plt.subplots(figsize = (8,12))
    plt.figure(tank_name)
    plt.hist(tracer_tot, bins = 101, color = 'darkorange')
    plt.xlabel('Maximum % of Water Sourced from Tank {} [GPM]'.format(tank_name))
    plt.ylabel('Number of Junctions')
    plt.savefig(image_path+'/Tracer plots/tracer histogram rtankes {}.png'.format(tank_name))
    

# In[]
for tank_name, tank in wn.tanks():
    trace_node = tank_name
    wn.options.quality.parameter = 'TRACE'
    wn.options.quality.trace_node = trace_node
    sim_am9001 = wntr.sim.EpanetSimulator(wn)
    results_am9001 = sim_am9001.run_sim()
    tracer_am9001 = results_am9001.node['quality'].loc[:, '72838']
    # fig, ax=plt.subplots(figsize = (8,12))
    plt.figure(tank_name + node)
    plt.plot(x, tracer_am9001)
    plt.ylabel('Maximum % of Water Sourced from Tank {} [GPM]'.format(tank_name))
    plt.xlabel('Time [hr]')
    
for tank_name, tank in wn.reservoirs():
    trace_node = tank_name
    wn.options.quality.parameter = 'TRACE'
    wn.options.quality.trace_node = trace_node
    sim_am9001 = wntr.sim.EpanetSimulator(wn)
    results_am9001 = sim_am9001.run_sim()
    tracer_am9001 = results_am9001.node['quality'].loc[:, '72838']
    # fig, ax=plt.subplots(figsize = (8,12))
    plt.figure(tank_name + node)
    plt.plot(x, tracer_am9001)
    plt.ylabel('Maximum % of Water Sourced from Res {} [GPM]'.format(tank_name))
    plt.xlabel('Time [hr]')
    
for tank_name, tank in wn.tanks():
    trace_node = tank_name
    wn.options.quality.parameter = 'TRACE'
    wn.options.quality.trace_node = trace_node
    sim_am9001 = wntr.sim.EpanetSimulator(wn)
    results_am9001 = sim_am9001.run_sim()
    tracer_am9001 = results_am9001.node['quality'].loc[:, '786631']
    # fig, ax=plt.subplots(figsize = (8,12))
    plt.figure(tank_name + node)
    plt.plot(x, tracer_am9001)
    plt.ylabel('Maximum % of Water Sourced from Tank {} [GPM]'.format(tank_name))
    plt.xlabel('Time [hr]')
    
for tank_name, tank in wn.reservoirs():
    trace_node = tank_name
    wn.options.quality.parameter = 'TRACE'
    wn.options.quality.trace_node = trace_node
    sim_am9001 = wntr.sim.EpanetSimulator(wn)
    results_am9001 = sim_am9001.run_sim()
    tracer_am9001 = results_am9001.node['quality'].loc[:, '786631']
    # fig, ax=plt.subplots(figsize = (8,12))
    plt.figure(tank_name + node)
    plt.plot(x, tracer_am9001)
    plt.ylabel('Maximum % of Water Sourced from Res {} [GPM]'.format(tank_name))
    plt.xlabel('Time [hr]')
    
wn.options.time.duration = 3 * wn.options.time.duration

for tank_name, tank in wn.tanks():
    trace_node = tank_name
    wn.options.quality.parameter = 'TRACE'
    wn.options.quality.trace_node = trace_node
    sim_am9001 = wntr.sim.EpanetSimulator(wn)
    results_am9001 = sim_am9001.run_sim()
    x_val = len(results_am9001.node['head'].loc[:, junc_names[0]])
    time_step = wn.options.time.report_timestep
    mult_ts = 3600/time_step
    x = np.linspace(0,(x_val-1)/mult_ts,x_val)

    tracer_am9001 = results_am9001.node['quality'].loc[:, '72838']
    # fig, ax=plt.subplots(figsize = (8,12))
    plt.figure(tank_name + node)
    plt.plot(x, tracer_am9001)
    plt.ylabel('Maximum % of Water Sourced from Tank {} [GPM]'.format(tank_name))
    plt.xlabel('Time [hr]')
    
for tank_name, tank in wn.reservoirs():
    trace_node = tank_name
    wn.options.quality.parameter = 'TRACE'
    wn.options.quality.trace_node = trace_node
    sim_am9001 = wntr.sim.EpanetSimulator(wn)
    results_am9001 = sim_am9001.run_sim()
    tracer_am9001 = results_am9001.node['quality'].loc[:, '72838']
    # fig, ax=plt.subplots(figsize = (8,12))
    plt.figure(tank_name + node)
    plt.plot(x, tracer_am9001)
    plt.ylabel('Maximum % of Water Sourced from Res {} [GPM]'.format(tank_name))
    plt.xlabel('Time [hr]')
    
for tank_name, tank in wn.tanks():
    trace_node = tank_name
    wn.options.quality.parameter = 'TRACE'
    wn.options.quality.trace_node = trace_node
    sim_am9001 = wntr.sim.EpanetSimulator(wn)
    results_am9001 = sim_am9001.run_sim()
    tracer_am9001 = results_am9001.node['quality'].loc[:, '786631']
    # fig, ax=plt.subplots(figsize = (8,12))
    plt.figure(tank_name + node)
    plt.plot(x, tracer_am9001)
    plt.ylabel('Maximum % of Water Sourced from Tank {} [GPM]'.format(tank_name))
    plt.xlabel('Time [hr]')
    
for tank_name, tank in wn.reservoirs():
    trace_node = tank_name
    wn.options.quality.parameter = 'TRACE'
    wn.options.quality.trace_node = trace_node
    sim_am9001 = wntr.sim.EpanetSimulator(wn)
    results_am9001 = sim_am9001.run_sim()
    tracer_am9001 = results_am9001.node['quality'].loc[:, '786631']
    # fig, ax=plt.subplots(figsize = (8,12))
    plt.figure(tank_name + node)
    plt.plot(x, tracer_am9001)
    plt.ylabel('Maximum % of Water Sourced from Res {} [GPM]'.format(tank_name))
    plt.xlabel('Time [hr]')
    
# In[]  NODE COLOR LISTS FOR TRACER STUDY FOR 72 HOURS

wn.options.time.duration = 4 * wn.options.time.duration

for res_name, res in wn.reservoirs():
    trace_node = res_name
    wn.options.quality.parameter = 'TRACE'
    wn.options.quality.trace_node = trace_node
    sim_am9001 = wntr.sim.EpanetSimulator(wn)
    results_am9001 = sim_am9001.run_sim()
    tracer_am9001 = results_am9001.node['quality']
    tr_am9001 = {}
    junc_list = []
    tracer = []
    tracer_tot = []
    
    for junc_name, junc in wn.junctions():
        if wn.get_node(junc_name).base_demand != 0:
            t_r = tracer_am9001.loc[:,junc_name]
            tr_am9001[junc_name] = np.max(t_r)
            tracer_tot.append(np.max(t_r))
            if np.max(t_r) != 0:
                junc_list.append(junc_name)
                tracer.append(np.max(t_r))
        
    fig, ax = plt.subplots(figsize=(15,25))
    nodes = nxp.draw_networkx_nodes(G, pos_dict, nodelist = junc_list, node_size = 40, node_color = tracer, cmap = cmap)
    nxp.draw_networkx_edges(G, pos_dict, arrows = None, edge_color = 'k')
    
    plot_spl_elements()
    cbar = plt.colorbar(nodes)
    cbar.set_label('Maximum daily percentage of water sourced from Reservoir {} for 72 hr duration'.format(res_name), fontsize = 15)
    plt.axis('off')
    plt.savefig(image_path+'/Tracer plots/res {} tracer 72 hrs.png'.format(res_name))
    
    fig, ax=plt.subplots(figsize = (8,12))
    plt.figure(res_name)    
    plt.hist(tracer_tot, bins = 101, color = 'darkorange')
    plt.xlabel('72 hrs: Maximum % of Water Sourced from Res {} [GPM]'.format(res_name))
    plt.ylabel('Number of Junctions')
    plt.savefig(image_path+'/Tracer plots/tracer histogram res {} 72 hr.png'.format(res_name))

# Tanks
for tank_name, tank in wn.tanks():
    trace_node = tank_name
    wn.options.quality.parameter = 'TRACE'
    wn.options.quality.trace_node = trace_node
    sim_am9001 = wntr.sim.EpanetSimulator(wn)
    results_am9001 = sim_am9001.run_sim()
    tracer_am9001 = results_am9001.node['quality']
    tr_am9001 = {}
    junc_list = []
    tracer = []
    tracer_tot = []

    for junc_name, junc in wn.junctions():
        if wn.get_node(junc_name).base_demand != 0:
            t_r = tracer_am9001.loc[:,junc_name]
            tr_am9001[junc_name] = np.max(t_r)
            tracer_tot.append(np.max(t_r))
            if np.max(t_r) != 0:
                junc_list.append(junc_name)
                tracer.append(np.max(t_r))
        
    fig, ax = plt.subplots(figsize=(15,25))
    nodes = nxp.draw_networkx_nodes(G, pos_dict, nodelist = junc_list, node_size = 40, node_color = tracer, cmap = cmap)
    nxp.draw_networkx_edges(G, pos_dict, arrows = None, edge_color = 'k')
    
    plot_spl_elements()
    cbar = plt.colorbar(nodes)
    cbar.set_label('Maximum daily percentage of water sourced from Tank {} for 72 hr duration'.format(tank_name), fontsize = 15)
    plt.axis('off')
    plt.savefig(image_path+'/Tracer plots/tank {} tracer 72 hrs.png'.format(tank_name))
    
    fig, ax=plt.subplots(figsize = (8,12))
    plt.figure(tank_name)
    plt.hist(tracer_tot, bins = 101, color = 'darkorange')
    plt.xlabel('72 hrs: Maximum % of Water Sourced from Tank {} [GPM]'.format(tank_name))
    plt.ylabel('Number of Junctions')
    plt.savefig(image_path+'/Tracer plots/tracer histogram tank {} 72 hr.png'.format(tank_name))

#wn.options.time.duration = wn.options.time.duration/3

# In[]

times_list = [12, 24, 33, 48, 72]

             
for times in times_list:
    for res_name, res in wn.reservoirs():
        trace_node = res_name
        wn.options.quality.parameter = 'TRACE'
        wn.options.quality.trace_node = trace_node
        sim_am9001 = wntr.sim.EpanetSimulator(wn)
        results_am9001 = sim_am9001.run_sim()
        tracer_am9001 = results_am9001.node['quality']
        junc_list = []
        tracer = []
    
        for junc_name, junc in wn.junctions():
            if wn.get_node(junc_name).base_demand != 0:
                t_r = tracer_am9001.loc[times*time_step,junc_name]
                if t_r != 0:
                    junc_list.append(junc_name)
                    tracer.append(t_r)
            
        fig, ax = plt.subplots(figsize=(15,25))
        nodes = nxp.draw_networkx_nodes(G, pos_dict, nodelist = junc_list, node_size = 40, node_color = tracer, cmap = cmap, vmin = 0, vmax = 100)
        nxp.draw_networkx_edges(G, pos_dict, arrows = None, edge_color = 'k')
        
        plot_spl_elements()
        plt.title('Hour {}'.format(times), fontdict = {'fontsize' : 30})
        if times == 72:
            cbar = plt.colorbar(nodes)
            cbar.set_label('Percentage of water sourced from Reservoir {}'.format(res_name,times), fontsize = 15)
        plt.axis('off')
        plt.savefig(image_path+'/Tracer plots/{} hr res {} tracer.png'.format(times, res_name))
           
    # Tanks
    for res_name, res in wn.tanks():
        trace_node = res_name
        wn.options.quality.parameter = 'TRACE'
        wn.options.quality.trace_node = trace_node
        sim_am9001 = wntr.sim.EpanetSimulator(wn)
        results_am9001 = sim_am9001.run_sim()
        tracer_am9001 = results_am9001.node['quality']
        junc_list = []
        tracer = []
    
        for junc_name, junc in wn.junctions():
            if wn.get_node(junc_name).base_demand != 0:
                t_r = tracer_am9001.loc[times*time_step,junc_name]
                if t_r != 0:
                    junc_list.append(junc_name)
                    tracer.append(t_r)
            
        fig, ax = plt.subplots(figsize=(15,25))
        nodes = nxp.draw_networkx_nodes(G, pos_dict, nodelist = junc_list, node_size = 40, node_color = tracer, cmap = cmap, vmin = 0, vmax = 100)
        nxp.draw_networkx_edges(G, pos_dict, arrows = None, edge_color = 'k')
        
        plot_spl_elements()
        plt.title('Hour {}'.format(times), fontdict = {'fontsize' : 30})
        if times == 72:
            cbar = plt.colorbar(nodes)
            cbar.set_label('Percentage of water sourced from Tank {}'.format(res_name,times), fontsize = 15)
        plt.axis('off')
        plt.savefig(image_path+'/Tracer plots/{} hr tank {} tracer.png'.format(times, res_name))
        
# In[]
# Basic plot
fig, ax = plt.subplots(figsize=(15,25))
nxp.draw_networkx_nodes(G, pos_dict, node_size = 0, label = None)
nxp.draw_networkx_nodes(G, pos_dict, nodelist = wn.reservoir_name_list, node_size = 200, node_color = 'k', node_shape = 's')
nxp.draw_networkx_nodes(G, pos_dict, nodelist = wn.tank_name_list, node_size = 200, node_color = 'b', node_shape = 'h')
nxp.draw_networkx_nodes(G, pos_dict, nodelist = spl_nodes, node_size = 200, node_color = 'r')
nxp.draw_networkx_edges(G, pos_dict, arrows = False, edge_color = 'k', width = 1.5)
plt.text(wn.get_node('AM9001').coordinates[0]-500,wn.get_node('AM9001').coordinates[1],s = 'Anderson Mill R + T + PS', bbox=dict(facecolor='mediumaquamarine', alpha=0.9, edgecolor='black'),horizontalalignment='right', fontsize = '15')
plt.text(wn.get_node('FP9001').coordinates[0],wn.get_node('FP9001').coordinates[1]-1400,s = 'Four Points R + T + PS', bbox=dict(facecolor='mediumaquamarine', alpha=0.9, edgecolor='black'),horizontalalignment='left', fontsize = '15')
plt.text(wn.get_node('104158').coordinates[0]-400,wn.get_node('104158').coordinates[1]-500,s = 'GL Tank', bbox=dict(facecolor='mediumaquamarine', alpha=0.9, edgecolor='black'),horizontalalignment='right', fontsize = '15')
plt.text(wn.get_node('STC9001').coordinates[0]-400,wn.get_node('STC9001').coordinates[1]+500,s = 'STC Tank', bbox=dict(facecolor='mediumaquamarine', alpha=0.9, edgecolor='black'),horizontalalignment='right', fontsize = '15')
plt.text(wn.get_node('PP35').coordinates[0]-300,wn.get_node('PP35').coordinates[1]-800,s = 'PP35', bbox=dict(facecolor='white', alpha=0.9, edgecolor='black'),horizontalalignment='right', fontsize = '12')
plt.text(wn.get_node('PP48').coordinates[0]-600,wn.get_node('PP48').coordinates[1]+500,s = 'PP48', bbox=dict(facecolor='white', alpha=0.9, edgecolor='black'),horizontalalignment='right', fontsize = '12')
plt.text(wn.get_node('SP13').coordinates[0]+1200,wn.get_node('SP13').coordinates[1]+1000,s = 'SP13', bbox=dict(facecolor='white', alpha=0.9, edgecolor='black'),horizontalalignment='right', fontsize = '12')
plt.text(wn.get_node('SP41').coordinates[0]-100,wn.get_node('SP41').coordinates[1]+600,s = 'SP41', bbox=dict(facecolor='white', alpha=0.9, edgecolor='black'),horizontalalignment='right', fontsize = '12')
plt.text(wn.get_node('SP37').coordinates[0]-1100,wn.get_node('SP37').coordinates[1]-300,s = 'SP37', bbox=dict(facecolor='white', alpha=0.9, edgecolor='black'),horizontalalignment='right', fontsize = '12')
plt.text(wn.get_node('SP39').coordinates[0]+1100,wn.get_node('SP39').coordinates[1]+700,s = 'SP39', bbox=dict(facecolor='white', alpha=0.9, edgecolor='black'),horizontalalignment='right', fontsize = '12')
plt.text(wn.get_node('SP38').coordinates[0]+700,wn.get_node('SP38').coordinates[1]+700,s = 'SP38', bbox=dict(facecolor='white', alpha=0.9, edgecolor='black'),horizontalalignment='right', fontsize = '12')
plt.text(wn.get_node('SP36').coordinates[0]+1100,wn.get_node('SP36').coordinates[1]-800,s = 'SP36', bbox=dict(facecolor='white', alpha=0.9, edgecolor='black'),horizontalalignment='right', fontsize = '12')
plt.text(wn.get_node('SP42').coordinates[0]-400,wn.get_node('SP42').coordinates[1]-400,s = 'SP42', bbox=dict(facecolor='white', alpha=0.9, edgecolor='black'),horizontalalignment='right', fontsize = '12')
plt.text(wn.get_node('SP25').coordinates[0]+1100,wn.get_node('SP25').coordinates[1]-800,s = 'SP25', bbox=dict(facecolor='white', alpha=0.9, edgecolor='black'),horizontalalignment='right', fontsize = '12')
plt.text(wn.get_node('SP22').coordinates[0]-200,wn.get_node('SP22').coordinates[1]-1200,s = 'SP22', bbox=dict(facecolor='white', alpha=0.9, edgecolor='black'),horizontalalignment='right', fontsize = '12')
# plot_spl_elements()
# add valves
valve_list = []
for valve_name, valve in wn.valves():
    valve_list.append(valve.start_node_name)
nxp.draw_networkx_nodes(G, pos_dict, nodelist = valve_list, node_size = 200, node_color = 'orange', node_shape = 'P')
plt.axis('off')
fig.savefig(image_path+'/barebones.png')


# In[] for old version
spl_nodes = ['SP38', 'SP39', 'SP22', 'SP42', 'SP37', 'SP25', 'SP13', 'SP41', 'SP36']
fig, ax = plt.subplots(figsize=(15,25))
nxp.draw_networkx_nodes(G, pos_dict, node_size = 0, label = None)
nxp.draw_networkx_nodes(G, pos_dict, nodelist = wn.reservoir_name_list, node_size = 200, node_color = 'k', node_shape = 's')
nxp.draw_networkx_nodes(G, pos_dict, nodelist = wn.tank_name_list, node_size = 200, node_color = 'b', node_shape = 'h')
nxp.draw_networkx_nodes(G, pos_dict, nodelist = spl_nodes, node_size = 200, node_color = 'r')
nxp.draw_networkx_edges(G, pos_dict, arrows = False, edge_color = 'k', width = 1.5)
plt.text(wn.get_node('AM9001').coordinates[0]-500,wn.get_node('AM9001').coordinates[1],s = 'Anderson Mill R + T + PS', bbox=dict(facecolor='mediumaquamarine', alpha=0.9, edgecolor='black'),horizontalalignment='right', fontsize = '15')
plt.text(wn.get_node('FP9001').coordinates[0],wn.get_node('FP9001').coordinates[1]-1400,s = 'Four Points R + T + PS', bbox=dict(facecolor='mediumaquamarine', alpha=0.9, edgecolor='black'),horizontalalignment='left', fontsize = '15')
plt.text(wn.get_node('104158').coordinates[0]-400,wn.get_node('104158').coordinates[1]-500,s = 'GL Tank', bbox=dict(facecolor='mediumaquamarine', alpha=0.9, edgecolor='black'),horizontalalignment='right', fontsize = '15')
plt.text(wn.get_node('STC9001').coordinates[0]-400,wn.get_node('STC9001').coordinates[1]+500,s = 'STC Tank', bbox=dict(facecolor='mediumaquamarine', alpha=0.9, edgecolor='black'),horizontalalignment='right', fontsize = '15')
plt.text(wn.get_node('PP35').coordinates[0]-300,wn.get_node('PP35').coordinates[1]-800,s = 'PP35', bbox=dict(facecolor='white', alpha=0.9, edgecolor='black'),horizontalalignment='right', fontsize = '12')
plt.text(wn.get_node('PP48').coordinates[0]-600,wn.get_node('PP48').coordinates[1]+500,s = 'PP48', bbox=dict(facecolor='white', alpha=0.9, edgecolor='black'),horizontalalignment='right', fontsize = '12')
plt.text(wn.get_node('SP13').coordinates[0]+1200,wn.get_node('SP13').coordinates[1]+1000,s = 'SP13', bbox=dict(facecolor='white', alpha=0.9, edgecolor='black'),horizontalalignment='right', fontsize = '12')
plt.text(wn.get_node('SP41').coordinates[0]-100,wn.get_node('SP41').coordinates[1]+600,s = 'SP41', bbox=dict(facecolor='white', alpha=0.9, edgecolor='black'),horizontalalignment='right', fontsize = '12')
plt.text(wn.get_node('SP37').coordinates[0]-1100,wn.get_node('SP37').coordinates[1]-300,s = 'SP37', bbox=dict(facecolor='white', alpha=0.9, edgecolor='black'),horizontalalignment='right', fontsize = '12')
plt.text(wn.get_node('SP39').coordinates[0]+1100,wn.get_node('SP39').coordinates[1]+700,s = 'SP39', bbox=dict(facecolor='white', alpha=0.9, edgecolor='black'),horizontalalignment='right', fontsize = '12')
plt.text(wn.get_node('SP38').coordinates[0]+700,wn.get_node('SP38').coordinates[1]+700,s = 'SP38', bbox=dict(facecolor='white', alpha=0.9, edgecolor='black'),horizontalalignment='right', fontsize = '12')
plt.text(wn.get_node('SP36').coordinates[0]+1100,wn.get_node('SP36').coordinates[1]-800,s = 'SP36', bbox=dict(facecolor='white', alpha=0.9, edgecolor='black'),horizontalalignment='right', fontsize = '12')
plt.text(wn.get_node('SP42').coordinates[0]-400,wn.get_node('SP42').coordinates[1]-400,s = 'SP42', bbox=dict(facecolor='white', alpha=0.9, edgecolor='black'),horizontalalignment='right', fontsize = '12')
plt.text(wn.get_node('SP25').coordinates[0]+1100,wn.get_node('SP25').coordinates[1]-800,s = 'SP25', bbox=dict(facecolor='white', alpha=0.9, edgecolor='black'),horizontalalignment='right', fontsize = '12')
plt.text(wn.get_node('SP22').coordinates[0]-200,wn.get_node('SP22').coordinates[1]-1200,s = 'SP22', bbox=dict(facecolor='white', alpha=0.9, edgecolor='black'),horizontalalignment='right', fontsize = '12')
# plot_spl_elements()
# add valves
valve_list = []
for valve_name, valve in wn.valves():
    valve_list.append(valve.start_node_name)
nxp.draw_networkx_nodes(G, pos_dict, nodelist = valve_list, node_size = 200, node_color = 'orange', node_shape = 'P')
plt.axis('off')
fig.savefig(image_path+'/barebones.png')
