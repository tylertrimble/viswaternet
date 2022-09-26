import warnings
warnings.filterwarnings("ignore")
import wntr
import numpy as np
import matplotlib.pyplot as plt
import networkx.drawing.nx_pylab as nxp
import matplotlib as mpl
import matplotlib.patches as mpatches
import os
import pandas as pd
import imageio

default_cmap = mpl.cm.get_cmap('autumn_r')


def initialize_model(inp_file):
    """Initializes all variables needed to perform other plotting functions
        Arguments:
    inp_file: Takes a string. Directorty location of network input file. Ends with .inp"""
    
    
# =============================================================================
#   Initilize model dictionary. Get directory code is stored in to set input
#   file and saved images path
# =============================================================================
    model = {}
    dirname = os.path.dirname(__file__)
    inp_file = os.path.join(dirname, inp_file)
    model['inp_file'] = inp_file
    image_path = os.path.join(dirname)
    model['image_path'] = image_path
    
    
    # Run hydraulic simulation and store results
    wn = wntr.network.WaterNetworkModel(inp_file)
    model['wn'] = wn
    sim = wntr.sim.EpanetSimulator(wn)
    model['sim'] = sim
    
    
    results = sim.run_sim()
    model['results'] = results
    

# =============================================================================
#   Create name lists for easy reference
#   junc_names excludes resevoirs and tanks 
#   node_names includes all nodes
# =============================================================================
    model['junc_names'] = wn.junction_name_list
    model['valve_names'] = wn.valve_name_list
    model['tank_names'] = wn.tank_name_list
    model['node_names'] = wn.node_name_list
    model['reservoir_names'] = wn.reservoir_name_list
    
    
    #Gets start and end points of all links
    pipe_tp =[]
    pipe_tp2 = []
    
    
    for link_name, link in wn.links():
        
        pipe_tp.append(link.start_node_name)
        pipe_tp2.append(link.end_node_name)
        
        
    pipe_list = list(zip(pipe_tp, pipe_tp2))
    model['pipe_list'] = pipe_list
    
    
    #Creates wntr graph
    G = wn.get_graph()
    model['G'] = G
    
    
    #Gets node coordiantes
    pos_dict = {}
    
    
    for i in range(len(model['node_names'])):
        
        pos_dict[model['node_names'][i]] = wn.get_node(model['node_names'][i]).coordinates
        
        
    model['pos_dict'] = pos_dict
    
    
    #Stores pipe names, pump connections only, and valve connections only
    G_pipe_name_list = []
    G_list_pumps_only = []
    G_list_valves_only = []
    
    
    #Stores pipe names, as well as creating a list of pumps and valves only
    for j in range(len(pipe_tp)):
        
        G_pipe_name_list.append(wn.link_name_list[j])
        
        
        if wn.link_name_list[j] in wn.pump_name_list:
            
            G_list_pumps_only.append(pipe_list[j])
            
            
            continue
        
        
        if wn.link_name_list[j] in wn.valve_name_list:
            
            G_list_valves_only.append(pipe_list[j])
          
            
    model['G_pipe_name_list'] = G_pipe_name_list
    model['G_list_pumps_only'] = G_list_pumps_only  
    model['G_list_valves_only'] = G_list_valves_only    
       
    
    return model




def convert_excel(model,file,data_type,element_index,value_index):
    """Converts an excel file into the correct dictionary structure needed to
    be used with drawing functions.
    Arguments:
    model: Takes dictionary. Uses input file name to give each image a unique
    name.
    file: Takes string. Location in Directory where excel file is located.
    data_type: Takes string. Type of data that is being extracted. Unique data
    is data that is seperated into groups such as pressure groups. Discrete
    data is numerical and is """
    
    if data_type == 'unique':
        element_list= {}
        dirname = os.path.dirname(__file__)
        dataFile = os.path.join(dirname, 'Excel', file)
        
        
        df = pd.read_excel(dataFile,dtype=str)
        bins = pd.unique(df.iloc[:,value_index])
    
    
        for binName in bins:
            
            element_list[binName] = {}
            
            
        for node,data in zip(df.iloc[:,element_index].dropna(),df.iloc[:,value_index].dropna()):
            
            element_list[data][node] = model['G_pipe_name_list'].index(node)
    
    
        return element_list, bins
    
    if data_type == 'continuous' or 'discrete':
        dirname = os.path.dirname(__file__)
        dataFile = os.path.join(dirname, 'Excel', file)
        
        df = pd.read_excel(dataFile)
        element_list = pd.Series(data=df.iloc[:,value_index].values,index=df.iloc[:,element_index].values)
        data = {}
        data['element_list'] = element_list
        data['index'] = list(str(i) for i in list(element_list.index))
        return data

def unit_conversion(parameter_results,parameter,new_unit):
    conversion_factors = {'base_demand':{'LPS':1000,
                                         'LPM':60000,
                                         'MLD':86.4,
                                         'CMH':3600,
                                         'CMD':86400,
                                         'CFS':35.31467,
                                         'GPM':15850.32314,
                                         'MGD':22.82447,
                                         'IMGD':13198.15490,
                                         'AFD':70.04562},
                          'demand':{'LPS':1000,
                                    'LPM':60000,
                                    'MLD':86.4,
                                    'CMH':3600,
                                    'CMD':86400,
                                    'CFS':35.31467,
                                    'GPM':15850.32314,
                                    'MGD':22.82447,
                                    'IMGD':13198.15490,
                                    'AFD':70.04562},
                          'diameter':{'ft':3.28084,
                                      'in:':39.37008,
                                      'cm:':100},
                          'elevation':{'ft':3.28084,
                                      'in:':39.37008,
                                      'cm:':100},
                          'flowrate':{'LPS':1000,
                                      'LPM':60000,
                                      'MLD':86.4,
                                      'CMH':3600,
                                      'CMD':86400,
                                      'CFS':35.31467,
                                      'GPM':15850.32314,
                                      'MGD':22.82447,
                                      'IMGD':13198.15490,
                                      'AFD':70.04562},
                          'head':{'ft':3.28084,
                                      'in:':39.37008,
                                      'cm:':100},
                          'length':{'ft':3.28084,
                                      'in:':39.37008,
                                      'cm:':100},
                          'pressure':{'psi':1.42197},
                          'velocity':{'ft/s':3.28084}}
    parameter_results = parameter_results*conversion_factors[parameter][new_unit]
    return parameter_results
    
    
def save_fig(model, save_name=None):
    """Saves figure to the <file directory>/Images.
    Arguments:
    model: Takes dictionary. Uses input file name to give each image a unique
    name.
    save_name: Takes string. SaveName acts as a prefix for the image file name,
    and is followed by the name of the network."""
    
    networkName = model['inp_file']
    
    
    if networkName.endswith('.inp'):
        
        try:
            
            prefixRemove = networkName.rfind('\\')
            
            
            networkName = networkName[prefixRemove+1:]
            
            
        except Exception:
            
            pass
            
        
        networkName =  networkName[:-4]
    
    
    if save_name is not None:   
        
        image_path2 = '\\' + str(save_name) +  networkName + '.png'
        
        
    else:
        
        image_path2 = '\\' +  networkName + '.png'
    
    
    plt.savefig(model['image_path']+image_path2)
  
    
  
    
