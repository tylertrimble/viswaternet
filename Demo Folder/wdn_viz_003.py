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




def pattern_match(model,nodePattern,pattern, junc_name,demandPatternNodes):
    """Determines if demand pattern of node is the one specified, then stores 
    it with the apropriate dictionary key.
    Arguments:
    nodePattern: The demand pattern of the node
    pattern: Which pattern the node demand pattern is being checked against
    junc_name: Name of node/junction being checked
    demandPatternNodes: Name of demand pattern dictionary"""
    
    
    if nodePattern == pattern:
        
        demandPatternNodes[pattern][junc_name] = model['node_names'].index(junc_name)
        
        
    return demandPatternNodes




def convert_excel(model,file,dataType,elementIndex,valueIndex):
    """Converts an excel file into the correct dictionary structure needed to
    be used with drawing functions.
    Arguments:
    model: Takes dictionary. Uses input file name to give each image a unique
    name.
    file: Takes string. Location in Directory where excel file is located.
    dataType: Takes string. Type of data that is being extracted. Unique data
    is data that is seperated into groups such as pressure groups. Discrete
    data is numerical and is """
    
    if dataType == 'unique':
        element_list= {}
        dirname = os.path.dirname(__file__)
        dataFile = os.path.join(dirname, 'Excel', file)
        
        
        df = pd.read_excel(dataFile,dtype=str)
        bins = pd.unique(df.iloc[:,valueIndex])
    
    
        for binName in bins:
            
            element_list[binName] = {}
            
            
        for node,data in zip(df.iloc[:,elementIndex].dropna(),df.iloc[:,valueIndex].dropna()):
            
            element_list[data][node] = model['G_pipe_name_list'].index(node)
    
    
        return element_list, bins
    
    if dataType == 'continuous':
        dirname = os.path.dirname(__file__)
        dataFile = os.path.join(dirname, 'Excel', file)
        
        df = pd.read_excel(dataFile)
        element_list = pd.Series(data=df.iloc[:,valueIndex].values,index=df.iloc[:,elementIndex].values)
        data = {}
        data['element_list'] = element_list
        data['index'] = list(element_list.index)
        return data


def save_fig(model, saveName=None):
    """Saves figure to the <file directory>/Images.
    Arguments:
    model: Takes dictionary. Uses input file name to give each image a unique
    name.
    saveName: Takes string. SaveName acts as a prefix for the image file name,
    and is followed by the name of the network."""
    
    networkName = model['inp_file']
    if networkName.endswith('.inp'):
        try:
            prefixRemove =  networkName.rfind('\\')
            networkName =  networkName[prefixRemove+1:]
            
        except:
            "do nothing"
        networkName =  networkName[:-4]
    
    if saveName != None:    
        image_path2 = '\\' + str(saveName) +  networkName + '.png'
        
    else:
        image_path2 = '\\' +  networkName + '.png'
    
    plt.savefig(model['image_path']+image_path2)
  
    
  
    
