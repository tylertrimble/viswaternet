# Import libraries
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
import os

# Define .INP file name
dirname = os.path.dirname(__file__)
inp_file = os.path.join(dirname, 'Networks', 'CTown.inp')

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

image_path = os.path.join(dirname, 'Images')

def plot_spl_elements(size_of_font, type_of_graph):
    if type_of_graph == "continuous":
        size_of_font = size_of_font - 4
    
    nxp.draw_networkx_nodes(G, pos_dict, nodelist = wn.reservoir_name_list, node_size = 200, node_color = 'k', node_shape = 's')
    nxp.draw_networkx_nodes(G, pos_dict, nodelist = wn.tank_name_list, node_size = 200, node_color = 'b', node_shape = 'h')
    plt.text(wn.get_node('R1').coordinates[0]+450,wn.get_node('R1').coordinates[1]+75,s = 'Resevoir 1', bbox=dict(facecolor='mediumaquamarine', alpha=0.9, edgecolor='black'),horizontalalignment='right', fontsize = size_of_font)
    plt.text(wn.get_node('T1').coordinates[0]+125,wn.get_node('T1').coordinates[1]+75,s = 'Tank 1', bbox=dict(facecolor='mediumaquamarine', alpha=0.9, edgecolor='black'),horizontalalignment='right', fontsize = size_of_font)
    plt.text(wn.get_node('T2').coordinates[0]+175,wn.get_node('T2').coordinates[1]-125,s = 'Tank 2', bbox=dict(facecolor='mediumaquamarine', alpha=0.9, edgecolor='black'),horizontalalignment='right', fontsize = size_of_font)
    plt.text(wn.get_node('T3').coordinates[0],wn.get_node('T3').coordinates[1]-100,s = 'Tank 3', bbox=dict(facecolor='mediumaquamarine', alpha=0.9, edgecolor='black'),horizontalalignment='right', fontsize = size_of_font)
    plt.text(wn.get_node('T4').coordinates[0]+350,wn.get_node('T4').coordinates[1]+75,s = 'Tank 4', bbox=dict(facecolor='mediumaquamarine', alpha=0.9, edgecolor='black'),horizontalalignment='right', fontsize = size_of_font)
    plt.text(wn.get_node('T5').coordinates[0]+100,wn.get_node('T5').coordinates[1]+75,s = 'Tank 5', bbox=dict(facecolor='mediumaquamarine', alpha=0.9, edgecolor='black'),horizontalalignment='right', fontsize = size_of_font)
    plt.text(wn.get_node('T6').coordinates[0]+200,wn.get_node('T6').coordinates[1]+75,s = 'Tank 6', bbox=dict(facecolor='mediumaquamarine', alpha=0.9, edgecolor='black'),horizontalalignment='right', fontsize = size_of_font)
    plt.text(wn.get_node('T7').coordinates[0]+100,wn.get_node('T7').coordinates[1]+75,s = 'Tank 7', bbox=dict(facecolor='mediumaquamarine', alpha=0.9, edgecolor='black'),horizontalalignment='right', fontsize = size_of_font)
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


for i in range(len(spl_nodes)):
    spl_nodes_dict[spl_nodes[i]] = spl_nodes[i]


# In[] 1. NODE DEMANDS (distinct)

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


fig, ax = plt.subplots(figsize=(15,25))
nxp.draw_networkx_nodes(G, pos_dict, nodelist = dem10, node_size = 30, node_color = cmap(float(1/6)), label = '0 - 2')
nxp.draw_networkx_nodes(G, pos_dict, nodelist = dem20, node_size = 50, node_color = cmap(float(2/6)), label = '2 - 4')
nxp.draw_networkx_nodes(G, pos_dict, nodelist = dem30, node_size = 70, node_color = cmap(float(3/6)), label = '4 - 10')
nxp.draw_networkx_nodes(G, pos_dict, nodelist = dem40, node_size = 90, node_color = cmap(float(4/6)), label = '10 - 20')
nxp.draw_networkx_nodes(G, pos_dict, nodelist = dem50, node_size = 120, node_color = cmap(float(5/6)), label = '20 - 40')
nxp.draw_networkx_nodes(G, pos_dict, nodelist = dem60, node_size = 200, node_color = cmap(1.0), label = '> 40')