def get_parameter(model,parameter_type,parameter,value=None,tanks=False,reservoirs=False):
    """Gets parameter for each node in the network and stores it in
    parameter_results. Also grabs the indices of the nodes that had that
    parameter.
    Arguments:
    model: Takes dictionary. Utilizes network model and results from WNTR to 
    get parameters.
    parameter_type: Takes String. The type of node, can be 'Node' or 'Link'.
    parameter: Takes String. The name of the parameter. 
    value: Takes Integer. Parameters from results must include a value 
    with it. The value given is the value index, not time.
    Takes node parameters: 
        'base_demand'
        'elevation'
    Takes node-value parameters: 
        'pressure'
        'quality'
        'head'
        'demand' 
    Takes link parameters:
        'length'
        'diameter'
        'roughness'
        'minor_loss'
    Takes link-value parameters:
        'velocity'
        'flowrate'
        'headloss'
        'friction_factor'
        'reaction_rate'
        'link_quality'"""
    
    if parameter_type == 'node':
        try:
            
            if value is None:
                
                parameter_results = model['results'].node[parameter]
                element_list = list(parameter_results.index)
                
                
            else:
                if value == 'max':
                    
                    parameter_results = np.max(model['results'].node[parameter])
                    
                    
                    element_list = list(parameter_results.index)
                    
                    
                elif value == 'min':
                    
                    parameter_results = np.min(model['results'].node[parameter])
                    
                    
                    element_list = list(parameter_results.index)
                    
                    
                elif value == 'mean':
                    
                    parameter_results = np.mean(model['results'].node[parameter])
                    
                    
                    element_list = list(parameter_results.index)
                    
                    
                elif type(value) == int:
                    
                    parameter_results = model['results'].node[parameter].iloc[value]
                    
                    
                    element_list = list(parameter_results.index)
                    
                    
            try:   
                
                if tanks:
                    pass
                
                else:
                    for tank in model['tank_names']:
                        
                        parameter_results.drop(tank, axis=0, inplace=True)
                        
                        
                        element_list.remove(tank)
                        
                        
                if reservoirs:
                    pass
                
                else:
                    for reservoir in model['reservoir_names']:
                        
                        parameter_results.drop(reservoir, axis=0, inplace=True)
                        
                        
                        element_list.remove(reservoir) 
            
            
            except KeyError:
                
                pass
            
            
            return parameter_results, element_list
        
        
        except KeyError:
            
            
            parameter_results = model['wn'].query_node_attribute(parameter)
            
            
            element_list = list(parameter_results.index)
            
            
            try:   
                
                if tanks:
                    pass
                
                else:                  
                    for tank in model['tank_names']:
                        
                        parameter_results.drop(tank, axis=0, inplace=True)
                        
                        
                        element_list.remove(tank)
                        
                        
                if reservoirs:
                    pass
                
                else:
                    for reservoir in model['reservoir_names']:
                        
                        parameter_results.drop(reservoir, axis=0, inplace=True)
                        
                        
                        element_list.remove(reservoir)
                        
                        
            except KeyError:
                
                pass
                
            
            return parameter_results, element_list
        
        
    elif parameter_type == 'link':
        
        try:
            
            if value is None:
                
                parameter_results = model['results'].link[parameter]
                
                
                element_list = list(parameter_results.index)
                
                
            else:
                
                if value == 'max':
                    
                    parameter_results = np.max(model['results'].link[parameter])
                    
                    
                    element_list = list(parameter_results.index)
                    
                    
                elif value == 'min':
                    
                    parameter_results = np.min(model['results'].link[parameter])
                    
                    
                    element_list = list(parameter_results.index)
                    
                    
                elif value == 'mean':
                    
                    parameter_results = np.mean(model['results'].link[parameter])
                    
                    
                    element_list = list(parameter_results.index)
                    
                    
                elif type(value) == int:
                    
                    parameter_results = model['results'].link[parameter].iloc[value]
                    
                    
                    element_list = list(parameter_results.index)   
                    
                    
            return parameter_results, element_list
        
        
        except KeyError:
            
            
            parameter_results = model['wn'].query_link_attribute(parameter)
            
            
            element_list = list(parameter_results.index)
            
            return parameter_results, element_list




def get_demand_patterns(model):
    
    demandPatterns = []
    
    
    patterns = model['wn'].pattern_name_list
    
    
    patterns = np.append(patterns, 'None')
    
    
    for junction in model['junc_names']:
        
        try:
            
            demandPattern = model['wn'].get_node(junction).demand_timeseries_list[0].pattern.name
            
            
            demandPatterns = np.append(demandPatterns, demandPattern)
            
            
        except AttributeError:
            
            demandPatterns = np.append(demandPatterns, 'None')
            
            
    demand_pattern_nodes = {}
    
    
    for pattern in patterns:
        
        demand_pattern_nodes[pattern] = {}
        
    counter = 0  
    for junc_name in model['junc_names']:
        
        for pattern in patterns:
            if demandPatterns[counter] == pattern:
                
                demand_pattern_nodes[pattern][junc_name] = model['junc_names'].index(junc_name)
        counter += 1
            
    for pattern in patterns:
        
        if len(demand_pattern_nodes[pattern]) == 0:
            
            patterns = np.delete(patterns,np.where(patterns == pattern))
            
            
            del demand_pattern_nodes[pattern]
            
    return demand_pattern_nodes, patterns  
    



def bin_parameter(model,parameter_results,element_list,bin_edge_num,bin_list='automatic',disable_bin_deleting=False):
    """Bins results from get_parameter based on user specifications.
    Arguments:
    model: Takes Dictionary. Gets pipe or node name list.
    parameter_results: Takes Series. Results from get_parameter.
    bin_edge_num: Number of bin edges that the user wants.
    bin_list: List of bin edges. When set to 'Automatic' it will create bin
    edges."""
    
    
    if bin_list == 'automatic':
        
        bins=bin_edge_num
        
        
        bin_list = np.linspace(np.min(parameter_results),np.max(parameter_results),bins)
        
        
    binnedParameter = {}
    binNames = []
    
    
    elementsWithParameter = element_list
    elementType = None
    
    
    for elementWithParameter in elementsWithParameter:   

        if (elementWithParameter in model['node_names']) is True:

            break
        else:   
            element_list = model['G_pipe_name_list']
            elementType = "link"

            break
        
    if elementType != "link":
        
        element_list = model['node_names']

    for i in range(len(bin_list)):
        
        if i == 0:
            
            if np.min(parameter_results) < bin_list[i]:
                
                binNames = np.append(binNames, '< {0:1.3f}'.format(bin_list[i]))
                
                
            binNames = np.append(binNames, '{0:1.3f} - {1:1.3f}'.format(bin_list[i], bin_list[i+1]))
            
            
        elif (i<len(bin_list) - 1):
            
            binNames = np.append(binNames, '{0:1.3f} - {1:1.3f}'.format(bin_list[i], bin_list[i+1]))
            
            
        elif i == len(bin_list) - 1:
            
            if np.max(parameter_results) > bin_list[i]:
                
                binNames = np.append(binNames, '> {0:1.3f}'.format(bin_list[i]))
                
                
    for binName in binNames:
        
        binnedParameter[binName] = {}


    for i in range(len(bin_list)):
        
        if i == 0:
            
            counter = 0

            
            for parameter in parameter_results:
                
                if parameter >= bin_list[i] and parameter < bin_list[i+1]:
                    
                        binnedParameter['{0:1.3f} - {1:1.3f}'.format(bin_list[i], bin_list[i+1])][elementsWithParameter[counter]] = element_list.index(elementsWithParameter[counter])
                        
                        
                if parameter < bin_list[i]:
                    
                        binnedParameter['< {0:1.3f}'.format(bin_list[i])][elementsWithParameter[counter]] = element_list.index(elementsWithParameter[counter])
                        
                        
                counter += 1
                
                
        elif i == len(bin_list) - 2:
            
            counter = 0
            
            
            for parameter in parameter_results:
                
                if parameter >= bin_list[i] and parameter <= bin_list[i+1]:
                    
                        binnedParameter['{0:1.3f} - {1:1.3f}'.format(bin_list[i], bin_list[i+1])][elementsWithParameter[counter]] = element_list.index(elementsWithParameter[counter])
                        
                        
                counter += 1
                
                
        elif (i<len(bin_list) - 2):
            
            counter = 0
            
            
            for parameter in parameter_results:
                
                if parameter >= bin_list[i] and parameter < bin_list[i+1]:
                    
                        binnedParameter['{0:1.3f} - {1:1.3f}'.format(bin_list[i], bin_list[i+1])][elementsWithParameter[counter]] = element_list.index(elementsWithParameter[counter])
                        
                        
                counter += 1
                
                
        elif i == len(bin_list) - 1:
            
            counter = 0
            
            
            for parameter in parameter_results:
                
                if parameter > bin_list[i]:
                    
                    binnedParameter['> {0:1.3f}'.format(bin_list[i])][elementsWithParameter[counter]] = element_list.index(elementsWithParameter[counter])
                    
                    
                counter += 1
                
    if disable_bin_deleting:        
        pass
    
    else:
        for binName in binNames:
            
            if len(binnedParameter[binName]) == 0:
                
                binNames = np.delete(binNames,np.where(binNames == binName))
                
                
                del binnedParameter[binName]
    

    return binnedParameter, binNames



