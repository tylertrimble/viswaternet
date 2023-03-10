"""
This example demonstrates how to plot EPANET simulation results
"""

import viswaternet as vis
import matplotlib.pyplot as plt

#Create visnet model
model = vis.VisWNModel('Networks/CTown.inp')  

#Plot maximum water age in hours
model.plot_discrete_nodes(parameter = "quality", value = 'max', unit = "hr",     
                          num_intervals = 4, intervals = [0,6,12,24,48],
                          interval_node_size_list = [100,150,250,350,450], 
                          interval_node_border_color_list = ['k','k','k','k','k'],
                          interval_node_border_width_list = [1,1,1,1,1],    
                          cmap = 'Greens', legend_loc_2 = "lower left",    
                          legend_title_font_size="16",
                          legend_sig_figs=0, 
                          save_name = 'figures/example12', dpi=400)
plt.show()
