# -*- coding: utf-8 -*-
"""
Created on Sat Oct  8 17:18:55 2022

@author: Tyler
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Oct  8 16:36:38 2022

@author: Tyler
"""
import visnet.network as visinit
import visnet.drawing as visplotz

import matplotlib.pyplot as plt
import os
#Initialize model
model = visinit.initialize_model(r'Networks\Net3.inp')

#Define the file path for images. By default, this is the location where the python file is located.
#Because of how Jupyter Notebook works, a relative path from the notebook can not be obtained.
cwd = os.getcwd()
model['image_path'] = cwd + '\Images'
#Defines a matplotlib figure and axis. The user can customize the size of the plot in this way.
#Defines a matplotlib figure and axis. The user can customize the size of the plot in this way.
fig, ax = plt.subplots(figsize=(10,15))
#Removes border from figure
ax.set_frame_on(False);
#Removes border from figure

#Plots diameter.
visplot.plot_unique_data(model, ax, parameter='diameter',cmap='Blues',
                         unit='in',
                         bin_width_list=[2,2.4,2.8,3.2,3.6,4,4.4,4.8,5.2,5.6],
                         legend_loc_2='lower left',
                         legend_title='Pipe Diameter (in)',
                         font_color='k')