def draw_nodes(model,node_list,parameter_results=None,vmin=None,vmax=None,node_size=None,node_color='k',cmap='tab10',node_shape='.',edge_colors='k',line_widths=0,label=None):
    
    if parameter_results is None:
        parameter_results = []
        
    if node_size is None:
        node_size = []
        
    if len(parameter_results) != 0:
        
        negativeValues = False
        
    if isinstance(node_size,list) and len(node_size) == 0:
        
        node_size = np.ones(len(node_list))*100
        
    if isinstance(node_size,int):
        node_size = np.ones(len(node_list))*node_size
        
        for value in parameter_results:
            
            if value < -1e-5:
                
                negativeValues = True
                
                
                cmap = mpl.cm.get_cmap(cmap)
    
                if vmin is None and vmax is None:
                    g = nxp.draw_networkx_nodes(model['G'], model['pos_dict'], nodelist=node_list,node_size = node_size, node_color=parameter_results,vmax=np.max(parameter_results),vmin=-np.max(parameter_results), cmap=cmap,node_shape = node_shape,linewidths=line_widths,edgecolors=edge_colors,label=label)
                else:
                    g = nxp.draw_networkx_nodes(model['G'], model['pos_dict'], nodelist=node_list,node_size = node_size, node_color=parameter_results,vmax=vmax,vmin=vmin, cmap=cmap,node_shape = node_shape,linewidths=line_widths,edgecolors=edge_colors,label=label)
                
                return g
    
    
        if negativeValues:
            pass
        
        else:
            cmap = mpl.cm.get_cmap(cmap)
            
            
            g = nxp.draw_networkx_nodes(model['G'], model['pos_dict'], nodelist=node_list,node_size = node_size, node_color=parameter_results, cmap=cmap, node_shape = node_shape,linewidths=line_widths,edgecolors=edge_colors, vmin=vmin, vmax=vmax)
            
            
            return g
        
    else:
        
        nxp.draw_networkx_nodes(model['G'], model['pos_dict'], nodelist=node_list,node_size = node_size, node_color=node_color, node_shape = node_shape,edgecolors=edge_colors,linewidths=line_widths,label=label)
    
    
    
    
def draw_links(model,link_list,parameter_results=None,edge_color='k',cmap='tab10',widths=[],vmin=None,vmax=None):
    
    if parameter_results is None:
        parameter_results = []
    
    if widths is None:
        widths = []
        
    edgeList = {}
    
    if len(widths) == 0:
        
        widths = np.ones(len(link_list))*1
    
    
    
   
    negativeValues = False
    
    
    if len(parameter_results) != 0:
        for i in link_list:
            
            edgeList[i] = link_list.index(i)
            
        for value in parameter_results:
            
            if value < -1e-5:
                
                negativeValues = True
                
                
                cmap = mpl.cm.get_cmap(cmap)
                
                if vmin is None and vmax is None:
                    g = nxp.draw_networkx_edges(model['G'], model['pos_dict'], edgelist=([model['pipe_list'][i] for i in edgeList.values()]), edge_color=parameter_results, edge_vmax=np.max(parameter_results),edge_vmin=-np.max(parameter_results),edge_cmap=cmap,arrows=False,width=widths)
                else:
                    g = nxp.draw_networkx_edges(model['G'], model['pos_dict'], edgelist=([model['pipe_list'][i] for i in edgeList.values()]), edge_color=parameter_results, edge_vmax=vmax,edge_vmin=vmin,edge_cmap=cmap,arrows=False,width=widths)
                
                return g

        
        if negativeValues:
            pass
        
        else:
            cmap = mpl.cm.get_cmap(cmap)
            
            
            g = nxp.draw_networkx_edges(model['G'], model['pos_dict'], edgelist=([model['pipe_list'][i] for i in edgeList.values()]), edge_color=parameter_results, edge_cmap=cmap, arrows=False,width=widths,vmin=vmin,vmax=vmax)
            
            
            return g
            
    else:
        for i in link_list:
            edgeList[i] = model['G_pipe_name_list'].index(i)
        nxp.draw_networkx_edges(model['G'], model['pos_dict'], edgelist=([model['pipe_list'][i] for i in edgeList.values()]), edge_color=edge_color, arrows=False,width=widths)
    
    
def draw_base_elements(model,ax,nodes=True,links=True,reservoirs=True,tanks=True,pumps=True,valves=True,legend=True):
    """Draws nodes, links, resevoirs, tanks, pumps and valves without any data
    attached to them.
    Arguments:
    model: Takes dictionary.
    ax: Axis of the figure the user wants the elements to be plotted on.
    reservoirs: Takes Boolean. Determines whether to draw reservoirs or not.
    tanks: Takes Boolean. Determines whether to draw tanks or not.
    pumps: Takes Boolean. Determines whether to draw pumps or not.
    valves: Takes Boolean. Determines whether to draw valves or not.
    legend: Takes Boolean. Determines whether to draw legend or not."""
    if nodes:
        
        nxp.draw_networkx_nodes(model['G'], model['pos_dict'], node_size = 30, node_color = 'k')
        
        
    if reservoirs:
        
        nxp.draw_networkx_nodes(model['G'], model['pos_dict'], ax=ax, nodelist = model['reservoir_names'], node_size = 200, node_color = 'black',linewidths=3,node_shape = 's', label='Reservoirs')
    
    
    if tanks:
        
        nxp.draw_networkx_nodes(model['G'], model['pos_dict'], ax=ax, nodelist = model['tank_names'], node_size = 200, node_color = 'black',linewidths=3, node_shape = 'd', label='Tanks')
   
    
    if valves:
        
        valve_coordinates = {}
        valveCounter = 0
        
        
        for point1, point2 in model['G_list_valves_only']:
            
            midpoint = [(model['wn'].get_node(point1).coordinates[0] + model['wn'].get_node(point2).coordinates[0])/2,(model['wn'].get_node(point1).coordinates[1] + model['wn'].get_node(point2).coordinates[1])/2]
            
            
            valve_coordinates[model['valve_names'][valveCounter]] = midpoint
            valveCounter += 1
            
            
        nxp.draw_networkx_nodes(model['G'], valve_coordinates, ax=ax, nodelist = model['valve_names'], node_size = 200, node_color = 'orange', edgecolors='black',linewidths=1,node_shape = 'P', label='Valves')
        
    if links:  
        
        nxp.draw_networkx_edges(model['G'], model['pos_dict'], ax=ax, arrows = False, edge_color = 'k')
    
    
    if pumps:
        
        nxp.draw_networkx_edges(model['G'], model['pos_dict'], ax=ax, edgelist = model['G_list_pumps_only'], node_size = 200, edge_color = 'b', width=3, arrows=False)  
        
        
     
        