nxp.draw_networkx_edges(G, pos_dict, arrows = False, edge_color = 'k')
plot_spl_elements(15, "discrete")

plt.axis('off')
plt.legend(scatterpoints = 1, title = 'Demand [GPM]', loc = 'lower right', fontsize = '15', title_fontsize = '17')
fig.savefig(image_path+'/demands.png')


# In[] 2. NODE ELEVATIONS (continuous)

junc_list = []
elevations = []

for junc_name, junc in wn.junctions():
    elevations.append(3.28084*junc.elevation)
    junc_list.append(junc_name)
    
fig, ax = plt.subplots(figsize=(15,25))
nodes = nxp.draw_networkx_nodes(G, pos_dict, nodelist = junc_list, node_size = 40, node_color = elevations, cmap = cmap)
nxp.draw_networkx_edges(G, pos_dict, arrows = False, edge_color = 'k')

plot_spl_elements(15, "continuous")

valve_list = []
for valve_name, valve in wn.valves():
    valve_list.append(valve.start_node_name)
nxp.draw_networkx_nodes(G, pos_dict, nodelist = valve_list, node_size = 200, node_color = 'orange', node_shape = 'P')

cbar = plt.colorbar(nodes)
cbar.set_label('Junction elevation [ft]', fontsize = 15)
plt.axis('off')
plt.savefig(image_path+'/elevations.png') 


# In[] AVERAGE PRESSURE (distinct + continuous)

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
    

fig, ax = plt.subplots(figsize=(15,25))
nodes = nxp.draw_networkx_nodes(G, pos_dict, nodelist = junc_list, node_size = 40, node_color = avg_pres, cmap = cmap)
nxp.draw_networkx_nodes(G, pos_dict, nodelist = pres_90_nodes, node_size = 80, node_color = 'k')
nxp.draw_networkx_nodes(G, pos_dict, nodelist = pres_90_nodes, node_size = 40, node_color = 'crimson')
nxp.draw_networkx_edges(G, pos_dict, arrows = False, edge_color = 'k')
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


# In[] WATER AGE AVERAGE

# Extracting from WNTR
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

# Plotting
fig, ax = plt.subplots(figsize=(15,25))
nodes = nxp.draw_networkx_nodes(G, pos_dict, nodelist = junc_list, node_size = 40, node_color = water_age, cmap = cmap)
nxp.draw_networkx_edges(G, pos_dict, arrows = False, edge_color = 'k')
plot_spl_elements()

cbar = plt.colorbar(nodes)
cbar.set_label('Average water age at each junction [hr]', fontsize = 15)
plt.axis('off')
plt.savefig(image_path+'/avg water age.png') 

# In[] WATER AGE MAX

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
    nxp.draw_networkx_edges(G, pos_dict, arrows = False, edge_color = 'k')
    
    plot_spl_elements()
    cbar = plt.colorbar(nodes)
    cbar.set_label('Maximum daily percentage of water sourced from Reservoir {} for 24 hr duration'.format(res_name), fontsize = 15)
    plt.axis('off')
    plt.savefig(image_path+'/Tracer plots/res {} tracer 24 hrs.png'.format(res_name))
    

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
    nxp.draw_networkx_edges(G, pos_dict, arrows = False, edge_color = 'k')
    
    plot_spl_elements()
    cbar = plt.colorbar(nodes)
    cbar.set_label('Maximum daily percentage of water sourced from Tank {} for 24 hr duration'.format(tank_name), fontsize = 15)
    plt.axis('off')
    plt.savefig(image_path+'/Tracer plots/tank {} tracer 24 hrs.png'.format(tank_name))
    
    

# In[]
for tank_name, tank in wn.tanks():
    trace_node = tank_name
    wn.options.quality.parameter = 'TRACE'
    wn.options.quality.trace_node = trace_node
    sim_am9001 = wntr.sim.EpanetSimulator(wn)
    results_am9001 = sim_am9001.run_sim()
    tracer_am9001 = results_am9001.node['quality'].loc[:, '72838']
    # fig, ax=plt.subplots(figsize = (8,12))

