import visnet.network as visinit
import visnet.drawing as visplot
import matplotlib.pyplot as plt
import os

# Run EPANET2.0 Simulation and store results
model = visinit.initialize_model(r"Networks\Net3.inp")  

cwd = os.getcwd()
# Sets image path to /Images folder
model["image_path"] = cwd + "\Images"  

# Define figure to be drawn to
fig, ax = plt.subplots(figsize=(10, 15))  

# Sets title
plt.title("Pipe Diameters for CTown Network", fontsize=16)  

# Disables frame around figure
ax.set_frame_on(False)


#
visplot.plot_unique_data(
    model, ax, 
    parameter="diameter", 
    unit="in", 
    cmap="Blues",
    bin_width_list=[1,1.4,1.8,2.2,2.6,3,3.4,4.2,5.4,7],
    legend_loc_2="lower left", 
    legend_title="Pipe Diameter (in)",
    legend_sig_figs=0, 
    pump_color="mediumseagreen", 
    pump_width=5,
    tank_shape="h", 
    tank_color="b", 
    tank_border_color="k", 
    tank_border_width=2,  
    reservoir_color="b", 
    reservoir_size=150, 
    reservoir_border_color="k",
    reservoir_border_width=3,
)
plt.show()
