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
    """Determines if demand pattern of node is the one specified, then stores 
    it with the apropriate dictionary key.
    Arguments:
    nodePattern: The demand pattern of the node
    pattern: Which pattern the node demand pattern is being checked against
    junc_name: Name of node/junction being checked
    demandPatternNodes: Name of demand pattern dictionary"""
    if nodePattern == pattern:
        demandPatternNodes[pattern][junc_name] = junc_name
    return demandPatternNodes




def initializeModel(inp_file):
    """Initializes all variables needed to perform other plotting functions
    Arguments:
    inp_file: Network input file. Ends with .inp"""
    model = {}
    dirname = os.path.dirname(__file__)
    inp_file = os.path.join(dirname, 'Networks', inp_file)
    model['inp_file'] = inp_file
    image_path = os.path.join(dirname, 'Images')
    model['image_path'] = image_path
    
    # Run hydraulic simulation and store results
    wn = wntr.network.WaterNetworkModel(inp_file)
    model['wn'] = wn
    sim = wntr.sim.EpanetSimulator(wn)
    model['sim'] = sim
    results = sim.run_sim()
    model['results'] = results
    
    # Create name lists for easy reference
    junc_names = wn.junction_name_list
    valve_names = wn.valve_name_list
    tank_names = wn.tank_name_list
    node_names = wn.node_name_list
    model['junc_names'] = junc_names
    model['valve_names'] = valve_names
    model['tank_names'] = tank_names
    model['node_names'] = node_names
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
    model['G'] = G
    G_edge_list = list(G.edges())
    model['G_edge_list'] = G_edge_list
    inc_mat = sp.csr_matrix.toarray(nx.incidence_matrix(G,nodelist = node_names, oriented=True))
    inc_mat_no = sp.csr_matrix.toarray(nx.incidence_matrix(G,nodelist = node_names, edgelist = new_pipes_list, oriented=False))
    adj_mat = sp.csr_matrix.toarray(nx.adjacency_matrix(G,nodelist = node_names))
    
    pos_dict = {}
    for i in range(len(node_names)):
        pos_dict[node_names[i]] = wn.get_node(node_names[i]).coordinates
    model['pos_dict'] = pos_dict
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
    model['G_pipe_name_list'] = G_pipe_name_list
    model['G_list_pipes_only'] = G_list_pipes_only  
    model['G_list_pumps_only'] = G_list_pumps_only  
    model['G_list_valves_only'] = G_list_valves_only  
    model['G_pipe_index'] = G_pipe_index  
    model['pipe_list_names'] = pipe_list_names                   
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
        
    return model




def createBasicPlot(model, savefig=False):
    """Creates a basic plot, similar to the default seen in EPANET.
    Arguments:
    model: Saved initilization done with initializeModel
    savefig: Boolean. Determines whether plot is saved to /Images directory"""
    fig, ax = plt.subplots(figsize=(15,25))
    nxp.draw_networkx_nodes(model['G'], model['pos_dict'], node_size = 30, node_color = 'k')
    nxp.draw_networkx_nodes(model['G'], model['pos_dict'], nodelist = model['wn'].reservoir_name_list, node_size = 200, node_color = 'black',linewidths=3,node_shape = 's')
    nxp.draw_networkx_nodes(model['G'], model['pos_dict'], nodelist = model['wn'].tank_name_list, node_size = 200, node_color = 'black',linewidths=3, node_shape = 'd')
    nxp.draw_networkx_edges(model['G'], model['pos_dict'], arrows = False, edge_color = 'k')
    if savefig == True:
        if model['inp_file'].endswith('.inp'):
            prefixRemove = len(model['image_path']) + 3
            model['inp_file'] = model['inp_file'][prefixRemove:-4]
        image_path2 = '/Basic' + model['inp_file'] + '.png'
        plt.savefig(model['image_path']+image_path2) 
    
    
    

def createFlowRatePlot(model, savefig=False, animation=None):
    """Creates a plot showing flow rate. For now only includes average flow 
    rate. However, creating a gif showing the change over time is possible.
    Arguments:
    model: Saved initilization done with initializeModel
    savefig: Boolean. Determines whether plot is saved to /Images directory"""
    fig, ax = plt.subplots(figsize=(15,25))
    
    flow_rates = []
    for i in range(len(model['pipe_list_names'])-1):
        flow_rates.append(np.average(model['results'].link['flowrate'].iloc[:,i]).item())
    max_flow_rate = np.max(flow_rates)
    min_flow_rate = np.min(flow_rates)
    
    normalized_flow_rates = np.copy(flow_rates)
    norm = mc.Normalize(vmin=min_flow_rate, vmax=max_flow_rate, clip=True)
    mapper = mpl.cm.ScalarMappable(norm=norm, cmap=mpl.cm.Blues)
    counter = 0
    for flow_rate in flow_rates:
        normalized_flow_rates[counter] = (flow_rate - min_flow_rate)/(max_flow_rate - min_flow_rate)
        counter += 1
    widths = normalized_flow_rates*5
    nxp.draw_networkx_nodes(model['G'], model['pos_dict'], node_size = 30, node_color = 'k')
    nxp.draw_networkx_nodes(model['G'], model['pos_dict'], nodelist = model['wn'].reservoir_name_list, node_size = 200, node_color = 'black',linewidths=3,node_shape = 's')
    nxp.draw_networkx_nodes(model['G'], model['pos_dict'], nodelist = model['wn'].tank_name_list, node_size = 200, node_color = 'black',linewidths=3, node_shape = 'd')
    g = nxp.draw_networkx_edges(model['G'], model['pos_dict'], edgelist = model['G_list_pipes_only'], edge_color = mapper.to_rgba(flow_rates), width = widths, edge_cmap = mpl.cm.Blues, arrows = False)
    cbar = plt.colorbar(g)
    cbar.set_label('Pipe FlowRate', fontsize = 15)
    
