#!/usr/bin/env python
# coding: utf-8

# In[1]:


import wdn_viz_003 as wdn
import matplotlib.pyplot as plt


# In[2]:


#Runs simulations and stores necessary information about network and the simulation in a dataframe
model = wdn.initialize_model('Networks\CTown.inp')
model['image_path'] = 'D:\Class Projects\wdn-viz\Base Codes\Images'

# In[3]:


#Defines a matplotlib figure and axis.
fig, ax = plt.subplots(figsize=(15,25))
#Creates plot of network with basic elements
wdn.plot_basic_elements(model,ax)


# In[4]:


#Plots links and pumps only without legend
fig, ax = plt.subplots(figsize=(15,25))
wdn.plot_basic_elements(model,ax,nodes=False,links=True,reservoirs=False,tanks=False,pumps=True,legend=False)


# In[5]:


#Plots basic elements but does not save the image. The save name can also be changed with save_name function input.
fig, ax = plt.subplots(figsize=(15,25))
wdn.plot_basic_elements(model,ax,savefig=False, save_name='Basic')


# In[6]:


fig, ax = plt.subplots(figsize=(15,25))
#Plots network parameter that does not change with time. 
wdn.plot_discrete_nodes(model,ax,bin_edge_num=5,parameter='elevation',legend=False)


# In[7]:


fig, ax = plt.subplots(figsize=(15,25))
#Plots network parameter that changes with time (pressure, demand, etc.) at timestep 13
wdn.plot_discrete_nodes(model,ax,bin_edge_num=5,parameter='pressure', value=12)


# In[8]:


fig, ax = plt.subplots(figsize=(15,25))
#Plots network max pressure. Can also plot min, mean, or median pressure/other parameters.
wdn.plot_discrete_nodes(model,ax,bin_edge_num=5,parameter='pressure', value='max')


# In[9]:


fig, ax = plt.subplots(figsize=(15,25))
#Plots network max pressure with custom bins
wdn.plot_discrete_nodes(model,ax,bin_edge_num=5,bins=[-0.0001,20,40,60,80],parameter='pressure', value='max')


# In[10]:


fig, ax = plt.subplots(figsize=(15,25))
#Plots network elevation with all customization options used
wdn.plot_discrete_nodes(model,ax,bin_edge_num=5,parameter='elevation',bin_size_list = [100,125,150,175,200], bin_shape_list = ['.','v','8','D','1'], bin_border_list=['b','k','y','b','k'],bin_border_width_list=[1,1.1,0.5,0.9,1],cmap=None,color_list=['#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22'],savefig=True, legend_title= 'Elevation Groups', save_name = 'ElevationMap2')


# In[11]:


fig, ax = plt.subplots(figsize=(15,25))
#Plots network elevation continuously with color bar.
wdn.plot_continuous_nodes(model,ax,parameter='elevation',color_bar_title="Elevation", save_name="ContinuousElevation")


# In[12]:


fig, ax = plt.subplots(figsize=(15,25))
#Plots mean network demand with autumn color map and node shape 'X' with node size 75
wdn.plot_continuous_nodes(model,ax,parameter='demand',value='mean',cmap='autumn',node_shape='X',node_size=75,color_bar_title="Demand", save_name="ContinuousDemand")


# In[13]:


fig, ax = plt.subplots(figsize=(15,25))
#Plots mean flowrate with 5 bin edges.
wdn.plot_discrete_links(model,ax,bin_edge_num=5,parameter='flowrate',value='mean',pumps=False)


# In[14]:


fig, ax = plt.subplots(figsize=(15,25))
#Plots mean flowrate with 5 bin edges with custom bin edges, no reservoirs or tanks and custom cmap
wdn.plot_discrete_links(model,ax,bin_edge_num=5,parameter='flowrate',value='mean',bin_width_list=[1,1,2,2], reservoirs=False,tanks=False,cmap='autumn')


# In[15]:


fig, ax = plt.subplots(figsize=(15,25))
ax.set_facecolor((0.1, 0.1, 0.1))
#Plots continuous mean flowrate, with min_width and max_width being set equal to each other. Uses gray background to better see plot.
wdn.plot_continuous_links(model,ax,parameter='flowrate',value='mean', cmap='bwr', pumps=False, min_width=1,max_width=1)


# In[16]:


fig, ax = plt.subplots(figsize=(15,25))
ax.set_facecolor((0.1, 0.1, 0.1))
#Plots continuous mean flowrate, with min_width and max_width being set to different values. Uses gray background to better see plot.
wdn.plot_continuous_links(model,ax,parameter='flowrate',value='mean', cmap='bwr', pumps=False, min_width=1,max_width=3)


# In[17]:


