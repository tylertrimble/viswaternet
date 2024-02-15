"""
This example demonstrates how to plot data stored in Excel files.
 The excel_columns input takes in a list of length 2 containing the indices of the columns in the file corresponding to 
 (1) the list of node/link names, and (2) the corresponding data points. 
 Note that the A column of the Excel file is represented by index 0. 
"""

import viswaternet as vis
import matplotlib.pyplot as plt

#Create water network model
model = vis.VisWNModel('Networks/CTown.inp')

#Plot custom data generated in nodalerror_generation.py
model.plot_unique_data(parameter='excel_data', data_file = 'Excel/CTown_pipe_ages.xlsx',
                       parameter_type='link',
                       data_type='unique',excel_columns=[0,1], discrete_legend_loc = 'lower left',
                       color_list = ["red","blue","green", "orange"],
                       pump_color = 'grey', legend_title = 'Pipe Installation Year',
                       reservoir_color = 'navy', tank_color = 'k',
                       save_name = 'figures/example9', dpi = 400)
plt.show()
