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
import math

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

def binParameter(parameterResults,binList):
    if binList == 'Automatic':
        bins=math.floor(math.pow(len(parameterResults),1/3))
        binList = np.linspace(np.min(parameterResults),np.max(parameterResults),bins)
    binnedParameter = {}
    binNames = []
    junctionNames = list(parameterResults.index)
    for i in range(len(binList)):
        
        if i == 0:
            binNames = np.append(binNames, '< ' + str(binList[i]))
            binNames = np.append(binNames, str(binList[i]) + ' - ' + str(binList[i+1]))
        elif i == len(binList)-1:
            binNames = np.append(binNames, '> ' + str(binList[i]))

        else:
            binNames = np.append(binNames, str(binList[i]) + ' - ' + str(binList[i+1]))
    for binName in binNames:
        binnedParameter[binName] = {}
    for i in range(len(binList)):
        
        if i == 0:
            counter = 0
            for parameter in parameterResults:
                if parameter < binList[i]:
                    binnedParameter['< ' + str(binList[i])][junctionNames[counter]] = junctionNames[counter]
                if parameter >= binList[i] and parameter < binList[i+1]:
                        binnedParameter[str(binList[i]) + ' - ' + str(binList[i+1])][junctionNames[counter]] = junctionNames[counter]
                counter += 1
        elif i == len(binList)-1:
            counter = 0
            for parameter in parameterResults:
                if parameter > binList[i]:
                    binnedParameter['> ' + str(binList[i])][junctionNames[counter]] = junctionNames[counter]
                counter += 1
        else:
            counter = 0
            for parameter in parameterResults:
                if parameter >= binList[i] and parameter < binList[i+1]:
                        binnedParameter[str(binList[i]) + ' - ' + str(binList[i+1])][junctionNames[counter]] = junctionNames[counter]
                counter += 1
    for binName in binNames:
        if len(binnedParameter[binName]) == 0:
            binNames = np.delete(binNames,np.where(binNames == binName))
            del binnedParameter[binName]
    print(binNames)
    return binnedParameter, binNames
            
def drawLegend(ax,title='Node Types',pumps=True,loc='upper right'):
    handles, labels = ax.get_legend_handles_labels()
    if pumps == True:
        patch1 = mpatches.Patch(color='blue', label='Pumps')
        patch2 = mpatches.Patch(color='black', label='Pipes')
        handles.extend([patch1,patch2])
    
    else:
        patch = mpatches.Patch(color='black', label='Pipes')
        handles.extend([patch])
    
    legend = plt.legend(title=title,handles=handles, loc=loc,fontsize = '15', title_fontsize = '17')
    ax.add_artist(legend)


def drawSpecialLegend(ax,binList,title=None,loc='lower right'):
    handles, labels = ax.get_legend_handles_labels()
    legend = plt.legend(title=title,handles=handles[len(labels) - len(binList):], loc=loc,fontsize = '15', title_fontsize = '17')
    ax.add_artist(legend)
    
    
def drawDistinctNodes(model,nodes, binList, cmap='tab10', legend=True, legendtitle=None, legendLoc='lower right'):
    cmap = mpl.cm.get_cmap(cmap)
    cmapValue = 1/len(binList)
    global ax
    for binName in binList:
        nxp.draw_networkx_nodes(model['G'], model['pos_dict'], nodelist = nodes.get(binName).values(), node_size = 100, node_color = cmap(float(cmapValue)), label=binName)
        cmapValue += 1/len(binList)
        
    if legend == True:
        drawSpecialLegend(ax,binList,title=legendtitle,loc=legendLoc)
    handles, labels = ax.get_legend_handles_labels()       
        
    
def drawBaseElements(model,resevoirs=True,tanks=True,pumps=True,valves=True,legend=True):
    nxp.draw_networkx_nodes(model['G'], model['pos_dict'], node_size = 30, node_color = 'k')
    
    if resevoirs == True:
        nxp.draw_networkx_nodes(model['G'], model['pos_dict'], nodelist = model['wn'].reservoir_name_list, node_size = 200, node_color = 'black',linewidths=3,node_shape = 's', label='Resevoirs')
    
    if tanks == True:
        nxp.draw_networkx_nodes(model['G'], model['pos_dict'], nodelist = model['wn'].tank_name_list, node_size = 200, node_color = 'black',linewidths=3, node_shape = 'd', label='Tanks')
   
    if valves == True:
        valve_coordinates = {}
        valveCounter = 0
        for point1, point2 in model['G_list_valves_only']:
            midpoint = [(model['wn'].get_node(point1).coordinates[0] + model['wn'].get_node(point2).coordinates[0])/2,(model['wn'].get_node(point1).coordinates[1] + model['wn'].get_node(point2).coordinates[1])/2]
            valve_coordinates[model['valve_names'][valveCounter]] = midpoint
            valveCounter += 1
        nxp.draw_networkx_nodes(model['G'], valve_coordinates, nodelist = model['valve_names'], node_size = 200, node_color = 'orange', edgecolors='black',linewidths=1,node_shape = 'P', label='Valves')
        
    nxp.draw_networkx_edges(model['G'], model['pos_dict'], arrows = False, edge_color = 'k')
    
    if pumps == True:
        nxp.draw_networkx_edges(model['G'], model['pos_dict'], edgelist = model['G_list_pumps_only'], node_size = 200, edge_color = 'b', width=3)  
        
    if legend == True:
        global ax
        drawLegend(ax,pumps=pumps)      
