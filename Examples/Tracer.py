# -*- coding: utf-8 -*-
import visnet as vis
import matplotlib.pyplot as plt
#Initialize model
model = vis.network.initialize_model('Networks/Net3Tracer.inp')

#Special Labels
fig, ax = plt.subplots(figsize=(10,15))
#Removes border from figure
plt.box(False)

quality,element_list=vis.network.get_parameter(model,
                                               'link',
                                               element_list=['60','335','329','125','129','131','135','137'],
                                               parameter='quality',
                                               value=48)
vis.drawing.draw_base_elements(model,ax,pumps=False)
g=vis.drawing.draw_links(model,
                         ax,
                         element_list,
                         parameter_results=quality,
                         cmap="winter",
                         widths=vis.utils.normalize_parameter(model,quality,1,3))

vis.drawing.draw_color_bar(ax,
                           g,
                           cmap='winter',
                           color_bar_title="Tracer (%)")
plt.show()