for tank_name, tank in wn.reservoirs():
    trace_node = tank_name
    wn.options.quality.parameter = 'TRACE'
    wn.options.quality.trace_node = trace_node
    sim_am9001 = wntr.sim.EpanetSimulator(wn)
    results_am9001 = sim_am9001.run_sim()
    tracer_am9001 = results_am9001.node['quality'].loc[:, '72838']
    # fig, ax=plt.subplots(figsize = (8,12))

    
for tank_name, tank in wn.tanks():
    trace_node = tank_name
    wn.options.quality.parameter = 'TRACE'
    wn.options.quality.trace_node = trace_node
    sim_am9001 = wntr.sim.EpanetSimulator(wn)
    results_am9001 = sim_am9001.run_sim()
    tracer_am9001 = results_am9001.node['quality'].loc[:, '786631']
    # fig, ax=plt.subplots(figsize = (8,12))

for tank_name, tank in wn.reservoirs():
    trace_node = tank_name
    wn.options.quality.parameter = 'TRACE'
    wn.options.quality.trace_node = trace_node
    sim_am9001 = wntr.sim.EpanetSimulator(wn)
    results_am9001 = sim_am9001.run_sim()
    tracer_am9001 = results_am9001.node['quality'].loc[:, '786631']
    # fig, ax=plt.subplots(figsize = (8,12))

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

    
for tank_name, tank in wn.reservoirs():
    trace_node = tank_name
    wn.options.quality.parameter = 'TRACE'
    wn.options.quality.trace_node = trace_node
    sim_am9001 = wntr.sim.EpanetSimulator(wn)
    results_am9001 = sim_am9001.run_sim()
    tracer_am9001 = results_am9001.node['quality'].loc[:, '72838']
    # fig, ax=plt.subplots(figsize = (8,12))

for tank_name, tank in wn.tanks():
    trace_node = tank_name
    wn.options.quality.parameter = 'TRACE'
    wn.options.quality.trace_node = trace_node
    sim_am9001 = wntr.sim.EpanetSimulator(wn)
    results_am9001 = sim_am9001.run_sim()
    tracer_am9001 = results_am9001.node['quality'].loc[:, '786631']
    # fig, ax=plt.subplots(figsize = (8,12))

    
for tank_name, tank in wn.reservoirs():
    trace_node = tank_name
    wn.options.quality.parameter = 'TRACE'
    wn.options.quality.trace_node = trace_node
    sim_am9001 = wntr.sim.EpanetSimulator(wn)
    results_am9001 = sim_am9001.run_sim()
    tracer_am9001 = results_am9001.node['quality'].loc[:, '786631']
    # fig, ax=plt.subplots(figsize = (8,12))

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
    nxp.draw_networkx_edges(G, pos_dict, arrows = False, edge_color = 'k')
    
    plot_spl_elements()
    cbar = plt.colorbar(nodes)
    cbar.set_label('Maximum daily percentage of water sourced from Reservoir {} for 72 hr duration'.format(res_name), fontsize = 15)
    plt.axis('off')
    plt.savefig(image_path+'/Tracer plots/res {} tracer 72 hrs.png'.format(res_name))
    
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
    nxp.draw_networkx_edges(G, pos_dict, arrows = False, edge_color = 'k')
    
    plot_spl_elements()
    cbar = plt.colorbar(nodes)
    cbar.set_label('Maximum daily percentage of water sourced from Tank {} for 72 hr duration'.format(tank_name), fontsize = 15)
    plt.axis('off')
    plt.savefig(image_path+'/Tracer plots/tank {} tracer 72 hrs.png'.format(tank_name))
    

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
        nxp.draw_networkx_edges(G, pos_dict, arrows = False, edge_color = 'k')
        
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
        nxp.draw_networkx_edges(G, pos_dict, arrows = False, edge_color = 'k')
        
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
plot_spl_elements()
# add valves
valve_list = []
for valve_name, valve in wn.valves():
    valve_list.append(valve.start_node_name)
nxp.draw_networkx_nodes(G, pos_dict, nodelist = valve_list, node_size = 200, node_color = 'orange', node_shape = 'P')
plt.axis('off')
fig.savefig(image_path+'/barebones.png')