def get_parameter(model,parameterType,parameter,value = None,tanks=False,reservoirs=False):
    """Gets parameter for each node in the network and stores it in
    parameterResults. Also grabs the indices of the nodes that had that
    parameter.
    Arguments:
    model: Takes dictionary. Utilizes network model and results from WNTR to 
    get parameters.
    parameterType: Takes String. The type of node, can be 'Node' or 'Link'.
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
    
    if parameterType == 'node':
        try:
            if value == None:
                
                parameterResults = model['results'].node[parameter]
                elementList = list(parameterResults.index)
                
                
            else:
                if value == 'max':
                    parameterResults = np.max(model['results'].node[parameter])
                    elementList = list(parameterResults.index)
                elif value == 'min':
                    parameterResults = np.min(model['results'].node[parameter])
                    elementList = list(parameterResults.index)
                elif value == 'mean':
                    parameterResults = np.mean(model['results'].node[parameter])
                    elementList = list(parameterResults.index)
                elif type(value) == int:
                    parameterResults = model['results'].node[parameter].iloc[value]
                    elementList = list(parameterResults.index)
            try:   
                if tanks == False:
                    for tank in model['tank_names']:
                        parameterResults.drop(tank, axis=0, inplace=True)
                        elementList.remove(tank)
                if reservoirs == False:
                    for reservoir in model['reservoir_names']:
                        parameterResults.drop(reservoir, axis=0, inplace=True)
                        elementList.remove(reservoir) 
            
            except KeyError:
                "do nothing"
            
            return parameterResults, elementList
        
        
        except KeyError:
            
            parameterResults = model['wn'].query_node_attribute(parameter)
            elementList = list(parameterResults.index)
            
            try:   
                if tanks == False:
                    for tank in model['tank_names']:
                        parameterResults.drop(tank, axis=0, inplace=True)
                        elementList.remove(tank)
                if reservoirs == False:
                    for reservoir in model['reservoir_names']:
                        parameterResults.drop(reservoir, axis=0, inplace=True)
                        elementList.remove(reservoir)
            except KeyError:
                "do nothing"
                
            return parameterResults, elementList
        
        
    elif parameterType == 'link':
        
        try:
            if value == None:
                parameterResults = model['results'].link[parameter]
                elementList = list(parameterResults.index)
                
                
            else:
                if value == 'max':
                    parameterResults = np.max(model['results'].link[parameter])
                    elementList = list(parameterResults.index)
                elif value == 'min':
                    parameterResults = np.min(model['results'].link[parameter])
                    elementList = list(parameterResults.index)
                elif value == 'mean':
                    parameterResults = np.mean(model['results'].link[parameter])
                    elementList = list(parameterResults.index)
                elif type(value) == int:
                    parameterResults = model['results'].link[parameter].iloc[value]
                    elementList = list(parameterResults.index)   
                    
            return parameterResults, elementList
        
        
        except KeyError:
            
            parameterResults = model['wn'].query_link_attribute(parameter)
            elementList = list(parameterResults.index)

            return parameterResults, elementList




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
    demandPatternNodes = {}
    for pattern in patterns:
        demandPatternNodes[pattern] = {}
        
    for i in range(len(model['junc_names'])):
        for pattern in patterns:
            demandPatternNodes = pattern_match(model,demandPatterns[i],pattern,model['junc_names'][i],demandPatternNodes)
    for pattern in patterns:
        if len(demandPatternNodes[pattern]) == 0:
            patterns = np.delete(patterns,np.where(patterns == pattern))
            del demandPatternNodes[pattern]
    return demandPatternNodes, patterns  
    



def bin_parameter(model,parameterResults,elementList,binEdgeNum,binList='automatic'):
    """Bins results from get_parameter based on user specifications.
    Arguments:
    model: Takes Dictionary. Gets pipe or node name list.
    parameterResults: Takes Series. Results from get_parameter.
    binEdgeNum: Number of bin edges that the user wants.
    binList: List of bin edges. When set to 'Automatic' it will create bin
    edges."""
    
    
    if binList == 'automatic':
        bins=binEdgeNum
        binList = np.linspace(np.min(parameterResults),np.max(parameterResults),bins)
        
        
    binnedParameter = {}
    binNames = []
    
    
    elementsWithParameter = elementList
    elementType = None
    
    
    for elementWithParameter in elementsWithParameter:   
        
        if (elementWithParameter in model['node_names']):
            continue
        
        
        else:
            elementList = model['G_pipe_name_list']
            elementType = "link"
            break
        
        
    if elementType != "link":
        
        elementList = model['node_names']

    for i in range(len(binList)):
        
        if i == 0:
            if np.min(parameterResults) < binList[i]:
                
                binNames = np.append(binNames, '< {0:1.3f}'.format(binList[i]))
                
                
            binNames = np.append(binNames, '{0:1.3f} - {1:1.3f}'.format(binList[i], binList[i+1]))
            
            
        elif (i<len(binList) - 1) == True:
            
            binNames = np.append(binNames, '{0:1.3f} - {1:1.3f}'.format(binList[i], binList[i+1]))
            
            
        elif i == len(binList) - 1:
            
            if np.max(parameterResults) > binList[i]:
                
                binNames = np.append(binNames, '> {0:1.3f}'.format(binList[i]))
                
                
    for binName in binNames:
        
        binnedParameter[binName] = {}


    for i in range(len(binList)):
        
        if i == 0:
            
            counter = 0

            
            for parameter in parameterResults:
                
                if parameter >= binList[i] and parameter < binList[i+1]:
                    
                        binnedParameter['{0:1.3f} - {1:1.3f}'.format(binList[i], binList[i+1])][elementsWithParameter[counter]] = elementList.index(elementsWithParameter[counter])
                        
                        
                if parameter < binList[i]:
                    
                        binnedParameter['< {0:1.3f}'.format(binList[i])][elementsWithParameter[counter]] = elementList.index(elementsWithParameter[counter])
                        
                        
                counter += 1
                
                
        elif i == len(binList) - 2:
            
            counter = 0
            
            
            for parameter in parameterResults:
                
                if parameter >= binList[i] and parameter <= binList[i+1]:
                    
                        binnedParameter['{0:1.3f} - {1:1.3f}'.format(binList[i], binList[i+1])][elementsWithParameter[counter]] = elementList.index(elementsWithParameter[counter])
                        
                        
                counter += 1
                
                
        elif (i<len(binList) - 2) == True:
            
            counter = 0
            
            
            for parameter in parameterResults:
                
                if parameter >= binList[i] and parameter < binList[i+1]:
                    
                        binnedParameter['{0:1.3f} - {1:1.3f}'.format(binList[i], binList[i+1])][elementsWithParameter[counter]] = elementList.index(elementsWithParameter[counter])
                        
                        
                counter += 1
                
                
        elif i == len(binList) - 1:
            
            counter = 0
            
            
            for parameter in parameterResults:
                
                if parameter > binList[i]:
                    
                    binnedParameter['> {0:1.3f}'.format(binList[i])][elementsWithParameter[counter]] = elementList.index(elementsWithParameter[counter])
                    
                    
                counter += 1
                
                
    for binName in binNames:
        
        if len(binnedParameter[binName]) == 0:
            
            binNames = np.delete(binNames,np.where(binNames == binName))
            del binnedParameter[binName]
    
    
    return binnedParameter, binNames



def draw_nodes(model,nodeList,parameterResults=[],nodeSize=300,nodeColor='k',cmap='tab10',nodeShape='.',edgeColors='k',lineWidths=0,label=None):
    if len(parameterResults) != 0:
        
        negativeValues = False
        
        
        for value in parameterResults:
            
            if value < -1e-5:
                
                negativeValues = True
                
                
                cmap = mpl.cm.get_cmap(cmap)
    
    
                g = nxp.draw_networkx_nodes(model['G'], model['pos_dict'], nodelist=nodeList,node_size = nodeSize, node_color=parameterResults,vmax=np.max(parameterResults),vmin=-np.max(parameterResults), cmap=cmap,node_shape = nodeShape,linewidths=lineWidths,edgecolors=edgeColors,label=label)
                
                
                return g
    
    
        if negativeValues == False:
            
            cmap = mpl.cm.get_cmap(cmap)
            
            
            g = nxp.draw_networkx_nodes(model['G'], model['pos_dict'], nodelist=nodeList,node_size = nodeSize, node_color=parameterResults, cmap=cmap, node_shape = nodeShape)
            
            
            return g
        
    else:
        
        nxp.draw_networkx_nodes(model['G'], model['pos_dict'], nodelist=nodeList,node_size = nodeSize, node_color=nodeColor, node_shape = nodeShape,edgecolors=edgeColors,linewidths=lineWidths,label=label)
    
    
    
    
def draw_links(model,linkList,parameterResults=[],edgeColor='k',cmap='tab10',widths=[]):
    
    edgeList = {}
    
    if len(widths) == 0:
        
        widths = np.ones(len(linkList))*1
    
    for i in linkList:
        
        edgeList[i] = linkList.index(i)
    
    
    negativeValues = False
    
    
    if len(parameterResults) != 0:
        
        for value in parameterResults:
            
            if value < -1e-5:
                
                negativeValues = True
                
                
                cmap = mpl.cm.get_cmap(cmap)
                
                
                g = nxp.draw_networkx_edges(model['G'], model['pos_dict'], edgelist=([model['pipe_list'][i] for i in edgeList.values()]), edge_color=parameterResults, edge_vmax=np.max(parameterResults),edge_vmin=-np.max(parameterResults),edge_cmap=cmap,arrows=False,width=widths)
                
                
                return g

        
        if negativeValues == False:
            
            cmap = mpl.cm.get_cmap(cmap)
            
            
            g = nxp.draw_networkx_edges(model['G'], model['pos_dict'], edgelist=([model['pipe_list'][i] for i in edgeList.values()]), edge_color=parameterResults, edge_cmap=cmap, arrows=False,width=widths)
            
            
            return g
            
    else:
        
        nxp.draw_networkx_edges(model['G'], model['pos_dict'], edgelist=([model['pipe_list'][i] for i in edgeList.values()]), edge_color=edgeColor, arrows=False)
    
    
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
    if nodes == True:
        
        nxp.draw_networkx_nodes(model['G'], model['pos_dict'], node_size = 30, node_color = 'k')
        
        
    if reservoirs == True:
        
        nxp.draw_networkx_nodes(model['G'], model['pos_dict'], ax=ax, nodelist = model['reservoir_names'], node_size = 200, node_color = 'black',linewidths=3,node_shape = 's', label='Reservoirs')
    
    
    if tanks == True:
        
        nxp.draw_networkx_nodes(model['G'], model['pos_dict'], ax=ax, nodelist = model['tank_names'], node_size = 200, node_color = 'black',linewidths=3, node_shape = 'd', label='Tanks')
   
    
    if valves == True:
        valve_coordinates = {}
        valveCounter = 0
        
        
        for point1, point2 in model['G_list_valves_only']:
            
            midpoint = [(model['wn'].get_node(point1).coordinates[0] + model['wn'].get_node(point2).coordinates[0])/2,(model['wn'].get_node(point1).coordinates[1] + model['wn'].get_node(point2).coordinates[1])/2]
            
            
            valve_coordinates[model['valve_names'][valveCounter]] = midpoint
            valveCounter += 1
            
            
        nxp.draw_networkx_nodes(model['G'], valve_coordinates, ax=ax, nodelist = model['valve_names'], node_size = 200, node_color = 'orange', edgecolors='black',linewidths=1,node_shape = 'P', label='Valves')
        
    if links == True:   
        nxp.draw_networkx_edges(model['G'], model['pos_dict'], ax=ax, arrows = False, edge_color = 'k')
    
    
    if pumps == True:
        
        nxp.draw_networkx_edges(model['G'], model['pos_dict'], ax=ax, edgelist = model['G_list_pumps_only'], node_size = 200, edge_color = 'b', width=3, arrows=False)  
        
        
     
        
def draw_discrete_nodes(model,ax,nodes, binList, binSizeList=None, binLabelList=None, binShapeList=None,cmap='tab10', binBorderList = None, binBorderWidthList = None, colorList =  None):
    """Draws nodes based off of discrete bins.
    Arguments:
    model: Takes Dictionary.
    ax: Axis of the figure the user wants the elements to be plotted on.
    nodes: Takes Dictionary. List of nodes to be plotted organized by bin 
    into dictionaries.
    binList: Takes List. List of bin names.
    binSizeList: Takes List. List of node sizes for each bin.
    binLabelList: Takes List. List of labels for each bin.
    binShapeList: Takes List. List of markers for each bin.
    cmap: Takes String. Colormap that determines bin colors.
    colorList: Takes List. List of hexadecimal strings that determine bin
    colors. cmap must = None for colorList to take priority."""
    
    
    if binSizeList == None:
        
        if len(model['node_names']) < 300:
            
            binSizeList = np.ones(len(binList))*300
            
            
        elif len(model['node_names']) >= 300 and len(model['node_names']) < 1000:
            
            binSizeList = np.ones(len(binList))*(80000/len(model['node_names']))
            
            
        else:
            
            binSizeList = np.ones(len(binList))*80

    
    if binLabelList == None:
        
        binLabelList = binList
        
        
    if binShapeList == None:
        
        binShapeList = []
        
        
        for i in range(len(binList)):
            
            binShapeList = np.append(binShapeList,'.')
            
    if binBorderList == None:
        binBorderList = []
        
        for i in range(len(binList)):
            
            binBorderList = np.append(binBorderList,'k')
    
    if binBorderWidthList == None:
        binBorderWidthList = []
        
        for i in range(len(binList)):
            
            binBorderWidthList = np.append(binBorderWidthList,0)
            
            
    counter = 0
    
    
    if (colorList != None and cmap != None) == True or cmap != None:    
        
        cmap = mpl.cm.get_cmap(cmap)
        cmapValue = 1/len(binList)
        
        
        for binName in binList:
            
            nxp.draw_networkx_nodes(model['G'], model['pos_dict'], ax=ax, nodelist = ([model['node_names'][i] for i in nodes.get(binName).values()]), node_size = binSizeList[counter], node_color = cmap(float(cmapValue)), node_shape = binShapeList[counter],label=binLabelList[counter], edgecolors = binBorderList[counter],linewidths = binBorderWidthList[counter])
            
            
            cmapValue += 1/len(binList)
            
            
            counter += 1
            
            
    else:
        
        for binName in binList:
            
            nxp.draw_networkx_nodes(model['G'], model['pos_dict'], ax=ax, nodelist = ([model['node_names'][i] for i in nodes.get(binName).values()]), node_size = binSizeList[counter], node_color = colorList[counter], node_shape = binShapeList[counter],label=binLabelList[counter], edgecolors = binBorderList[counter],linewidths = binBorderWidthList[counter])
            
            
            counter += 1




def draw_discrete_links(model,ax,links, binList, binWidthList=None, binLabelList=None,cmap='tab10', colorList =  None):
    """Draws links s based off of discrete bins.
    Arguments:
    model: Takes Dictionary.
    ax: Axis of the figure the user wants the elements to be plotted on.
    links: Takes Dictionary. List of links to be plotted organized by bin 
    into dictionaries.
    binList: Takes List. List of bin names.
    binWidthList: Takes List. List of link widths for each bin.
    binLabelList: Takes List. List of labels for each bin.
    binShapeList: Takes List. List of markers for each bin.
    cmap: Takes String. Colormap that determines bin colors.
    colorList: Takes List. List of hexadecimal strings that determine bin
    colors. cmap must = None for colorList to take priority."""
    
    
    if binWidthList == None:
        
        binWidthList = np.ones(len(binList))*2
        

    if binLabelList == None:
        
        binLabelList = binList
        
        
    counter = 0
    
    
    if (colorList != None and cmap != None) == True or cmap != None:    
        
        cmap = mpl.cm.get_cmap(cmap)
        cmapValue = 1/len(binList)
        
        
        for binName in binList:
            
            nxp.draw_networkx_edges(model['G'], model['pos_dict'], edgelist = ([model['pipe_list'][i] for i in links.get(binName).values()]),edge_color = cmap(float(cmapValue)),width = binWidthList[counter],arrows = False,label=binLabelList[counter])
            
            
            cmapValue += 1/len(binList)
            
            
            counter += 1
            
            
    else:
        
        for binName in binList:
            
            nxp.draw_networkx_edges(model['G'], model['pos_dict'], edgelist = ([model['pipe_list'][i] for i in links.get(binName).values()]),edge_color = colorList[counter],width = binWidthList[counter],arrows = False,label=binLabelList[counter])
            
            
            counter += 1        
        
   
    
    
def draw_legend(ax,binList=[],title=None,pumps=True,loc='upper right',loc2='lower right'):
    """Draws legend for basic elements.
    Arguments:
    ax: Axis of the figure the user wants the elements to be plotted on.
    binList: Takes List. List of bins.
    title: Takes String. Legend title.
    pumps: Takes Boolean. Determines whether pumps are drawn or not.
    loc: Takes String. Location of elements legend.
    loc2 = Takes String. Location of bins legend"""
    
    
    handles, labels = ax.get_legend_handles_labels()
    
    
    if pumps == True:
        
        patch1 = mpatches.Patch(color='blue', label='Pumps')
        patch2 = mpatches.Patch(color='black', label='Pipes')
        
        
        handles.extend([patch1,patch2])
    
    
    else:
        
        patch = mpatches.Patch(color='black', label='Pipes')
        
        
        handles.extend([patch])
    
        
    
    
    if len(binList) != 0:
        legend = ax.legend(handles=handles[len(binList):], loc=loc,fontsize = '15')
        ax.add_artist(legend)
        legend2 = ax.legend(title=title,handles=handles[:len(binList)], loc=loc2,fontsize = '15', title_fontsize = '17')
        ax.add_artist(legend2)
    else:
        legend = ax.legend(handles=handles, loc=loc,fontsize = '15')
        ax.add_artist(legend)
    


    

def draw_color_bar(ax,g,cmap,colorBarTitle=None):
    """Draws Color Bar.
    Arguments:
    g: NetworkX graph of plotted elements.
    cmap: Colormap
    colorBarTitle: Takes String. Title of Color Bar."""

    
    cbar = plt.colorbar(g)
    cbar.set_label(colorBarTitle, fontsize = 15)
    
    
    
    
def draw_label(model,ax,labels,xCoords,yCoords,nodes=None):
    
    
    if nodes != None:
        
        for label, node, xCoord, yCoord in zip(labels, nodes, xCoords, yCoords): 
            
            plt.text(model['wn'].get_node(node).coordinates[0]+xCoord,model['wn'].get_node(node).coordinates[1]+yCoord,s = label, bbox=dict(facecolor='mediumaquamarine', alpha=0.9, edgecolor='black'),horizontalalignment='right', fontsize = 11)
            
            
    elif nodes == None:
        
        for label, xCoord, yCoord in zip(labels, xCoords, yCoords):
            
            plt.text(xCoord,yCoord,s = label, bbox=dict(facecolor='mediumaquamarine', alpha=0.9, edgecolor='black'),horizontalalignment='right', fontsize = 11,transform=ax.transAxes)
    
    
    
    
    
    
    
    
def plot_basic_elements(model, ax,pumps=True,valves=True,reservoirs=True,tanks=True,links=True,nodes=True,savefig=False, saveName=None, drawLegend=True):
    """Creates a basic plot, similar to the default seen in EPANET.
    Arguments:
    model: Saved initilization done with initializeModel
    savefig: Boolean. Determines whether plot is saved to /Images directory"""

    
    draw_base_elements(model,ax,nodes=nodes,reservoirs=reservoirs,tanks=tanks,links=links,valves=valves,pumps=pumps,legend=True)
    
    if drawLegend == True:
        
        draw_legend(ax)
    
    if savefig == True:
        
        save_fig(model, saveName=saveName)




def plot_discrete_nodes(model,ax,binEdgeNum,parameter=None, value=None, getTanks=False,getReservoirs=False,bins='automatic', binSizeList = None, binShapeList = None,binLabelList = None, binBorderList = None, binBorderWidthList = None, savefig=True, tanks=True, reservoirs=True, pumps=True, valves=True,legend=True,legendTitle = None, legendLoc='upper right', legendLoc2='lower right',saveName=None, cmap='tab10', colorList=None):
    """Plots discrete Nodes.
    Arguments:
    figsize: Figure size. Takes a 2-element List.
    parameter: Takes String. The name of the parameter. 
    value: Takes Integer. Parameters from results must include a value 
    with it. The value given is the value index, not time.
    bins: List of bin edges. When set to 'Automatic' it will create bin
    edges.
    binEdgeNum: Number of bin edges that the user wants.
    binList: Takes List. List of bin names.
    binSizeList: Takes List. List of node sizes for each bin.
    binLabelList: Takes List. List of labels for each bin.
    binShapeList: Takes List. List of markers for each bin.
    cmap: Takes String. Colormap that determines bin colors.
    colorList: Takes List. List of hexadecimal strings that determine bin
    colors. cmap must = None for colorList to take priority.
    reservoirs: Takes Boolean. Determines whether to draw reservoirs or not.
    tanks: Takes Boolean. Determines whether to draw tanks or not.
    pumps: Takes Boolean. Determines whether to draw pumps or not.
    valves: Takes Boolean. Determines whether to draw valves or not.
    legend: Takes Boolean. Determines whether to draw legend or not.
    legendTitle: Takes string. Title of legend.
    legendLoc: Takes String. Location of legend.
    savefig: Takes Boolean. Determines if figure is saved or not.
    saveName: Takes string. SaveName acts as a prefix for the image file name,
    and is followed by the name of the network.
    specialData: Takes either Excel file or correctly formatted dictionary. 
    Used to plot custom data."""

    if parameter != None:
        
        parameterResults, nodeList = get_parameter(model,'node',parameter, value=value,tanks=getTanks,reservoirs=getReservoirs)
        
        binnedResults,binNames = bin_parameter(model,parameterResults,nodeList,binList=bins, binEdgeNum=binEdgeNum) 
        
        
        draw_discrete_nodes(model,ax,binnedResults,binNames,binSizeList=binSizeList,binShapeList=binShapeList, binLabelList=binLabelList,binBorderList = binBorderList, binBorderWidthList = binBorderWidthList,cmap=cmap, colorList=colorList)
    
    
        draw_base_elements(model,ax,nodes=False,tanks=tanks,reservoirs=reservoirs,pumps=pumps,valves=valves)
    
    
        if legend == True:
            
            draw_legend(ax,binNames,title=legendTitle,pumps=pumps,loc=legendLoc,loc2=legendLoc2)
    
    
    if savefig == True:
        
         save_fig(model, saveName=saveName)


    


def plot_continuous_nodes(model,ax,parameter=None, value=None, tanks=True, reservoirs=True, pumps=True, valves=True,cmap='gist_heat', colorBarTitle=None,nodeSize=100, nodeShape='.',savefig=True, saveName=None):
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
    legendTitle: Takes string. Title of legend.
    legendLoc: Takes String. Location of legend.
    savefig: Takes Boolean. Determines if figure is saved or not.
    saveName: Takes string. SaveName acts as a prefix for the image file name,
    and is followed by the name of the network.
    specialData: Takes either Excel file or correctly formatted dictionary. 
    Used to plot custom data."""
    
    
    if parameter != None:
        
        parameterResults, nodeList = get_parameter(model,'node',parameter, value=value)
        
        
        g = draw_nodes(model,nodeList,parameterResults=parameterResults,nodeSize=nodeSize,cmap=cmap,nodeShape=nodeShape)
            
        
        draw_base_elements(model,ax,nodes=False,tanks=tanks,reservoirs=reservoirs,pumps=pumps,valves=valves)
        
        
        draw_color_bar(ax,g,cmap,colorBarTitle=colorBarTitle)

        
    if savefig == True:
        
        save_fig(model, saveName=saveName)
  
    
  
    