#Special Labels
fig, ax = plt.subplots(figsize=(15,25))
#Draws distinct elevation.
wdn.plot_discrete_nodes(model,ax,bin_edge_num=5,parameter='elevation')
#Draws label without providing list of nodes. This means that the coordinates provided (the first set being x and the second being y coordinates) are absolute from 0 to 1. 
wdn.draw_label(model,ax,['label','not a label'],[0.5,0.3],[0.1,0.7])
#Draws label by providing list of nodes. This means that coordiantes are relative, and the value you will need to input will depend on the network.
wdn.draw_label(model,ax,['label2','really not a label trust me'],[50,-50],[75,20],nodes=['J511','J411'])


# In[18]:


#Special Labels
fig, ax = plt.subplots(figsize=(15,25))
#Draws distinct elevation.
wdn.plot_discrete_nodes(model,ax,bin_edge_num=5,parameter='elevation')
#Plots red square with black outline at specific nodes
wdn.draw_nodes(model,['J511','J411'],node_size=300,node_color='r',node_shape='s',edge_colors='k',line_widths=2)


# In[19]:


#Combination of distinct nodes + continuous links
fig, ax = plt.subplots(figsize=(15,25))
ax.set_facecolor((0.1, 0.1, 0.1))
wdn.plot_discrete_nodes(model,ax,bin_edge_num=5,parameter='elevation',savefig=True, legend_title= 'Elevation Groups', save_name = 'ElevationMap')

wdn.plot_continuous_links(model,ax,parameter='flowrate',value=11,pumps=False,cmap='bwr',color_bar_title="Flowrate", save_name="ContinuousFlowrate")


# In[20]:


#Subplotting
fig, (ax1,ax2) = plt.subplots(nrows=1, ncols=2,figsize=(25,25),sharex=True,sharey=True)
ax2.set_facecolor((0.1, 0.1, 0.1))

wdn.plot_discrete_nodes(model,ax1,5,parameter='elevation',savefig=True, legend_title= 'Elevation Groups', save_name = 'ElevationMap')

wdn.plot_continuous_links(model,ax2,parameter='flowrate',value=11,pumps=False,cmap='bwr',color_bar_title="Flowrate", save_name="ContinuousFlowrate")


# In[21]:


fig, ax = plt.subplots(figsize=(15,25))
#Plots unique pipe diameters
wdn.plot_unique_data(model,ax,parameter='diameter')


# In[22]:


fig, ax = plt.subplots(figsize=(15,25))
#Plots demand patterns
wdn.plot_unique_data(model,ax,parameter='demand_patterns')


# In[23]:


fig, ax = plt.subplots(figsize=(15,25))
#Plots node tags
wdn.plot_unique_data(model,ax,parameter='tag',cmap='tab10')


# In[24]:


model = wdn.initialize_model('Networks\\NWC_old_stations.inp')
model['image_path'] = 'D:\Class Projects\wdn-viz\Base Codes\Images'
fig, ax = plt.subplots(figsize=(15,25))
#Plots unique data from excel file
wdn.plot_unique_data(model,ax,parameter='NWC Pipes.xlsx',parameter_type='link',data_type='unique',excel_columns=[0,1],reservoirs=False,tanks=False,valves=False)


# In[25]:


fig, ax = plt.subplots(figsize=(15,25))
#Plots continuous excel data
wdn.plot_unique_data(model,ax,parameter='NWC Pipes.xlsx',parameter_type='link',data_type='continuous',excel_columns=[0,3],cmap='autumn_r',max_width=2)


# In[26]:


fig, ax = plt.subplots(figsize=(15,25))
#Plots discrete excel data
wdn.plot_unique_data(model,ax,parameter='NWC Pipes.xlsx',parameter_type='link',data_type='discrete',bin_edge_num=5,excel_columns=[0,3],cmap='autumn_r',max_width=2)


# In[27]:


#Special continuous numerical data in python
import random
fig, ax = plt.subplots(figsize=(15,25))
data = []
index = []

for node in model['node_names']:
    data.append(random.randint(0,100))
    index.append(node)
    
wdn.plot_unique_data(model,ax,parameter='custom_data',data_type='continuous',parameter_type='node',customDataValues=[index,data],cmap='autumn')


# In[28]:


#Special discrete numerical data in python
fig, ax = plt.subplots(figsize=(15,25))
data = []
index = []

for node in model['node_names']:
    data.append(random.randint(0,100))
    index.append(node)
    
wdn.plot_unique_data(model,ax,parameter='custom_data',data_type='discrete',bin_edge_num=5,parameter_type='node',customDataValues=[index,data],cmap='autumn')


# In[29]:


#Animates pressure at all timesteps
fig, ax = plt.subplots(figsize=(15,25))
wdn.animate_plot(model,ax,wdn.plot_discrete_nodes,first_timestep=0,last_timestep=30,bin_edge_num=5,bins=[-0.0001,20,40,60,80],parameter='pressure')