def draw_discrete_nodes(model,ax,nodes, bin_list, bin_size_list=None, bin_label_list=None, bin_shape_list=None,cmap='tab10', bin_border_list = None, bin_border_width_list = None, color_list =  None):
    """Draws nodes based off of discrete bins.
    Arguments:
    model: Takes Dictionary.
    ax: Axis of the figure the user wants the elements to be plotted on.
    nodes: Takes Dictionary. List of nodes to be plotted organized by bin 
    into dictionaries.
    bin_list: Takes List. List of bin names.
    bin_size_list: Takes List. List of node sizes for each bin.
    bin_label_list: Takes List. List of labels for each bin.
    bin_shape_list: Takes List. List of markers for each bin.
    cmap: Takes String. Colormap that determines bin colors.
    color_list: Takes List. List of hexadecimal strings that determine bin
    colors. cmap must = None for color_list to take priority."""
    
    
    if bin_size_list is None:
        
        if len(model['node_names']) < 300:
            
            bin_size_list = np.ones(len(bin_list))*300
            
            
        elif len(model['node_names']) >= 300 and len(model['node_names']) < 1000:
            
            bin_size_list = np.ones(len(bin_list))*(80000/len(model['node_names']))
            
            
        else:
            
            bin_size_list = np.ones(len(bin_list))*80

    
    if bin_label_list is None:
        
        bin_label_list = bin_list
        
        
    if bin_shape_list is None:
        
        bin_shape_list = []
        
        
        for i in range(len(bin_list)):
            
            bin_shape_list = np.append(bin_shape_list,'.')
            
    if bin_border_list is None:
        bin_border_list = []
        
        for i in range(len(bin_list)):
            
            bin_border_list = np.append(bin_border_list,'k')
    
    if bin_border_width_list is None:
        bin_border_width_list = []
        
        for i in range(len(bin_list)):
            
            bin_border_width_list = np.append(bin_border_width_list,0)
            
            
    counter = 0
    empty_bin = False
    
    if (color_list is not None and cmap is not None) or cmap is not None:    
        
        cmap = mpl.cm.get_cmap(cmap)
        cmapValue = 1/len(bin_list)
        
        
        for binName in bin_list:
            node_list = ([model['node_names'][i] for i in nodes.get(binName).values()])
            if len(node_list) == 0:
                nxp.draw_networkx_nodes(model['G'], model['pos_dict'], ax=ax, nodelist = [model['node_names'][0]], node_size = bin_size_list[counter], node_color = [cmap(float(cmapValue))], node_shape = bin_shape_list[counter],label=bin_label_list[counter], edgecolors = bin_border_list[counter],linewidths = bin_border_width_list[counter])
                empty_bin = True
            else:
                nxp.draw_networkx_nodes(model['G'], model['pos_dict'], ax=ax, nodelist = node_list, node_size = bin_size_list[counter], node_color = [cmap(float(cmapValue))], node_shape = bin_shape_list[counter],label=bin_label_list[counter], edgecolors = bin_border_list[counter],linewidths = bin_border_width_list[counter])
            
            
            cmapValue += 1/len(bin_list)
            
            
            counter += 1
        if empty_bin:
           counter2 = 0
           cmap2 = mpl.cm.get_cmap(cmap)
           cmapValue2 = 1/len(bin_list)
           for binName in bin_list:
               node_list = ([model['node_names'][i] for i in nodes.get(binName).values()])
               nxp.draw_networkx_nodes(model['G'], model['pos_dict'], ax=ax, nodelist = node_list, node_size = bin_size_list[counter2], node_color = [cmap2(float(cmapValue2))], node_shape = bin_shape_list[counter2], edgecolors = bin_border_list[counter2],linewidths = bin_border_width_list[counter2])
               cmapValue2 += 1/len(bin_list)
               counter2 += 1
            
    else:
        
        for binName in bin_list:
            node_list = ([model['node_names'][i] for i in nodes.get(binName).values()])
            if len(node_list) == 0:
                nxp.draw_networkx_nodes(model['G'], model['pos_dict'], ax=ax, nodelist = [model['node_names'][0]], node_size = bin_size_list[counter], node_color = color_list[counter], node_shape = bin_shape_list[counter],label=bin_label_list[counter], edgecolors = bin_border_list[counter],linewidths = bin_border_width_list[counter])
                empty_bin == True
            else:
                nxp.draw_networkx_nodes(model['G'], model['pos_dict'], ax=ax, nodelist = ([model['node_names'][i] for i in nodes.get(binName).values()]), node_size = bin_size_list[counter], node_color = color_list[counter], node_shape = bin_shape_list[counter],label=bin_label_list[counter], edgecolors = bin_border_list[counter],linewidths = bin_border_width_list[counter])
        
            
            counter += 1

        if empty_bin:
            counter2 = 0
            for binName in bin_list:
                node_list = ([model['node_names'][i] for i in nodes.get(binName).values()])
                nxp.draw_networkx_nodes(model['G'], model['pos_dict'], ax=ax, nodelist = node_list, node_size = bin_size_list[counter2], node_color = color_list[counter2], node_shape = bin_shape_list[counter2], edgecolors = bin_border_list[counter2],linewidths = bin_border_width_list[counter2])
                counter2 += 1


def draw_discrete_links(model,ax,links, bin_list, bin_width_list=None, bin_label_list=None,cmap='tab10', color_list =  None):
    """Draws links s based off of discrete bins.
    Arguments:
    model: Takes Dictionary.
    ax: Axis of the figure the user wants the elements to be plotted on.
    links: Takes Dictionary. List of links to be plotted organized by bin 
    into dictionaries.
    bin_list: Takes List. List of bin names.
    bin_width_list: Takes List. List of link widths for each bin.
    bin_label_list: Takes List. List of labels for each bin.
    bin_shape_list: Takes List. List of markers for each bin.
    cmap: Takes String. Colormap that determines bin colors.
    color_list: Takes List. List of hexadecimal strings that determine bin
    colors. cmap must = None for color_list to take priority."""
    
    
    if bin_width_list is None:
        
        bin_width_list = np.ones(len(bin_list))*2
        

    if bin_label_list is None:
        
        bin_label_list = bin_list
        
        
    counter = 0
    empty_bin = False
    
    if (color_list is not None and cmap is not None) or cmap is not None:    
        
        cmap = mpl.cm.get_cmap(cmap)
        cmapValue = 1/len(bin_list)
        
        
        for binName in bin_list:
            edge_list = ([model['pipe_list'][i] for i in links.get(binName).values()])
            if len(edge_list) == 0:
                nxp.draw_networkx_edges(model['G'], model['pos_dict'], edgelist = [model['pipe_list'][0]],edge_color = cmap(float(cmapValue)),width = bin_width_list[counter],arrows = False,label=bin_label_list[counter])
                empty_bin = True
            else:
                nxp.draw_networkx_edges(model['G'], model['pos_dict'], edgelist = edge_list,edge_color = cmap(float(cmapValue)),width = bin_width_list[counter],arrows = False,label=bin_label_list[counter])
            cmapValue += 1/len(bin_list)
            
            
            counter += 1
            
        if empty_bin:
            counter2 = 0
            cmap2 = mpl.cm.get_cmap(cmap)
            cmapValue2 = 1/len(bin_list)
            for binName in bin_list:
                edge_list = ([model['pipe_list'][i] for i in links.get(binName).values()])
                nxp.draw_networkx_edges(model['G'], model['pos_dict'], edgelist = edge_list,edge_color = cmap2(float(cmapValue2)),width = bin_width_list[counter2],arrows = False)      
                cmapValue2 += 1/len(bin_list)
                counter2 += 1
    else:
        
       for binName in bin_list:
           edge_list = ([model['pipe_list'][i] for i in links.get(binName).values()])
           if len(edge_list) == 0:
               nxp.draw_networkx_edges(model['G'], model['pos_dict'], edgelist = [model['pipe_list'][0]],edge_color = color_list[counter],width = bin_width_list[counter],arrows = False,label=bin_label_list[counter])
               empty_bin = True
           else:
               nxp.draw_networkx_edges(model['G'], model['pos_dict'], edgelist = edge_list,edge_color = color_list[counter],width = bin_width_list[counter],arrows = False,label=bin_label_list[counter])
           
           
           counter += 1
           
       if empty_bin:
           counter2 = 0
           for binName in bin_list:
               edge_list = ([model['pipe_list'][i] for i in links.get(binName).values()])
               nxp.draw_networkx_edges(model['G'], model['pos_dict'], edgelist = edge_list,edge_color = color_list[counter2],width = bin_width_list[counter2],arrows = False)      
               counter2 += 1   
        
   
    
    
