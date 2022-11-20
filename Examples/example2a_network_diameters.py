import viswaternet as vis
import matplotlib.pyplot as plt
import numpy as np

# Run EPANET2.0 Simulation and store results
model = vis.VisWNModel(r"Networks/CTown.inp")  

# Define figure to be drawn to
fig, ax = plt.subplots(figsize=(12, 12))  

# Disables frame around figure
ax.set_frame_on(False)

#Plots pipe diameters
model.plot_unique_data(
    ax, 
    parameter="diameter", 
    unit="in", 
    interval_link_width_list=np.linspace(1,7,10),
    cmap="Blues", #Controls link widths
    legend_loc_2="lower left", #Location of legend with bins
    legend_title="Pipe Diameter (in)",font_size=12,
    legend_sig_figs=0, #Whole numbers only
    pump_color="mediumseagreen", 
    pump_width=5, #In Pixels
)
plt.show()
