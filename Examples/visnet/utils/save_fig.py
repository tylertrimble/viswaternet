# -*- coding: utf-8 -*-
"""
Created on Sun Oct  2 20:45:17 2022

@author: Tyler
"""
import matplotlib.pyplot as plt

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
    
    
    plt.savefig(model['image_path']+image_path2,bbox_inches='tight')
  