def draw_legend(ax,bin_list=None,title=None,pumps=True,loc='upper right',loc2='lower right'):
    """Draws legend for basic elements.
    Arguments:
    ax: Axis of the figure the user wants the elements to be plotted on.
    bin_list: Takes List. List of bins.
    title: Takes String. Legend title.
    pumps: Takes Boolean. Determines whether pumps are drawn or not.
    loc: Takes String. Location of elements legend.
    loc2 = Takes String. Location of bins legend"""
    
    if bin_list is None:
        bin_list = []
        
    handles, labels = ax.get_legend_handles_labels()
    
    if pumps:
        
        patch1 = mpatches.Patch(color='blue', label='Pumps')
        patch2 = mpatches.Patch(color='black', label='Pipes')
        
        
        handles.extend([patch1,patch2])
    
    
    else:
        
        patch = mpatches.Patch(color='black', label='Pipes')
        
        
        handles.extend([patch])
    
        
    
    
    if len(bin_list) != 0:
        
        legend = ax.legend(handles=handles[len(bin_list):], loc=loc,fontsize = '15',frameon=False)
        ax.add_artist(legend)
        
        
        legend2 = ax.legend(title=title,handles=handles[:len(bin_list)], loc=loc2,fontsize = '15', title_fontsize = '17',frameon=False)
        ax.add_artist(legend2)
        
        
    else:
        
        legend = ax.legend(handles=handles, loc=loc,fontsize = '15',frameon=False)
        ax.add_artist(legend)
    


    

def draw_color_bar(ax,g,cmap,color_bar_title=None):
    """Draws Color Bar.
    Arguments:
    g: NetworkX graph of plotted elements.
    cmap: Colormap
    color_bar_title: Takes String. Title of Color Bar."""

    global cbar
    cbar = plt.colorbar(g)
    cbar.set_label(color_bar_title, fontsize = 15)
    
    
    
    
def draw_label(model,ax,labels,x_coords,y_coords,nodes=None):
    
    
    if nodes is not None:
        
        for label, node, xCoord, yCoord in zip(labels, nodes, x_coords, y_coords): 
            
            plt.text(model['wn'].get_node(node).coordinates[0]+xCoord,model['wn'].get_node(node).coordinates[1]+yCoord,s = label, bbox=dict(facecolor='mediumaquamarine', alpha=0.9, edgecolor='black'),horizontalalignment='right', fontsize = 11)
            
            
    elif nodes is None:
        
        for label, xCoord, yCoord in zip(labels, x_coords, y_coords):
            
            plt.text(xCoord,yCoord,s = label, bbox=dict(facecolor='mediumaquamarine', alpha=0.9, edgecolor='black'),horizontalalignment='right', fontsize = 11,transform=ax.transAxes)
    
    
    
    
    
    
    
    
def plot_basic_elements(model,ax,pumps=True,valves=True,reservoirs=True,tanks=True,links=True,nodes=True,savefig=True, save_name=None, legend=True,legend_loc='upper right'):
    """Creates a basic plot, similar to the default seen in EPANET.
    Arguments:
    model: Saved initilization done with initializeModel
    savefig: Boolean. Determines whether plot is saved to /Images directory"""

    
    draw_base_elements(model,ax,nodes=nodes,reservoirs=reservoirs,tanks=tanks,links=links,valves=valves,pumps=pumps,legend=True)
    
    if legend:
        
        draw_legend(ax,pumps=pumps,loc=legend_loc)
    
    if savefig:
        
        save_fig(model, save_name=save_name)




def plot_discrete_nodes(model,ax,bin_edge_num=5,parameter=None, value=None, unit=None,get_tanks=False,get_reservoirs=False,bins='automatic', bin_size_list = None, bin_shape_list = None,bin_label_list = None, bin_border_list = None, bin_border_width_list = None, savefig=True, tanks=True, reservoirs=True, pumps=True, valves=True,legend=True,legend_title = None, legend_loc_1='upper right', legend_loc_2='lower right',save_name=None, cmap= default_cmap, color_list=None,disable_bin_deleting=False):
    """Plots discrete Nodes.
    Arguments:
    figsize: Figure size. Takes a 2-element List.
    parameter: Takes String. The name of the parameter. 
    value: Takes Integer. Parameters from results must include a value 
    with it. The value given is the value index, not time.
    bins: List of bin edges. When set to 'Automatic' it will create bin
    edges.
    bin_edge_num: Number of bin edges that the user wants.
    bin_list: Takes List. List of bin names.
    bin_size_list: Takes List. List of node sizes for each bin.
    bin_label_list: Takes List. List of labels for each bin.
    bin_shape_list: Takes List. List of markers for each bin.
    cmap: Takes String. Colormap that determines bin colors.
    color_list: Takes List. List of hexadecimal strings that determine bin
    colors. cmap must = None for color_list to take priority.
    reservoirs: Takes Boolean. Determines whether to draw reservoirs or not.
    tanks: Takes Boolean. Determines whether to draw tanks or not.
    pumps: Takes Boolean. Determines whether to draw pumps or not.
    valves: Takes Boolean. Determines whether to draw valves or not.
    legend: Takes Boolean. Determines whether to draw legend or not.
    legend_title: Takes string. Title of legend.
    legend_loc_1: Takes String. Location of legend.
    savefig: Takes Boolean. Determines if figure is saved or not.
    save_name: Takes string. SaveName acts as a prefix for the image file name,
    and is followed by the name of the network.
    specialData: Takes either Excel file or correctly formatted dictionary. 
    Used to plot custom data."""


    if parameter is not None:
        
        parameter_results, node_list = get_parameter(model,'node',parameter, value=value,tanks=get_tanks,reservoirs=get_reservoirs)
        
        if unit is not None:
            parameter_results = unit_conversion(parameter_results,parameter,unit)
            
            
        binnedResults,binNames = bin_parameter(model,parameter_results,node_list,bin_list=bins, bin_edge_num=bin_edge_num,disable_bin_deleting=disable_bin_deleting) 
        
        
        draw_discrete_nodes(model,ax,binnedResults,binNames,bin_size_list=bin_size_list,bin_shape_list=bin_shape_list, bin_label_list=bin_label_list,bin_border_list = bin_border_list, bin_border_width_list = bin_border_width_list,cmap=cmap, color_list=color_list)
    
    
        draw_base_elements(model,ax,nodes=False,tanks=tanks,reservoirs=reservoirs,pumps=pumps,valves=valves)
    
    
        if legend:
            draw_legend(ax,bin_list=binNames,title=legend_title,pumps=pumps,loc=legend_loc_1,loc2=legend_loc_2)
    
    
    if savefig:
        
         save_fig(model, save_name=save_name)


    


