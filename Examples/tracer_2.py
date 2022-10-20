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
import visnet.drawing as visplot
import wntr
import matplotlib.pyplot as plt

wn = wntr.network.WaterNetworkModel(r'Networks\CTown.inp')
model = visinit.initialize_model(r'Networks\CTown.inp',network_model=wn)

wn.options.quality.parameter = 'TRACE'

fig, ((ax1,ax2),(ax3,ax4))= plt.subplots(nrows=2,ncols=2,figsize=(18,18))
ax_list=[ax1,ax2,ax3,ax4]

x_coords=[0,0,0,0]
y_coords=[200,-200,-200,200]

tanks = sorted(model['tank_names'])

draw_bins_legend=True
for i,(axes,tank,x_coord,y_coord) in enumerate(zip(ax_list,tanks,x_coords,y_coords)):
    wn.options.quality.trace_node = tank
    model = visinit.initialize_model(r'Networks\CTown.inp',network_model=wn)
    visplot.plot_discrete_links(model, 
                             axes, 
                             parameter='quality',
                             value='max',
                             unit='hr',
                             bin_edge_num=2,
                             bins=[0,0.00001],
                             bin_label_list=['No', 'Yes'],
                             legend_loc_2='lower left',
                             legend_title='Trace Present',
                             valves=False,
                             pumps=False,
                             disable_bin_deleting=True,
                             draw_base_legend=False,
                             draw_bins_legend=draw_bins_legend)
    draw_bins_legend=False
    visplot.draw_label(model,
                       axes,
                       labels=[tank],
                       x_coords=[x_coord],
                       y_coords=[y_coord],
                       nodes=[tank],
                       draw_arrow=False,
                       label_font_size=9
                       )
plt.show()