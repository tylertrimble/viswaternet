==========
Visnetwork
==========


.. image:: https://img.shields.io/pypi/v/viswaternet.svg
        :target: https://pypi.python.org/pypi/viswaternet

.. image:: https://readthedocs.org/projects/visnet/badge/?version=latest
        :target: https://visnet.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status




A python package for easy generation and customization of water network graphs.


* Free software: MIT license
* Documentation: https://visnet.readthedocs.io.

Dependencies
------------
* Python 3.7+
* Numpy
* Pandas
* Matplotlib
* NetworkX
* imageio

Features
--------
Viswaternet is designed to plot simulation data onto a network graph, with a large variety of customization options available. The package includes the capabilities to:

* Discretize network or simulation data.
* Visualize discretized or continuous data on network graphs.
* Import data from excel files or data generated with python.
* Create GIFs of data across simulation timesteps.
* Customize style of virtually every element of the network graph, including: reservoirs, tanks, valves, pumps, links, and nodes.
* Draw labels relative to nodes or based on an absolute position on the figure.
* Draw specific nodes or links with their own data and style.

Getting Started
---------------
To get started, import both viswaternet and matplotlib.pyplot:

.. code:: python

    import viswaternet as vis
    import matplotlib.pyplot as plt

Next, initialize a matplotlib figure and viswaternet model. For example purposes we use the CTown network included in the Examples folder:

.. code:: python

    fig, ax = plt.subplots(figsize=(12, 12))
    model = vis.VisWNModel(r'Networks/CTown.inp')
    
Finally, call on any of the plotting functions with the argument inputs of your choice. For example:

.. code:: python

    model.plot_discrete_nodes(ax,parameter="quality",value='max',unit="hr")

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