def plot_continuous_nodes(model,ax,parameter=None, value=None, unit=None,vmin=None,vmax=None,get_tanks=False,get_reservoirs=False,tanks=True, reservoirs=True, pumps=True, valves=True,cmap= default_cmap, color_bar_title=None,node_size=100, node_shape='.',edge_colors=None,line_widths=None,legend=True,legend_loc='upper right',savefig=True, save_name=None):
    """Plots continuous Nodes.
    Arguments:
    figsize: Figure size. Takes a 2-element List.
    parameter: Takes String. The name of the parameter. 
    value: Takes Integer. Parameters from results must include a value 
    with it. The value given is the value index, not time.
    reservoirs: Takes Boolean. Determines whether to draw reservoirs or not.
    tanks: Takes Boolean. Determines whether to draw tanks or not.
    pumps: Takes Boolean. Determines whether to draw pumps or not.
    valves: Takes Boolean. Determines whether to draw valves or not.
    legend: Takes Boolean. Determines whether to draw legend or not.
    legend_title: Takes string. Title of legend.
    legend_loc_1: Takes String. Location of legend.
    savefig: Takes Boolean. Determines if figure is saved or not.
    save_name: Takes string. SaveName acts as a prefix for the image file name,
    and is followed by the name of the network.
    specialData: Takes either Excel file or correctly formatted dictionary. 
    Used to plot custom data."""
    
    
    if parameter is not None:
        
        parameter_results, node_list = get_parameter(model,'node',parameter, value=value, tanks=get_tanks, reservoirs=get_reservoirs)
        
        if unit is not None:
            parameter_results = unit_conversion(parameter_results,parameter,unit)
            
        g = draw_nodes(model,node_list,parameter_results=parameter_results,vmin=vmin,vmax=vmax,node_size=node_size,cmap=cmap,node_shape=node_shape,edge_colors=edge_colors,line_widths=line_widths)
            
        
        draw_base_elements(model,ax,nodes=False,tanks=tanks,reservoirs=reservoirs,pumps=pumps,valves=valves)
        
        
        draw_color_bar(ax,g,cmap,color_bar_title=color_bar_title)

    if legend:
        
        draw_legend(ax,pumps=pumps,loc=legend_loc)
        
    if savefig:
        
        save_fig(model, save_name=save_name)
  
    
  
    
def plot_discrete_links(model, ax,bin_edge_num=5, parameter=None, value=None, unit=None,bins='automatic', bin_width_list=None, bin_label_list=None,color_list=None,tanks=True, reservoirs=True, pumps=True, valves=True,cmap=default_cmap,legend=True, legend_title=None, legend_loc_1='upper right', legend_loc_2='lower right',savefig=True,save_name=None,disable_bin_deleting=False):
    """Plots discrete Links.
    Arguments:
    figsize: Figure size. Takes a 2-element List.
    parameter: Takes String. The name of the parameter. 
    value: Takes Integer. Parameters from results must include a value 
    with it. The value given is the value index, not time.
    bins: List of bin edges. When set to 'Automatic' it will create bin
    edges.
    bin_edge_num: Number of bin edges that the user wants.
    bin_list: Takes List. List of bin names.
    bin_width_list: Takes List. List of link widths for each bin.
    bin_label_list: Takes List. List of labels for each bin.
    bin_shape_list: Takes List. List of markers for each bin.
    cmap: Takes String. Colormap that determines bin colors.
    color_list: Takes List. List of hexadecimal strings that determine bin
    colors. cmap must = None for color_list to take priority.
    reservoirs: Takes Boolean. Determines whether to draw reservoirs or not.
    tanks: Takes Boolean. Determines whether to draw tanks or not.
    pumps: Takes Boolean. Determines whether to draw pumps or not.
    valves: Takes Boolean. Determines whether to draw valves or not.
    legend: Takes Boolean. Determines whether to draw legend or not.
    legend_title: Takes string. Title of legend.
    legend_loc_1: Takes String. Location of legend.
    savefig: Takes Boolean. Determines if figure is saved or not.
    save_name: Takes string. SaveName acts as a prefix for the image file name,
    and is followed by the name of the network.
    specialData: Takes either Excel file or correctly formatted dictionary. 
    Used to plot custom data."""
    
    if parameter is not None:
        
        parameter_results, link_list = get_parameter(model,'link',parameter, value=value)
        
        
        if unit is not None:
            parameter_results = unit_conversion(parameter_results,parameter,unit)
            
        
        binnedResults,binNames = bin_parameter(model,parameter_results,link_list,bin_list=bins, bin_edge_num=bin_edge_num,disable_bin_deleting=disable_bin_deleting)
        
        
        draw_discrete_links(model,ax,binnedResults,binNames,bin_width_list=bin_width_list, bin_label_list=bin_label_list,cmap=cmap, color_list=color_list)
        
        
        draw_base_elements(model,ax,nodes=False,links=False,tanks=tanks,reservoirs=reservoirs,pumps=pumps,valves=valves)
        
        
        if legend:
            
            draw_legend(ax,bin_list=binNames,title=legend_title,pumps=pumps,loc=legend_loc_1,loc2=legend_loc_2)


    if savefig:
        
         save_fig(model, save_name=save_name)
   
         
   
    
def plot_continuous_links(model,ax,parameter=None,value=None,unit=None,min_width=1,max_width=5,vmin=None,vmax=None,tanks=True, reservoirs=True, pumps=True, valves=True,cmap=default_cmap,color_bar_title=None,legend=True,legend_loc='upper right',legend_title=None,savefig=True, save_name=None):
    """Plots continuous Links.
    Arguments:
    figsize: Figure size. Takes a 2-element List.
    parameter: Takes String. The name of the parameter. 
    value: Takes Integer. Parameters from results must include a value 
    with it. The value given is the value index, not time.
    reservoirs: Takes Boolean. Determines whether to draw reservoirs or not.
    tanks: Takes Boolean. Determines whether to draw tanks or not.
    pumps: Takes Boolean. Determines whether to draw pumps or not.
    valves: Takes Boolean. Determines whether to draw valves or not.
    legend: Takes Boolean. Determines whether to draw legend or not.
    legend_title: Takes string. Title of legend.
    legend_loc_1: Takes String. Location of legend.
    savefig: Takes Boolean. Determines if figure is saved or not.
    save_name: Takes string. SaveName acts as a prefix for the image file name,
    and is followed by the name of the network.
    specialData: Takes either Excel file or correctly formatted dictionary. 
    Used to plot custom data."""
    
    


    
    if parameter is not None:
        
        parameter_results, link_list = get_parameter(model,'link',parameter, value=value)
        
        
        if unit is not None:
            parameter_results = unit_conversion(parameter_results,parameter,unit)
            
            
        minParameter = np.min(parameter_results)
        maxParameter = np.max(parameter_results)
        
        
        normalizedParameter = np.copy(parameter_results)
        
        
        counter = 0
        
        
        for parameter in parameter_results:
            
            normalizedParameter[counter] = ((max_width - min_width)*((parameter - minParameter)/(maxParameter - minParameter))) + min_width
           
            
            counter += 1
        
        
        widths = normalizedParameter
        
        
        g = draw_links(model,link_list,parameter_results=parameter_results,cmap=cmap,widths=widths,vmin=vmin,vmax=vmax)
      
    
        draw_base_elements(model,ax,nodes=False,links=False,tanks=tanks,reservoirs=reservoirs,pumps=pumps,valves=valves)
    
    
        draw_color_bar(ax,g,cmap,color_bar_title=color_bar_title)
    
    if legend:
        
        draw_legend(ax,title=legend_title,pumps=pumps,loc=legend_loc)
    
    if savefig:
        
        save_fig(model, save_name=save_name)
    
    
    
    
