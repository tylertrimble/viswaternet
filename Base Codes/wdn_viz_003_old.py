# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 03:57:36 2022

@author: Tyler
"""

import wntr
import numpy as np
import matplotlib.pyplot as plt
from wntr.epanet.util import *
import networkx.drawing.nx_pylab as nxp
import matplotlib.colors as colors
import matplotlib as mpl
from matplotlib import cm
import matplotlib.patches as mpatches
import os
import pandas as pd
import time

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

def convertExcel(data):
    node_list= {}
    dirname = os.path.dirname(__file__)
    dataFile = os.path.join(dirname, 'Excel', data)
    df = pd.read_excel(dataFile,dtype=str)
    headers = df.columns

    for header in headers:
        node_list[header] = {}
        for node in df.loc[:,header].dropna():
            node_list[header][node] = node

    return node_list, headers
            
    
def binParameter(parameterResults,binList,binNum):
    if binList == 'Automatic':
        bins=binNum
        binList = np.linspace(np.min(parameterResults),np.max(parameterResults),bins)
    binnedParameter = {}
    binNames = []
    junctionNames = list(parameterResults.index)
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
                        binnedParameter['{0:1.3f} - {1:1.3f}'.format(binList[i], binList[i+1])][junctionNames[counter]] = junctionNames[counter]
                if parameter < binList[i]:
                        binnedParameter['< {0:1.3f}'.format(binList[i])][junctionNames[counter]] = junctionNames[counter]
                counter += 1
        elif i == len(binList) - 2:
            counter = 0
            for parameter in parameterResults:
                if parameter >= binList[i] and parameter <= binList[i+1]:
                        binnedParameter['{0:1.3f} - {1:1.3f}'.format(binList[i], binList[i+1])][junctionNames[counter]] = junctionNames[counter]
                counter += 1
        elif (i<len(binList) - 2) == True:
            counter = 0
            for parameter in parameterResults:
                if parameter >= binList[i] and parameter < binList[i+1]:
                        binnedParameter['{0:1.3f} - {1:1.3f}'.format(binList[i], binList[i+1])][junctionNames[counter]] = junctionNames[counter]
                counter += 1
                
        elif i == len(binList) - 1:
            counter = 0
            for parameter in parameterResults:
                if parameter > binList[i]:
                    binnedParameter['> {0:1.3f}'.format(binList[i])][junctionNames[counter]] = junctionNames[counter]
                counter += 1
                
    for binName in binNames:
        if len(binnedParameter[binName]) == 0:
            binNames = np.delete(binNames,np.where(binNames == binName))
            del binnedParameter[binName]
    return binnedParameter, binNames

def binLinkParameter(parameterResults,binList,binNum):
    if binList == 'Automatic':
        bins=binNum
        binList = np.linspace(np.min(parameterResults),np.max(parameterResults),bins)
    binnedParameter = {}
    binNames = []
    junctionNames = list(parameterResults.index)
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
                        binnedParameter['{0:1.3f} - {1:1.3f}'.format(binList[i], binList[i+1])][junctionNames[counter]] = int(counter)
                if parameter < binList[i]:
                        binnedParameter['< {0:1.3f}'.format(binList[i])][junctionNames[counter]] = counter
                counter += 1
        elif i == len(binList) - 2:
            counter = 0
            for parameter in parameterResults:
                if parameter >= binList[i] and parameter <= binList[i+1]:
                        binnedParameter['{0:1.3f} - {1:1.3f}'.format(binList[i], binList[i+1])][junctionNames[counter]] = int(counter)
                counter += 1
        elif (i<len(binList) - 2) == True:
            counter = 0
            for parameter in parameterResults:
                if parameter >= binList[i] and parameter < binList[i+1]:
                        binnedParameter['{0:1.3f} - {1:1.3f}'.format(binList[i], binList[i+1])][junctionNames[counter]] = int(counter)
                counter += 1
                
        elif i == len(binList) - 1:
            counter = 0
            for parameter in parameterResults:
                if parameter > binList[i]:
                    binnedParameter['> {0:1.3f}'.format(binList[i])][junctionNames[counter]] = int(counter)
                counter += 1
                
    for binName in binNames:
        if len(binnedParameter[binName]) == 0:
            binNames = np.delete(binNames,np.where(binNames == binName))
            del binnedParameter[binName]
    
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
    
 
def drawDistinctNodes(model,ax,nodes, binList, binSizeList=None, binLabelList=None, binShapeList=None,cmap='tab10', colorList =  None,legend=True, legendTitle=None, legendLoc='lower right'):
    if binSizeList == None:
        binSizeList = np.ones(len(binList))*300

    
    if binLabelList == None:
        binLabelList = binList
        
    if binShapeList == None:
        binShapeList = []
        for i in range(len(binList)):
            binShapeList = np.append(binShapeList,'.')
    counter = 0
    if (colorList != None and cmap != None) == True or cmap != None:        
        cmap = mpl.cm.get_cmap(cmap)
        cmapValue = 0
        
        for binName in binList:
            nxp.draw_networkx_nodes(model['G'], model['pos_dict'], nodelist = nodes.get(binName).values(), node_size = binSizeList[counter], node_color = cmap(float(cmapValue)), node_shape = binShapeList[counter],label=binLabelList[counter])
            cmapValue += 1/len(binList)
            counter += 1
            
    else:
        for binName in binList:
            nxp.draw_networkx_nodes(model['G'], model['pos_dict'], nodelist = nodes.get(binName).values(), node_size = binSizeList[counter], node_color = colorList[counter], node_shape = binShapeList[counter],label=binLabelList[counter])
            counter += 1
            
    if legend == True:
        drawSpecialLegend(ax,binList,title=legendTitle,loc=legendLoc)
    handles, labels = ax.get_legend_handles_labels()       

def drawDistinctLinks(model,ax,links, binList, binWidthList=None, binLabelList=None,cmap='tab10', colorList =  None,legend=True, legendTitle=None, legendLoc='lower right'):
    if binWidthList == None:
        binWidthList = np.ones(len(binList))*2

    
    if binLabelList == None:
        binLabelList = binList
    counter = 0
    if (colorList != None and cmap != None) == True or cmap != None:        
        cmap = mpl.cm.get_cmap(cmap)
        cmapValue = 0
        
        for binName in binList:
            nxp.draw_networkx_edges(model['G'], model['pos_dict'], edgelist = ([model['G_edge_list'][i] for i in links.get(binName).values()]),edge_color = cmap(float(cmapValue)),width = binWidthList[counter],arrows = False,label=binLabelList[counter])
            cmapValue += 1/len(binList)
            counter += 1
            
    else:
        for binName in binList:
            nxp.draw_networkx_edges(model['G'], model['pos_dict'], edgelist = model['G_edge_list'][links.get(binName).values()],edge_color = colorList[counter],width = binWidthList[counter],arrows = False,label=binLabelList[counter])
            counter += 1
            
    if legend == True:
        drawSpecialLegend(ax,binList,title=legendTitle,loc=legendLoc)
    handles, labels = ax.get_legend_handles_labels()      
        
    
def drawBaseElements(model,ax,resevoirs=True,tanks=True,pumps=True,valves=True,legend=True):
    nxp.draw_networkx_nodes(model['G'], model['pos_dict'], node_size = 30, node_color = 'k')
    
    if resevoirs == True:
        nxp.draw_networkx_nodes(model['G'], model['pos_dict'], nodelist = model['resevoir_names'], node_size = 200, node_color = 'black',linewidths=3,node_shape = 's', label='Resevoirs')
    
    if tanks == True:
        nxp.draw_networkx_nodes(model['G'], model['pos_dict'], nodelist = model['tank_names'], node_size = 200, node_color = 'black',linewidths=3, node_shape = 'd', label='Tanks')
   
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
        drawLegend(ax,pumps=pumps)      

def drawColorBar(model,ax,g,cmap,colorBarTitle, nodeSize = 100, nodeShape = '.'):

    cbar = plt.colorbar(g)
    cbar.set_label(colorBarTitle, fontsize = 15)
def getParameter(model,parameterType,parameter,timestep = None):
    if parameterType == 'Node':
        try:
            if timestep != None:
                parameterResults = model['results'].node[parameter].iloc[timestep]
                elementList = list(parameterResults.index)
            else:
                parameterResults = model['results'].node[parameter]
                elementList = list(parameterResults.index)
            return parameterResults, elementList
        except KeyError:
            parameterResults = model['wn'].query_node_attribute(parameter)
            elementList = list(parameterResults.index)
            return parameterResults, elementList
    else:
        try:
            if timestep != None:
                parameterResults = model['results'].link[parameter].iloc[timestep]
                elementList = list(parameterResults.index)
            else:
                parameterResults = model['results'].link[parameter]
                elementList = list(parameterResults.index)
            return parameterResults, elementList
        except KeyError:
            parameterResults = model['wn'].query_link_attribute(parameter)
            elementList = list(parameterResults.index)
            return parameterResults, elementList


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
    t = time.time()
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
    node_names = wn.node_name_list
    valve_names = wn.valve_name_list
    tank_names = wn.tank_name_list
    resevoir_names = wn.reservoir_name_list
    model['junc_names'] = junc_names
    model['valve_names'] = valve_names
    model['tank_names'] = tank_names
    model['node_names'] = node_names
    model['resevoir_names'] = resevoir_names
    
    pipe_tp =[]
    pipe_tp2 = []
    
    for link_name, link in wn.links():
        pipe_tp.append(link.start_node_name)
        pipe_tp2.append(link.end_node_name)
    
    G = wn.get_graph()
    model['G'] = G
    G_edge_list = list(G.edges())
    model['G_edge_list'] = G_edge_list
    
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
    
    print(time.time() - t)
    return model




def createBasicPlot(model, savefig=False, saveName=None):
    """Creates a basic plot, similar to the default seen in EPANET.
    Arguments:
    model: Saved initilization done with initializeModel
    savefig: Boolean. Determines whether plot is saved to /Images directory"""

    fig, ax = plt.subplots(figsize=(15,25))
    
    drawBaseElements(model,ax,pumps=False,legend=True)
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
    fig, ax = plt.subplots(figsize=(15,25))
    
    demandPatternNodes,patterns = getDemandPatterns(model)
    drawBaseElements(model,ax)  
    drawDistinctNodes(model,ax,demandPatternNodes,patterns,legendTitle='Demand Patterns')

    if savefig == True:
         saveFig(model, saveName=saveName)

def plotDistinctNodes(model, parameter=None, timestep=None, bins='Automatic', binNum=None, binSizeList = None, binShapeList = None,binLabelList = None, savefig=True, tanks=True, resevoirs=True, pumps=True, valves=True,legend=True,legendTitle = None, legendLoc='lower right', saveName=None, cmap='tab10', colorList=None, specialData=None, specialLegendTitle=None):
    fig, ax = plt.subplots(figsize=(15,25))
    drawBaseElements(model,ax,tanks=tanks,resevoirs=resevoirs,pumps=pumps,valves=valves)
    if parameter != None:
        parameterResults, nodeList = getParameter(model,'Node',parameter, timestep=timestep)
        binnedResults,binNames = binParameter(parameterResults,binList=bins, binNum=binNum)
        
        drawDistinctNodes(model,ax,binnedResults,binNames,binSizeList=binSizeList,binShapeList=binShapeList, binLabelList=binLabelList,cmap=cmap, colorList=colorList, legend=legend, legendTitle=legendTitle, legendLoc=legendLoc)
    if specialData != None:
        node_list, headers = convertExcel(specialData)
        drawDistinctNodes(model,ax,node_list,headers, legendTitle=specialLegendTitle)
    
    if savefig == True:
         saveFig(model, saveName=saveName)
   
def plotContinuousNodes(model, parameter=None, timestep=None, tanks=True, resevoirs=True, pumps=True, valves=True,cmap='gist_heat', colorBarTitle=None,nodeSize=100, nodeShape='.',savefig=True, saveName=None):
    fig, ax = plt.subplots(figsize=(15,25))
    drawBaseElements(model,ax,tanks=tanks,resevoirs=resevoirs,pumps=pumps,valves=valves)
    if parameter != None:
        parameterResults, nodeList = getParameter(model,'Node',parameter, timestep=timestep)
    negativeValues = False
    for value in parameterResults:
        if value < -1e-5:
            negativeValues = True
            cmap = 'bwr'
            top = cm.get_cmap('Oranges_r', 128)
            bottom = cm.get_cmap('Blues', 128)

            newcolors = np.vstack((top(np.linspace(0, 1, 128)),
                       bottom(np.linspace(0, 1, 128))))
            newcmp = ListedColormap(newcolors, name='OrangeBlue')
            g = nxp.draw_networkx_nodes(model['G'], model['pos_dict'], nodelist=nodeList,node_size = nodeSize, node_color=parameterResults, cmap=newcmap,node_shape = nodeShape)
            break
    if negativeValues == False:
        g = nxp.draw_networkx_nodes(model['G'], model['pos_dict'], nodelist=nodeList,node_size = nodeSize, node_color=parameterResults, cmap=cmap, node_shape = nodeShape)
    drawColorBar(model,ax,g,cmap,colorBarTitle=colorBarTitle)
    if savefig == True:
        saveFig(model, saveName=saveName)
    
def plotDistinctLinks(model, parameter=None, timestep=None, bins='Automatic', binNum=None, binWidthList=None, binLabelList=None,colorList=None,tanks=True, resevoirs=True, pumps=True, valves=True,cmap='gist_heat',legend=True, legendTitle=None, legendLoc='lower right',savefig=True,saveName=None):
    fig, ax = plt.subplots(figsize=(15,25))
    drawBaseElements(model,ax,tanks=tanks,resevoirs=resevoirs,pumps=pumps,valves=valves)
    if parameter != None:
        parameterResults, linkList = getParameter(model,'Link',parameter, timestep=timestep)
        binnedResults,binNames = binLinkParameter(parameterResults,binList=bins, binNum=binNum)
        drawDistinctLinks(model,ax,binnedResults,binNames,binWidthList=binWidthList, binLabelList=binLabelList,cmap=cmap, colorList=colorList, legend=legend, legendTitle=legendTitle, legendLoc=legendLoc)
    if savefig == True:
         saveFig(model, saveName=saveName)
         
def plotContinuousLinks(model,parameter=None,timestep=None,minWidth=1,maxWidth=5,tanks=True, resevoirs=True, pumps=True, valves=True,cmap='gist_heat',colorBarTitle=None,savefig=True, saveName=None):
    f