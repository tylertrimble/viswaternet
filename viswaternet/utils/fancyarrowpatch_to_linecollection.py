# -*- coding: utf-8 -*-
from matplotlib.collections import LineCollection
import numpy as np

def fancyarrowpatch_to_linecollection(fancyarrowpatch,cmap,vmin,vmax,parameter_results):
    linecollection_colors = [i.get_edgecolor() for i in fancyarrowpatch]
    linecollection_segs = [(i.get_path().vertices[0],i.get_path().vertices[2]) for i in fancyarrowpatch]
    linecollection = LineCollection(linecollection_segs,colors=linecollection_colors)
    linecollection.set_cmap(cmap)
    if vmin is None:
        vmin_path = np.min(parameter_results)
    else:
        vmin_path = vmin
    if vmax is None:
        vmax_path = np.max(parameter_results)
    else:
        vmax_path = vmax
        
    linecollection.set_clim(vmin_path,vmax_path)
    
    return linecollection