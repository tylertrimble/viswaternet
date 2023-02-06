.. image:: https://github.com/tylertrimble/viswaternet/blob/master/logo/viswaternet_logo.png?raw=true
		:target: https://github.com/tylertrimble/viswaternet/blob/master/logo/viswaternet_logo.png?raw=true

.. image:: https://img.shields.io/pypi/v/viswaternet.svg
        :target: https://pypi.python.org/pypi/viswaternet

.. image:: https://readthedocs.org/projects/viswaternet/badge/?version=latest
        :target: https://viswaternet.readthedocs.io/en/latest/
        :alt: Documentation Status




A Python package for easy generation and customization of water distribution network visualizations.


* Free software: MIT license
* Documentation: https://viswaternet.readthedocs.io.

Dependencies
------------
* Python 3.7+
* Numpy
* Pandas
* Matplotlib 3.3.0+
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

Installation
---------------
To install VisWaterNet, run this command in your terminal:

.. code:: python

    pip install viswaternet
    
Alternatively, the sources for VisWaterNet can be downloaded from the Github repo. You can clone the public repository:

.. code:: python

    git clone git://github.com/tylertrimble/viswaternet

Once you have a copy of the source, you can install it with:

.. code:: python

    python setup.py install

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

Contact
-------
Tyler Trimble - tylerl.trimble@utexas.edu

Meghna Thomas - meghnathomas@utexas.edu

Lina Sela - linasela@utexas.edu

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
