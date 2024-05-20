"""
In this example, we demonstrate how to draw attention to specific nodes or links in VisWaterNet by highlighting 
and labeling specific elements.
"""

# Import libraries
import viswaternet as vis
import matplotlib.pyplot as plt

# Initialize VisWaterNet model
model = vis.VisWNModel('Networks/CTown.inp')
style = vis.NetworkStyle(base_legend_loc='lower left',
                         dpi=400)
# Initialize a Matplotlib figure and axis.
fig, ax = plt.subplots(figsize=(11, 11))
ax.set_frame_on(False)

# Plot basic network layout
model.plot_basic_elements(ax,style=style)

# Highlight specific nodes
model.draw_nodes(ax,

                 node_list=['J37', 'J411'],  # names of nodes to be highlighted

                 # customize highlighted nodes
                 node_color=None, node_size=400, node_border_width=3, node_border_color='r',

                 label='Sensors')

# Add labels to highlighted nodes
model.draw_label(ax=ax,

                 draw_nodes=['J37', 'J411'],  # names of nodes to be labeled
                 labels=['Sensor 1', 'Sensor 2'],  # labels for these nodes
                 # label offset from each node location in x and y directions
                 x_coords=[100, 100], y_coords=[0, 0],

                 # customize label text
                 label_text_color='b', label_font_style='italic', label_font_size=15,
                 label_alpha=0.9, label_face_color='pink', label_edge_color='k', label_edge_width=4)  # customize label box

# Save figure
fig.tight_layout()
fig.savefig('figures/example16CTown', dpi=400)
plt.show()