def animate_plot(model,ax,function,fps=3,first_timestep=0,last_timestep=None,gif_save_name='gif',**kwargs):
    
    timesteps = int(model['wn'].options.time.duration/model['wn'].options.time.report_timestep)
    values = range(timesteps)
    if last_timestep is not None:
        values = values[first_timestep:last_timestep]
    
    filenames = []
    if function == plot_continuous_links or function == plot_continuous_nodes:
        if kwargs.get('vmin',None) is None or kwargs.get('vmax',None) is None:
            if function == plot_continuous_links:
                parameter_results, link_list = get_parameter(model,'link',kwargs.get('parameter'),kwargs.get('value',None))
            if function == plot_continuous_nodes:
                parameter_results, node_list = get_parameter(model,'node',kwargs.get('parameter'),kwargs.get('value',None))
            for value in np.min(parameter_results):   
                if value < -1e-5:
                    if kwargs.get('vmin',None) is None:
                        kwargs['vmin'] = -np.max(np.max(parameter_results))
                    if kwargs.get('vmax',None) is None:
                        kwargs['vmax'] = np.max(np.max(parameter_results))
                    break
                else:
                    if kwargs.get('vmin',None) is None:
                        kwargs['vmin'] = np.min(np.min(parameter_results))
                    if kwargs.get('vmax',None) is None:
                        kwargs['vmax'] = np.max(np.max(parameter_results))
    if function == plot_discrete_links or function == plot_discrete_nodes:
        kwargs['disable_bin_deleting'] = True
        
        if kwargs.get('bins',None) is None:
            if function == plot_discrete_links:
                parameter_results, link_list = get_parameter(model,'link',kwargs.get('parameter'),kwargs.get('value',None))
                
            if function == plot_discrete_nodes:
                parameter_results, node_list = get_parameter(model,'node',kwargs.get('parameter'),kwargs.get('value',None))
            
            kwargs['bins'] = np.linspace(np.min(np.min(parameter_results)),np.max(np.max(parameter_results)),kwargs.get('bin_edge_num',5))
    for value in values:
        
        function(model,ax,value=value,**kwargs)
        
        
        handles, labels = [], []
        
        
        plt.legend(handles, labels, title = 'Timestep ' + str(value*model['wn'].options.time.report_timestep) + " Seconds", loc='lower left',frameon=False)
        
        
        plt.savefig(model['image_path'] + '\\' + str(value) + '.png')
        
        
        filenames = np.append(filenames, model['image_path'] + '\\' + str(value) + '.png')
        ax.clear()
        if function == plot_continuous_links or function == plot_continuous_nodes:
           cbar.remove()
        
    # builds gif
    with imageio.get_writer(model['image_path'] + '\\' + gif_save_name + '.gif', mode='I',fps=fps) as writer:
        
        for filename in filenames:
            
            image = imageio.imread(filename)
            
            
            writer.append_data(image)
        
        
        for filename in set(filenames):
            
            os.remove(filename)


            
