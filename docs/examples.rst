====================
Example Applications
====================

Example 1 - Basic Network Layout Plots
-----------------------------

This example demonstrates the basic plotting functionality provided by VisWaterNet. The plot_basic_elements function is used to generate a view of the network layout, depicting the locations of nodes (junctions, tanks, and reservoirs) and links (pipes, pumps, and valves).

1.  Import the VisWaterNet and matplotlib.pyplot packages 

.. code:: python

    import viswaternet as vis
    import matplotlib.pyplot as plt
    
2. Initialize a VisWaterNet model object for the .INP file of the water distribution network

.. code:: python

    model = vis.VisWNModel("CTown.inp")

3. Initialize and customize a matplotlib figure and axis

.. code:: python

    fig, ax = plt.subplots(figsize=(11,11))  
    ax.set_frame_on(False) # remove frame from figure

4. Create a basic network plot

.. code:: python

    model.plot_basic_elements(ax)

.. _basic1:
.. figure:: figures/eg_plot_1.png
   :scale: 100 %
   :alt: Basic network layout

5. Customize the basic network plot

.. code:: python

    model.plot_basic_elements(ax, legend_loc = 'upper left', 
                              tank_color = 'g', pump_line_style = ':')

.. _basic2:
.. figure:: figures/eg_plot_2.png
   :scale: 100 %
   :alt: Basic network layout modified


All customization inputs can be found `here`_.

.. _`here`: https://viswaternet.readthedocs.io/en/latest/source/viswaternet.drawing.html#viswaternet.drawing.base.draw_base_elements

Example 2 - Continuous Data Plots
-----------------------------
 
This example demonstrates how to visualize data in a continuous manner, i.e., by assigning colors according to a color bar (or gradient scale).

1. Import packages and initialize VisWaterNet model object and matplotlib figure and axis using steps 1 - 3 in Example 1.

2. Create a continuous data plot for nodal pressure at hour 10.

.. code:: python

    model.plot_continuous_nodes(ax, parameter = "pressure", value = 10)
    
.. _basic3:
.. figure:: figures/eg_plot_3.png
   :scale: 100 %
   :alt: Continuous node plot

3. Create a continuous data plot for mean flow rate over the simulation duration. Here, we change the color map and vary the width of the links (between :code:`min_width` and :code:`max_width`) according to the link flow rate value.

.. code:: python

    model.plot_continuous_links(ax, parameter = "flowrate", value = 'mean', cmap = 'summer_r', min_width = 2, max_width = 6)

.. _basic4:
.. figure:: figures/eg_plot_4.png
   :scale: 100 %
   :alt: Continuous link plot

Example 3 - Discrete Data Plots
-----------------------------
 
This example demonstrates how to visualize data in a discete manner, i.e., by grouping data into intervals and assigning colors according to each interval shown in a legend.

1. Import packages and initialize VisWaterNet model object and matplotlib figure and axis using steps 1 - 3 in Example 1.

2. Create a discrete data plot for nodal demand at hour 10.

.. code:: python

    

3. Create a discrete data plot for mean flow rate over the simulation duration.

.. code:: python

    

Example 4 - Discrete Data Plots
-----------------------------
 
This example demonstrates how to visualize data in a discete manner, i.e., by grouping data into intervals and assigning colors according to each discrete interval as shown in a legend.

1. Import packages and initialize VisWaterNet model object and matplotlib figure and axis using steps 1 - 3 in Example 1.

2. Create a discrete data plot for nodal demand at hour 10.

.. code:: python

    

3. Create a discrete data plot for mean flow rate over the simulation duration.

.. code:: python

    


Example 5 - Categorical Data Plot
-----------------------------
 
This example demonstrates how to visualize categorical data, i.e., specific properties of nodes or links are represented as a fixed set of categories.

1. Import packages and initialize VisWaterNet model object and matplotlib figure and axis using steps 1 - 3 in Example 1.

2. Create a discrete data plot for nodal demand at hour 10.

.. code:: python

    

3. Create a discrete data plot for mean flow rate over the simulation duration.

.. code:: python

    