def getParameter(model,parameter):
    try:
        parameterResults = model['results'].node[parameter]
        return parameterResults
    except KeyError:
        parameterResults = model['wn'].query_node_attribute('elevation')
        return parameterResults

def getDemandPatterns(model):
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
    for pattern in patterns:
        if len(demandPatternNodes[pattern]) == 0:
            patterns = np.delete(patterns,np.where(patterns == pattern))
            del demandPatternNodes[pattern]
    return demandPatternNodes, patterns
    
    
def saveFig(model, saveName=None):
    if model['inp_file'].endswith('.inp'):
        prefixRemove = len(model['image_path']) + 3
        model['inp_file'] = model['inp_file'][prefixRemove:-4]
    image_path2 = '/' + str(saveName) + model['inp_file'] + '.png'
    plt.savefig(model['image_path']+image_path2)
    
    
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




def createBasicPlot(model, savefig=False, saveName=None):
    """Creates a basic plot, similar to the default seen in EPANET.
    Arguments:
    model: Saved initilization done with initializeModel
    savefig: Boolean. Determines whether plot is saved to /Images directory"""
    global fig,ax
    fig, ax = plt.subplots(figsize=(15,25))
    
    drawBaseElements(model,pumps=False,legend=True)
    if savefig == True:
        saveFig(model, saveName=saveName)
    

def createFlowRatePlot(model, savefig=False, animation=None):
    """Creates a plot showing flow rate. For now only includes average flow 
    rate. However, creating a gif showing the change over time is possible.
    Arguments:
    model: Saved initilization done with initializeModel
    savefig: Boolean. Determines whether plot is saved to /Images directory"""
    fig, ax = plt.subplots(figsize=(15,25))
    
    flow_rates = []
    for i in range(len(model['G_edge_list'])):
        flow_rates.append(np.average(model['results'].link['flowrate'].iloc[:,i]))
    flow_rates = from_si(FlowUnits.GPM, flow_rates, HydParam.Flow)
    max_flow_rate = np.max(flow_rates)
    min_flow_rate = np.min(flow_rates)
    normalized_flow_rates = np.copy(flow_rates)

    counter = 0
    for flow_rate in flow_rates:
        normalized_flow_rates[counter] = (flow_rate - min_flow_rate)/(max_flow_rate - min_flow_rate)
        counter += 1
    widths = normalized_flow_rates*5
    nxp.draw_networkx_nodes(model['G'], model['pos_dict'], node_size = 30, node_color = 'k')
    nxp.draw_networkx_nodes(model['G'], model['pos_dict'], nodelist = model['wn'].reservoir_name_list, node_size = 200, node_color = 'black',linewidths=3,node_shape = 's')
    nxp.draw_networkx_nodes(model['G'], model['pos_dict'], nodelist = model['wn'].tank_name_list, node_size = 200, node_color = 'black',linewidths=3, node_shape = 'd')
    g = nxp.draw_networkx_edges(model['G'], model['pos_dict'], edgelist = model['G_edge_list'], edge_color = flow_rates, width = widths, edge_cmap = mpl.cm.Reds, arrows = False)
    cbar = plt.colorbar(g)
    cbar.set_label('Pipe FlowRate (GPM)', fontsize = 15)
    if savefig == True:
        if model['inp_file'].endswith('.inp'):
            prefixRemove = len(model['image_path']) + 3
            model['inp_file'] = model['inp_file'][prefixRemove:-4]
        image_path2 = '/FlowRate' + model['inp_file'] + '.png'
        plt.savefig(model['image_path']+image_path2) 
   
    
def createDemandPatternPlot(model, savefig=True, saveName=None):   
    """Creates a plot showing demand pattern groups. By default also shows
    resevoirs, tanks, pipes, and valves. 
    Arguments:
    model: Saved initilization done with initializeModel
    savefig: Boolean. Determines whether plot is saved to /Images directory"""
    global fig,ax
    fig, ax = plt.subplots(figsize=(15,25))
    
    demandPatternNodes,patterns = getDemandPatterns(model)
    drawBaseElements(model)  
    drawDistinctNodes(model,demandPatternNodes,patterns,legendtitle='Demand Patterns')

    if savefig == True:
         saveFig(model, saveName=saveName)

def plotDistinctNodes(model, parameter=None,bins='Automatic', savefig=True, legendTitle = None, saveName=None):
    global fig,ax
    fig, ax = plt.subplots(figsize=(15,25))
    parameterResults = getParameter(model,parameter)
    binnedResults,binNames = binParameter(parameterResults,binList='Automatic')
    drawBaseElements(model)
    drawDistinctNodes(model,binnedResults,binNames,legendtitle=legendTitle)
    
    if savefig == True:
         saveFig(model,saveName=saveName)