# -*- coding: utf-8 -*-
import visnet010 as vis
import matplotlib.pyplot as plt
#Initialize model
model = vis.initialize_model('Networks/Net3Tracer.inp')

#Special Labels
fig, ax = plt.subplots(figsize=(10,15))
#Removes border from figure
plt.box(False)

quality,element_list=vis.get_parameter(model,'link',element_list=['60','335','329','125','129','131','135','137'],parameter='quality',value=48)
vis.draw_base_elements(model,ax,pumps=False)
g=vis.draw_links(model,ax,element_list,parameter_results=quality,cmap="winter",widths=vis.normalize_parameter(model,quality,3,3))
vis.draw_color_bar(ax,g,cmap='winter',color_bar_title="Tracer (%)")