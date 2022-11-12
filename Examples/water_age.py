import visnet as vis
import matplotlib.pyplot as plt

#Create visnet model
model = vis.VisnetModel(r"Networks/CTown.inp")  

# Define figure to be drawn to
fig, ax = plt.subplots(figsize=(12, 12))  

# Disables frame around figure
ax.set_frame_on(False)
#Plot maximum water age in hours
model.plot_discrete_nodes(
    ax,
    parameter="quality",value='max',unit="hr",
    num_intervals=5,intervals=[0,6,12,24,48],
    interval_node_size_list=[100,150,250,350,450], #Node sizes
    interval_node_border_color_list=['k','k','k','k','k'],
    interval_node_border_width_list=[1,1,1,1,1],
    cmap='Greens',legend_loc_2="lower left",
    legend_title="Max Water Age (hr)",font_color="k",
    legend_title_font_size="16",
    legend_sig_figs=0, #No decimal places
    pumps=False,valves=False,
)
plt.show()