def plot_unique_data(model, ax, parameter=None, parameter_type=None,data_type=None,excel_columns=None,custom_data_values=None, unit=None,bins='automatic',bin_size_list = None, bin_shape_list = None, bin_edge_num=5, bin_width_list=None, bin_label_list=None,bin_border_list = None, bin_border_width_list = None,color_list=None,min_width=1,max_width=5,vmin=None,vmax=None,tanks=True, reservoirs=True, pumps=True, valves=True,cmap=default_cmap,legend=True, legend_title=None,node_size=100, node_shape='.',legend_loc_1='upper right', legend_loc_2='lower right',savefig=True,save_name=None,color_bar_title=None):
    
    
    if parameter=='demand_patterns':
        
        demand_pattern_nodes,patterns = get_demand_patterns(model)
        
        
        draw_discrete_nodes(model,ax,demand_pattern_nodes,patterns,bin_size_list=bin_size_list,bin_shape_list=bin_shape_list, bin_label_list=bin_label_list,bin_border_list = bin_border_list, bin_border_width_list = bin_border_width_list,cmap=cmap, color_list=color_list)
        
        
        draw_base_elements(model,ax,nodes=False)  
        
        
        if legend:
            
            draw_legend(ax,patterns,title=legend_title,pumps=pumps,loc=legend_loc_1,loc2=legend_loc_2)
            
            
        if savefig:
            
            save_fig(model, save_name=save_name)
            
            
        return
    
    
    if parameter=='diameter' or parameter=='roughness':
        
        parameter_results, link_list = get_parameter(model,'link',parameter)
        
        if unit is not None:
            parameter_results = unit_conversion(parameter_results,parameter,unit)
            
            
        uniques = pd.unique(parameter_results)
        
        
        binNames = []
        
        
        for binName in uniques:
            
            binNames = np.append(binNames,('{:.4f}'.format(binName)))
            
            
        binnedResults = {}
        
        
        for binName in binNames:
            
            binnedResults[binName] = {}
        
        
        for link in link_list:
            
            binnedResults['{:.4f}'.format(parameter_results.loc[link])][link] = model['G_pipe_name_list'].index(link)
       
        
        draw_discrete_links(model,ax,binnedResults,binNames,bin_width_list=bin_width_list, bin_label_list=bin_label_list,cmap=cmap, color_list=color_list)
        
        
        draw_base_elements(model,ax,nodes=False,links=False,tanks=tanks,reservoirs=reservoirs,pumps=pumps,valves=valves)
        
        
        if legend:
            
            draw_legend(ax,binNames,title=legend_title,pumps=pumps,loc=legend_loc_1,loc2=legend_loc_2)
        
        
        if savefig:
            
            save_fig(model, save_name=save_name)
            
            
        return
    
    
    if parameter=='tag':
        
        parameter_results, node_list = get_parameter(model,'node',parameter)
        
        
        uniques = pd.unique(parameter_results)
        uniques =  uniques[uniques is not None]
        
        
        binNames = []
        
        
        if len(uniques) != 0:
            
            for binName in uniques:
                
                binNames = binName
            
            
        binNames = np.append(binNames,'No Tag')
        
        
        binnedResults = {}
        
        
        for binName in binNames:
            
            binnedResults[binName] = {}
        
        
        for node in node_list:
            
            if parameter_results.loc[node] is None:
                
                binnedResults['No Tag'][node] = model['node_names'].index(node)
                
                
                continue
            
            
            binnedResults[parameter_results.loc[node]][node] = model['node_names'].index(node)
       
        
        draw_discrete_nodes(model,ax,binnedResults,binNames,bin_size_list=bin_size_list,bin_shape_list=bin_shape_list, bin_label_list=bin_label_list,bin_border_list = bin_border_list, bin_border_width_list = bin_border_width_list,cmap=cmap, color_list=color_list)
        
        
        draw_base_elements(model,ax,nodes=False,tanks=tanks,reservoirs=reservoirs,pumps=pumps,valves=valves)
        
        
        if legend:
            
            draw_legend(ax,binNames,title=legend_title,pumps=pumps,loc=legend_loc_1,loc2=legend_loc_2)
        
        
        if savefig:
            
            save_fig(model, save_name=save_name)
            
            
        return
    
    
    if parameter == 'custom_data':
        
        if data_type == 'unique':
            
            if parameter_type == 'link':
                
                draw_discrete_links(model,ax,custom_data_values[0], custom_data_values[1],bin_width_list=bin_width_list, bin_label_list=bin_label_list,cmap=cmap, color_list=color_list)
                
                
                draw_base_elements(model,ax,links=False,nodes=False,tanks=tanks,reservoirs=reservoirs,pumps=pumps,valves=valves)
            
            
            elif parameter_type == 'node':
                
                draw_discrete_nodes(model,ax,custom_data_values[0], custom_data_values[1],bin_size_list=bin_size_list,bin_shape_list=bin_shape_list, bin_label_list=bin_label_list,bin_border_list = bin_border_list, bin_border_width_list = bin_border_width_list,cmap=cmap, color_list=color_list)
            
            
                draw_base_elements(model,ax,nodes=False,tanks=tanks,reservoirs=reservoirs,pumps=pumps,valves=valves)
           
            
           
            if legend:
                
                draw_legend(ax,custom_data_values[1],title=legend_title,pumps=pumps,loc=legend_loc_1,loc2=legend_loc_2)
            
            
            if savefig:
                
                save_fig(model, save_name=save_name)
                
                
            return
        
        if data_type == 'discrete':
            binnedResults,binNames = bin_parameter(model,custom_data_values[1],custom_data_values[0],bin_list=bins, bin_edge_num=bin_edge_num) 
            
            
            if parameter_type == 'link':
                
                draw_discrete_links(model,ax,binnedResults,binNames,bin_width_list=bin_width_list, bin_label_list=bin_label_list,cmap=cmap, color_list=color_list)
                
                
                draw_base_elements(model,ax,nodes=False,links=False,tanks=tanks,reservoirs=reservoirs,pumps=pumps,valves=valves)
                
                
            if parameter_type == 'node':
                
                draw_discrete_nodes(model,ax,binnedResults,binNames,bin_size_list=bin_size_list,bin_shape_list=bin_shape_list, bin_label_list=bin_label_list,bin_border_list = bin_border_list, bin_border_width_list = bin_border_width_list,cmap=cmap, color_list=color_list)
            
            
                draw_base_elements(model,ax,nodes=False,tanks=tanks,reservoirs=reservoirs,pumps=pumps,valves=valves)
            
        
            if legend:
                
                draw_legend(ax,binNames,title=legend_title,pumps=pumps,loc=legend_loc_1,loc2=legend_loc_2)
        
        
            if savefig:
            
             save_fig(model, save_name=save_name)
             
             return
         
            
        if data_type == 'continuous':
            
            minParameter = np.min(custom_data_values[1])
            maxParameter = np.max(custom_data_values[1])
            
            
            normalizedParameter = np.copy(custom_data_values[1])
            
            
            counter = 0
            
            
            for parameter in custom_data_values[1]:
                
                normalizedParameter[counter] = ((max_width - min_width)*((parameter - minParameter)/(maxParameter - minParameter))) + min_width
                
                
                counter += 1
            
            
            widths = normalizedParameter
            
            
            if parameter_type == 'link':
                
                g = draw_links(model,custom_data_values[0], parameter_results=custom_data_values[1],cmap=cmap,widths=widths)
                
                
                draw_base_elements(model,ax,links=False,nodes=False,tanks=tanks,reservoirs=reservoirs,pumps=pumps,valves=valves)
            
            
            elif parameter_type == 'node':
                
                g = draw_nodes(model,custom_data_values[0], parameter_results=custom_data_values[1],node_size=node_size,cmap=cmap,node_shape=node_shape)
            
            
                draw_base_elements(model,ax,nodes=False,tanks=tanks,reservoirs=reservoirs,pumps=pumps,valves=valves)
            
            
            draw_color_bar(ax,g,cmap)
            
            if legend:
                
                draw_legend(ax,title=legend_title,pumps=pumps,loc=legend_loc_1)
                
            if savefig:
                
                save_fig(model, save_name=save_name)
                
                
            return
        
        
    if isinstance(parameter,str):
        
        if data_type == 'unique':
            
            node_list, bin_list = convert_excel(model,parameter,data_type,excel_columns[0],excel_columns[1])
            
            
            if parameter_type == 'link':
                
                draw_discrete_links(model,ax,node_list, bin_list,bin_width_list=bin_width_list, bin_label_list=bin_label_list,cmap=cmap, color_list=color_list)
                
                
                draw_base_elements(model,ax,links=False,nodes=False,tanks=tanks,reservoirs=reservoirs,pumps=pumps,valves=valves)
            
            
            elif parameter_type == 'node':
                
                draw_discrete_nodes(model,ax,node_list, bin_list,bin_size_list=bin_size_list,bin_shape_list=bin_shape_list, bin_label_list=bin_label_list,bin_border_list = bin_border_list, bin_border_width_list = bin_border_width_list,cmap=cmap, color_list=color_list)
            
            
                draw_base_elements(model,ax,nodes=False,tanks=tanks,reservoirs=reservoirs,pumps=pumps,valves=valves)
            
            
            if legend:
                
                draw_legend(ax,bin_list,title=legend_title,pumps=pumps,loc=legend_loc_1,loc2=legend_loc_2)
            
            
            if savefig:
                
                save_fig(model, save_name=save_name)
            
            return 
        
        
        if data_type == 'discrete':
            
            data = convert_excel(model,parameter,data_type,excel_columns[0],excel_columns[1])
            
            binnedResults,binNames = bin_parameter(model,data['element_list'],data['index'],bin_list=bins, bin_edge_num=bin_edge_num) 
            
            
            if parameter_type == 'link':
                
                draw_discrete_links(model,ax,binnedResults,binNames,bin_width_list=bin_width_list, bin_label_list=bin_label_list,cmap=cmap, color_list=color_list)
                
                
                draw_base_elements(model,ax,nodes=False,links=False,tanks=tanks,reservoirs=reservoirs,pumps=pumps,valves=valves)
                
                
            if parameter_type == 'node':
                
                draw_discrete_nodes(model,ax,binnedResults,binNames,bin_size_list=bin_size_list,bin_shape_list=bin_shape_list, bin_label_list=bin_label_list,bin_border_list = bin_border_list, bin_border_width_list = bin_border_width_list,cmap=cmap, color_list=color_list)
            
            
                draw_base_elements(model,ax,nodes=False,tanks=tanks,reservoirs=reservoirs,pumps=pumps,valves=valves)
            
        
            if legend:
                
                draw_legend(ax,binNames,title=legend_title,pumps=pumps,loc=legend_loc_1,loc2=legend_loc_2)
        
        
            if savefig:
            
             save_fig(model, save_name=save_name)    
         
            return
        if data_type == 'continuous':
            
            data = convert_excel(model,parameter,data_type,excel_columns[0],excel_columns[1])
            
            
            minParameter = np.min(data['element_list'])
            maxParameter = np.max(data['element_list'])
            
            
            normalizedParameter = np.copy(data['element_list'])
            
            
            counter = 0
            
            
            for parameter in data['element_list']:
                
                normalizedParameter[counter] = ((max_width - min_width)*((parameter - minParameter)/(maxParameter - minParameter))) + min_width
                
                
                counter += 1
            
            
            widths = normalizedParameter
            
            
            if parameter_type == 'link':
                
                g = draw_links(model,data['index'], parameter_results=data['element_list'],cmap=cmap,widths=widths)
                
                
                draw_base_elements(model,ax,links=False,nodes=False,tanks=tanks,reservoirs=reservoirs,pumps=pumps,valves=valves)
            
            
            elif parameter_type == 'node':
                
                g = draw_nodes(model,data['index'], parameter_results=data['element_list'],node_size=node_size,cmap=cmap,node_shape=node_shape)
            
            
                draw_base_elements(model,ax,nodes=False,tanks=tanks,reservoirs=reservoirs,pumps=pumps,valves=valves)
            
            
            draw_color_bar(ax,g,cmap)
            
            draw_legend(ax,title=legend_title,pumps=pumps,loc=legend_loc_1)
            
            
            if savefig:
                
                save_fig(model, save_name=save_name)
                
                
        return
