# -*- coding: utf-8 -*-
"""
Created on Sun Oct  2 20:58:38 2022

@author: Tyler
"""
import networkx.drawing.nx_pylab as nxp
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from visnet.utils import save_fig

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
    
    
    
    
def draw_label(model,ax,labels,x_coords,y_coords,nodes=None,draw_arrow=True):
    
    
    if nodes is not None:
        
        for label, node, xCoord, yCoord in zip(labels, nodes, x_coords, y_coords): 
            
            if draw_arrow:
                edge_list = []
                if label == node:
                    pass
                else:
                    model['G'].add_node(label,pos=(xCoord,yCoord))
                    
                    model['pos_dict'][label]=(model['wn'].get_node(node).coordinates[0]+xCoord,model['wn'].get_node(node).coordinates[1]+yCoord)
                    
                    edge_list.append((node,label))
                    
                    nxp.draw_networkx_edges(model['G'], model['pos_dict'], edgelist = edge_list,edge_color = 'g',width=0.8,arrows=False) 
                    
                    model['G'].remove_node(label)
                    model['pos_dict'].pop(label,None)
                    edge_list.append((node,label)) 
            if xCoord < 0:    
                plt.text(model['wn'].get_node(node).coordinates[0]+xCoord,model['wn'].get_node(node).coordinates[1]+yCoord,s = label, bbox=dict(facecolor='mediumaquamarine', alpha=0.9, edgecolor='black'),horizontalalignment='right',verticalalignment='center', fontsize = 11)
            if xCoord >= 0:    
                plt.text(model['wn'].get_node(node).coordinates[0]+xCoord,model['wn'].get_node(node).coordinates[1]+yCoord,s = label, bbox=dict(facecolor='mediumaquamarine', alpha=0.9, edgecolor='black'),horizontalalignment='left',verticalalignment='center', fontsize = 11)
            
            
             
    elif nodes is None:
        
        for label, xCoord, yCoord in zip(labels, x_coords, y_coords):
            
            plt.text(xCoord,yCoord,s = label, bbox=dict(facecolor='mediumaquamarine', alpha=0.9, edgecolor='black'),horizontalalignment='right', fontsize = 11,transform=ax.transAxes)