def plot_discrete_links(model, ax,binEdgeNum, parameter=None, value=None, bins='automatic', binWidthList=None, binLabelList=None,colorList=None,tanks=True, reservoirs=True, pumps=True, valves=True,cmap='gist_heat',legend=True, legendTitle=None, legendLoc='upper right', legendLoc2='lower right',savefig=True,saveName=None):
    """Plots discrete Links.
    Arguments:
    figsize: Figure size. Takes a 2-element List.
    parameter: Takes String. The name of the parameter. 
    value: Takes Integer. Parameters from results must include a value 
    with it. The value given is the value index, not time.
    bins: List of bin edges. When set to 'Automatic' it will create bin
    edges.
    binEdgeNum: Number of bin edges that the user wants.
    binList: Takes List. List of bin names.
    binWidthList: Takes List. List of link widths for each bin.
    binLabelList: Takes List. List of labels for each bin.
    binShapeList: Takes List. List of markers for each bin.
    cmap: Takes String. Colormap that determines bin colors.
    colorList: Takes List. List of hexadecimal strings that determine bin
    colors. cmap must = None for colorList to take priority.
    reservoirs: Takes Boolean. Determines whether to draw reservoirs or not.
    tanks: Takes Boolean. Determines whether to draw tanks or not.
    pumps: Takes Boolean. Determines whether to draw pumps or not.
    valves: Takes Boolean. Determines whether to draw valves or not.
    legend: Takes Boolean. Determines whether to draw legend or not.
    legendTitle: Takes string. Title of legend.
    legendLoc: Takes String. Location of legend.
    savefig: Takes Boolean. Determines if figure is saved or not.
    saveName: Takes string. SaveName acts as a prefix for the image file name,
    and is followed by the name of the network.
    specialData: Takes either Excel file or correctly formatted dictionary. 
    Used to plot custom data."""
    
    if parameter != None:
        
        parameterResults, linkList = get_parameter(model,'link',parameter, value=value)
        
        
        binnedResults,binNames = bin_parameter(model,parameterResults,linkList,binList=bins, binEdgeNum=binEdgeNum)
        
        
        draw_discrete_links(model,ax,binnedResults,binNames,binWidthList=binWidthList, binLabelList=binLabelList,cmap=cmap, colorList=colorList)
        
        draw_base_elements(model,ax,nodes=False,links=False,tanks=tanks,reservoirs=reservoirs,pumps=pumps,valves=valves)
        
        if legend == True:
            
            draw_legend(ax,binNames,title=legendTitle,pumps=pumps,loc=legendLoc,loc2=legendLoc2)


    if savefig == True:
        
         save_fig(model, saveName=saveName)
   
         
   
    
