# -*- coding: utf-8 -*-
"""
Created on Sun Oct  2 21:14:38 2022

@author: Tyler
"""
import numpy as np
import matplotlib.pyplot as plt
import imageio
import os
from visnet.network import processing
from visnet.drawing import discrete, continuous

cbar=0

def animate_plot(model,ax,function,fps=3,first_timestep=0,last_timestep=None,gif_save_name='gif',**kwargs):
    
    timesteps = int(model['wn'].options.time.duration/model['wn'].options.time.report_timestep)
    values = range(timesteps)
    if last_timestep is not None:
        values = values[first_timestep:last_timestep]
    
    filenames = []
    if function == continuous.plot_continuous_links or function == continuous.plot_continuous_nodes:
        if kwargs.get('vmin',None) is None or kwargs.get('vmax',None) is None:
            if function == continuous.plot_continuous_links:
                parameter_results, link_list = processing.get_parameter(model,'link',kwargs.get('parameter'),kwargs.get('value',None))
            if function == continuous.plot_continuous_nodes:
                parameter_results, node_list = processing.get_parameter(model,'node',kwargs.get('parameter'),kwargs.get('value',None))
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
    if function == discrete.plot_discrete_links or function == discrete.plot_discrete_nodes:
        kwargs['disable_bin_deleting'] = True
        
        if kwargs.get('bins',None) is None:
            if function == discrete.plot_discrete_links:
                parameter_results, link_list = processing.get_parameter(model,'link',kwargs.get('parameter'),kwargs.get('value',None))
                
            if function == discrete.plot_discrete_nodes:
                parameter_results, node_list = processing.get_parameter(model,'node',kwargs.get('parameter'),kwargs.get('value',None))
            
            kwargs['bins'] = np.linspace(np.min(np.min(parameter_results)),np.max(np.max(parameter_results)),kwargs.get('bin_edge_num',5))
    for value in values:
        
        function(model,ax,value=value,**kwargs)
        
        
        handles, labels = [], []
        
        
        plt.legend(handles, labels, title = 'Timestep ' + str(value*model['wn'].options.time.report_timestep) + " Seconds", loc='lower left',frameon=False)
        
        
        plt.savefig(model['image_path'] + '\\' + str(value) + '.png')
        
        
        filenames = np.append(filenames, model['image_path'] + '\\' + str(value) + '.png')
        ax.clear()
        if function == continuous.plot_continuous_links or function == continuous.plot_continuous_nodes:
           cbar.remove()
        
    # builds gif
    with imageio.get_writer(model['image_path'] + '\\' + gif_save_name + '.gif', mode='I',fps=fps) as writer:
        
        for filename in filenames:
            
            image = imageio.imread(filename)
            
            
            writer.append_data(image)
        
        
        for filename in set(filenames):
            
            os.remove(filename)