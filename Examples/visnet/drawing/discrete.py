# -*- coding: utf-8 -*-
"""
Created on Sun Oct  2 20:55:15 2022

@author: Tyler
"""
import numpy as np
import matplotlib as mpl
import networkx.drawing.nx_pylab as nxp
from visnet.network import processing
from visnet.utils import save_fig, unit_conversion
from visnet.drawing import base

default_cmap = mpl.cm.get_cmap('autumn_r')


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
               
               
               
               
def plot_discrete_nodes(model,ax,bin_edge_num=5,parameter=None, value=None, unit=None,element_list=None,get_tanks=False,get_reservoirs=False,bins='automatic', bin_size_list = None, bin_shape_list = None,bin_label_list = None, bin_border_list = None, bin_border_width_list = None, savefig=True, tanks=True, reservoirs=True, pumps=True, valves=True,legend=True,legend_title = None, legend_loc_1='upper right', legend_loc_2='lower right',save_name=None, cmap= default_cmap, color_list=None,disable_bin_deleting=False):
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
        
        parameter_results, node_list = processing.get_parameter(model,'node',parameter, element_list=element_list,value=value,tanks=get_tanks,reservoirs=get_reservoirs)
        
        if unit is not None:
            parameter_results = unit_conversion(parameter_results,parameter,unit)
            
            
        binnedResults,binNames = processing.bin_parameter(model,parameter_results,node_list,bin_list=bins, bin_edge_num=bin_edge_num,disable_bin_deleting=disable_bin_deleting) 
        
        
        draw_discrete_nodes(model,ax,binnedResults,binNames,bin_size_list=bin_size_list,bin_shape_list=bin_shape_list, bin_label_list=bin_label_list,bin_border_list = bin_border_list, bin_border_width_list = bin_border_width_list,cmap=cmap, color_list=color_list)
    
    
        base.draw_base_elements(model,ax,nodes=False,tanks=tanks,reservoirs=reservoirs,pumps=pumps,valves=valves)
    
    
        if legend:
            base.draw_legend(ax,bin_list=binNames,title=legend_title,pumps=pumps,loc=legend_loc_1,loc2=legend_loc_2)
    
    
    if savefig:
        
         save_fig(model, save_name=save_name)
         
def plot_discrete_links(model, ax,bin_edge_num=5, parameter=None, element_list=None,value=None, unit=None,bins='automatic', bin_width_list=None, bin_label_list=None,color_list=None,tanks=True, reservoirs=True, pumps=True, valves=True,cmap=default_cmap,legend=True, legend_title=None, legend_loc_1='upper right', legend_loc_2='lower right',savefig=True,save_name=None,disable_bin_deleting=False):
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
        
        parameter_results, link_list = processing.get_parameter(model,'link',parameter, element_list=element_list,value=value)
        
        
        if unit is not None:
            parameter_results = unit_conversion(parameter_results,parameter,unit)
            
        
        binnedResults,binNames = processing.bin_parameter(model,parameter_results,link_list,bin_list=bins, bin_edge_num=bin_edge_num,disable_bin_deleting=disable_bin_deleting)
        
        
        draw_discrete_links(model,ax,binnedResults,binNames,bin_width_list=bin_width_list, bin_label_list=bin_label_list,cmap=cmap, color_list=color_list)
        
        
        base.draw_base_elements(model,ax,nodes=False,links=False,tanks=tanks,reservoirs=reservoirs,pumps=pumps,valves=valves)
        
        
        if legend:
            
            base.draw_legend(ax,bin_list=binNames,title=legend_title,pumps=pumps,loc=legend_loc_1,loc2=legend_loc_2)


    if savefig:
        
         save_fig(model, save_name=save_name)