def plot_continuous_links(model,ax,parameter=None,value=None,minWidth=1,maxWidth=5,tanks=True, reservoirs=True, pumps=True, valves=True,cmap='gist_heat',colorBarTitle=None,savefig=True, saveName=None, specialData=None):
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
    legendTitle: Takes string. Title of legend.
    legendLoc: Takes String. Location of legend.
    savefig: Takes Boolean. Determines if figure is saved or not.
    saveName: Takes string. SaveName acts as a prefix for the image file name,
    and is followed by the name of the network.
    specialData: Takes either Excel file or correctly formatted dictionary. 
    Used to plot custom data."""
    
    


    
    if parameter != None:
        
        parameterResults, linkList = get_parameter(model,'link',parameter, value=value)
        minParameter = np.min(parameterResults)
        maxParameter = np.max(parameterResults)
        normalizedParameter = np.copy(parameterResults)
        counter = 0
        
        for parameter in parameterResults:
            normalizedParameter[counter] = ((maxWidth - minWidth)*((parameter - minParameter)/(maxParameter - minParameter))) + minWidth
            counter += 1
        
        widths = normalizedParameter
        g = draw_links(model,linkList,parameterResults=parameterResults,cmap=cmap,widths=widths)
      
    
        draw_base_elements(model,ax,nodes=False,links=False,tanks=tanks,reservoirs=reservoirs,pumps=pumps,valves=valves)
    
    
        draw_color_bar(ax,g,cmap,colorBarTitle=colorBarTitle)
    
    if specialData != None:
        
        g = draw_links(model,specialData['index'],parameterResults=specialData['element_list'],cmap=cmap)
      
    
        draw_base_elements(model,ax,links=False,tanks=tanks,reservoirs=reservoirs,pumps=pumps,valves=valves)
    
    
        draw_color_bar(ax,g,cmap,colorBarTitle=colorBarTitle)
    
    
    if savefig == True:
        
        save_fig(model, saveName=saveName)
    
    
    
    
def animate_plot(model,ax,function,**kwargs):
    values = int(model['wn'].options.time.duration/model['wn'].options.time.report_value)
    
    
    filenames = []
    
    
    for value in range(values):
        
        function(model,value=value,**kwargs)
        
        
        handles, labels = [], []
        
        
        legend3 = plt.legend(handles, labels, title = 'Timestep ' + str(value*model['wn'].options.time.report_value) + " Seconds", loc='lower left')
        
        
        ax.add_artist(legend3)
        
        
        plt.savefig(str(value) + '.png')
        
        
        filenames = np.append(filenames, str(value) + '.png')


    # builds gif
    with imageio.get_writer('mygif.gif', mode='I',fps=3) as writer:
        
        for filename in filenames:
            
            image = imageio.imread(filename)
            
            
            writer.append_data(image)
        
        
        for filename in set(filenames):
            
            os.remove(filename)
def plot_unique_data(model, ax, parameter=None, parameterType=None,dataType=None,excelColumns=None,customDataValues=None, bins='automatic',binSizeList = None, binShapeList = None, binEdgeNum=None, binWidthList=None, binLabelList=None,binBorderList = None, binBorderWidthList = None,colorList=None,minWidth=1,maxWidth=5,tanks=True, reservoirs=True, pumps=True, valves=True,cmap='gist_heat',legend=True, legendTitle=None,nodeSize=100, nodeShape='.',legendLoc='upper right', legendLoc2='lower right',savefig=True,saveName=None,colorBarTitle=None):
    if parameter=='demand_patterns':
        demandPatternNodes,patterns = get_demand_patterns(model)
        draw_discrete_nodes(model,ax,demandPatternNodes,patterns,binSizeList=binSizeList,binShapeList=binShapeList, binLabelList=binLabelList,binBorderList = binBorderList, binBorderWidthList = binBorderWidthList,cmap=cmap, colorList=colorList)
        draw_base_elements(model,ax,nodes=False)  
        
        if legend == True:
            
            draw_legend(ax,patterns,title=legendTitle,pumps=pumps,loc=legendLoc,loc2=legendLoc2)
        if savefig == True:
            save_fig(model, saveName=saveName)
        return
    if parameter=='diameter':
        parameterResults, linkList = get_parameter(model,'link',parameter)
        uniques = pd.unique(parameterResults)
        binNames = []
        for binName in uniques:
            binNames = np.append(binNames,('{:.4f}'.format(binName)))
            
        binnedResults = {}
        for binName in binNames:
            binnedResults[binName] = {}
        
        for link in linkList:
            
            binnedResults['{:.4f}'.format(parameterResults.loc[link])][link] = model['G_pipe_name_list'].index(link)
       
        draw_discrete_links(model,ax,binnedResults,binNames,binWidthList=binWidthList, binLabelList=binLabelList,cmap=cmap, colorList=colorList)
        
        draw_base_elements(model,ax,nodes=False,links=False,tanks=tanks,reservoirs=reservoirs,pumps=pumps,valves=valves)
        
        if legend == True:
            
            draw_legend(ax,binNames,title=legendTitle,pumps=pumps,loc=legendLoc,loc2=legendLoc2)
        if savefig == True:
            
            save_fig(model, saveName=saveName)
        return
    if parameter=='tag':
        parameterResults, nodeList = get_parameter(model,'node',parameter)
        uniques = pd.unique(parameterResults)
        uniques =  uniques[uniques != None]
        binNames = []
        if len(uniques) != 0:
            for binName in uniques:
                binNames = binName
            
        binNames = np.append(binNames,'No Tag')
        
        binnedResults = {}
        for binName in binNames:
            binnedResults[binName] = {}
        
        for node in nodeList:
            if parameterResults.loc[node] == None:
                binnedResults['No Tag'][node] = model['node_names'].index(node)
                continue
            binnedResults[parameterResults.loc[node]][node] = model['node_names'].index(node)
       
        draw_discrete_nodes(model,ax,binnedResults,binNames,binSizeList=binSizeList,binShapeList=binShapeList, binLabelList=binLabelList,binBorderList = binBorderList, binBorderWidthList = binBorderWidthList,cmap=cmap, colorList=colorList)
        
        draw_base_elements(model,ax,nodes=False,tanks=tanks,reservoirs=reservoirs,pumps=pumps,valves=valves)
        
        if legend == True:
            
            draw_legend(ax,binNames,title=legendTitle,pumps=pumps,loc=legendLoc,loc2=legendLoc2)
        if savefig == True:
            
            save_fig(model, saveName=saveName)
        return
    if parameter == 'custom_data':
        if dataType == 'unique':
            if parameterType == 'link':
                draw_discrete_links(model,ax,customDataValues[0], customDataValues[1],binWidthList=binWidthList, binLabelList=binLabelList,cmap=cmap, colorList=colorList)
                
                draw_base_elements(model,ax,links=False,nodes=False,tanks=tanks,reservoirs=reservoirs,pumps=pumps,valves=valves)
            elif parameterType == 'node':
                draw_discrete_nodes(model,ax,customDataValues[0], customDataValues[1],binSizeList=binSizeList,binShapeList=binShapeList, binLabelList=binLabelList,binBorderList = binBorderList, binBorderWidthList = binBorderWidthList,cmap=cmap, colorList=colorList)
            
                draw_base_elements(model,ax,nodes=False,tanks=tanks,reservoirs=reservoirs,pumps=pumps,valves=valves)
            if legend == True:
                
                draw_legend(ax,customDataValues[1],title=legendTitle,pumps=pumps,loc=legendLoc,loc2=legendLoc2)
            if savefig == True:
                
                save_fig(model, saveName=saveName)
            return
        if dataType == 'continuous':
            minParameter = np.min(customDataValues[1])
            maxParameter = np.max(customDataValues[1])
            normalizedParameter = np.copy(customDataValues[1])
            counter = 0
            
            for parameter in customDataValues[1]:
                normalizedParameter[counter] = ((maxWidth - minWidth)*((parameter - minParameter)/(maxParameter - minParameter))) + minWidth
                counter += 1
            
            widths = normalizedParameter
            
            if parameterType == 'link':
                g = draw_links(model,customDataValues[0], parameterResults=customDataValues[1],cmap=cmap,widths=widths)
                
                draw_base_elements(model,ax,links=False,nodes=False,tanks=tanks,reservoirs=reservoirs,pumps=pumps,valves=valves)
            elif parameterType == 'node':
                g = draw_nodes(model,customDataValues[0], parameterResults=customDataValues[1],nodeSize=nodeSize,cmap=cmap,nodeShape=nodeShape)
            
                draw_base_elements(model,ax,nodes=False,tanks=tanks,reservoirs=reservoirs,pumps=pumps,valves=valves)
            draw_color_bar(ax,g,cmap)
            if savefig == True:
                
                save_fig(model, saveName=saveName)
            return
    if type(parameter) == str:
        if dataType == 'unique':
            nodeList, binList = convert_excel(model,parameter,dataType,excelColumns[0],excelColumns[1])
            if parameterType == 'link':
                draw_discrete_links(model,ax,nodeList, binList,binWidthList=binWidthList, binLabelList=binLabelList,cmap=cmap, colorList=colorList)
                
                draw_base_elements(model,ax,links=False,nodes=False,tanks=tanks,reservoirs=reservoirs,pumps=pumps,valves=valves)
            elif parameterType == 'node':
                draw_discrete_nodes(model,ax,nodeList, binList,binSizeList=binSizeList,binShapeList=binShapeList, binLabelList=binLabelList,binBorderList = binBorderList, binBorderWidthList = binBorderWidthList,cmap=cmap, colorList=colorList)
            
                draw_base_elements(model,ax,nodes=False,tanks=tanks,reservoirs=reservoirs,pumps=pumps,valves=valves)
            if legend == True:
                
                draw_legend(ax,binList,title=legendTitle,pumps=pumps,loc=legendLoc,loc2=legendLoc2)
            if savefig == True:
                
                save_fig(model, saveName=saveName)
        if dataType == 'continuous':
            data = convert_excel(model,parameter,dataType,excelColumns[0],excelColumns[1])
            minParameter = np.min(data['element_list'])
            maxParameter = np.max(data['element_list'])
            normalizedParameter = np.copy(data['element_list'])
            counter = 0
            
            for parameter in data['element_list']:
                normalizedParameter[counter] = ((maxWidth - minWidth)*((parameter - minParameter)/(maxParameter - minParameter))) + minWidth
                counter += 1
            
            widths = normalizedParameter
            if parameterType == 'link':
                g = draw_links(model,data['index'], parameterResults=data['element_list'],cmap=cmap,widths=widths)
                
                draw_base_elements(model,ax,links=False,nodes=False,tanks=tanks,reservoirs=reservoirs,pumps=pumps,valves=valves)
            elif parameterType == 'node':
                g = draw_nodes(model,data['index'], parameterResults=data['element_list'],nodeSize=nodeSize,cmap=cmap,nodeShape=nodeShape)
            
                draw_base_elements(model,ax,nodes=False,tanks=tanks,reservoirs=reservoirs,pumps=pumps,valves=valves)
            draw_color_bar(ax,g,cmap)
            if savefig == True:
                
                save_fig(model, saveName=saveName)
        return