def createDemandPatternPlot(model, savefig=False):   
    """Creates a plot showing demand pattern groups. By default also shows
    resevoirs, tanks, pipes, and valves. 
    Arguments:
    model: Saved initilization done with initializeModel
    savefig: Boolean. Determines whether plot is saved to /Images directory"""
    cmap = mpl.cm.get_cmap('tab10')
    valve_coordinates = {}
    valveCounter = 0
    for point1, point2 in model['G_list_valves_only']:
        midpoint = [(model['wn'].get_node(point1).coordinates[0] + model['wn'].get_node(point2).coordinates[0])/2,(model['wn'].get_node(point1).coordinates[1] + model['wn'].get_node(point2).coordinates[1])/2]
        valve_coordinates[model['valve_names'][valveCounter]] = midpoint
        valveCounter += 1
    fig, ax = plt.subplots(figsize=(15,25))
    demandPatterns = []
    patterns = model['wn'].pattern_name_list
    patterns = np.append(patterns, 'None')
    for junction in model['junc_names']:
        try:
            demandPattern = model['wn'].get_node(junction).demand_timeseries_list[0].pattern.name
            demandPatterns = np.append(demandPatterns, demandPattern)
        except AttributeError:
            demandPatterns = np.append(demandPatterns, 'None')
    demandPatternNodes = {}
    for pattern in patterns:
        demandPatternNodes[pattern] = {}
        
    for i in range(len(model['junc_names'])):
        for pattern in patterns:
            demandPatternNodes = patternMatch(demandPatterns[i],pattern,model['junc_names'][i],demandPatternNodes)

    if len(demandPatternNodes['None']) == 0:
        patterns = np.delete(patterns,len(patterns)-1)
        del demandPatternNodes['None']
         
    cmapValue = 1/6
    for pattern in patterns:
        nxp.draw_networkx_nodes(model['G'], model['pos_dict'], nodelist = demandPatternNodes.get(pattern).values(), node_size = 100, node_color = cmap(float(cmapValue)))
        cmapValue += 1/6
        
    nxp.draw_networkx_nodes(model['G'], model['pos_dict'], nodelist = model['wn'].reservoir_name_list, node_size = 200, node_color = 'white', edgecolors='red',linewidths=3,node_shape = 's', label="Resevoir")
    nxp.draw_networkx_nodes(model['G'], model['pos_dict'], nodelist = model['wn'].tank_name_list, node_size = 200, node_color = 'white', edgecolors='blue',linewidths=3, node_shape = 's', label="Tanks")
    nxp.draw_networkx_nodes(model['G'], valve_coordinates, nodelist = model['valve_names'], node_size = 200, node_color = 'orange', edgecolors='black',linewidths=1,node_shape = 'P', label="Valves")
    
    nxp.draw_networkx_edges(model['G'], model['pos_dict'], edgelist = model['G_list_pumps_only'], node_size = 200, edge_color = 'b', width=3)
    
    patch1 = mpatches.Patch(color='blue', label='Pumps')
    patch2 = mpatches.Patch(color='black', label='Pipes')
    nxp.draw_networkx_edges(model['G'], model['pos_dict'], arrows = False, edge_color = 'k')
    
    handles, labels = ax.get_legend_handles_labels()
    handles.extend([patch1,patch2])
    
    legend1 = plt.legend(title='Demand Patterns',labels=patterns, loc='lower right',fontsize = '15', title_fontsize = '17')
    legend2 = plt.legend(title='Node Types', handles=handles, loc='upper right',fontsize = '15', title_fontsize = '17')
    ax.add_artist(legend1)
    ax.add_artist(legend2)
    if savefig == True:
        if model['inp_file'].endswith('.inp'):
            prefixRemove = len(model['image_path']) + 3
            model['inp_file'] = model['inp_file'][prefixRemove:-4]
        image_path2 = '/DemandPatterns' + model['inp_file'] + '.png'
        plt.savefig(model['image_path']+image_path2) 