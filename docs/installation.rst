.. highlight:: shell

============
Installation
============


Stable release
--------------

To install VisWaterNet, run this command in your terminal:

.. code-block:: console

    $ pip install viswaternet

This is the preferred method to install VisWaterNet, as it will always install the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/


From sources
------------

The sources for VisWaterNet can be downloaded from the `Github repo`_.

You can either clone the public repository:

.. code-block:: console

    $ git clone git://github.com/tylertrimble/viswaternet

Or download the `tarball`_:

.. code-block:: console

    $ curl -OJL https://github.com/tylertrimble/viswaternet/tarball/master

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ python setup.py install


.. _Github repo: https://github.com/tylertrimble/viswaternet
.. _tarball: https://github.com/tylertrimble/viswaternet/tarball/master


Dependencies
--------------

VisWaterNet relies on the following dependencies:

* WNTR 0.2.2+
* Numpy
* Pandas
* Matplotlib 3.5.0+
* NetworkX 2.7+
* imageio

and has been tested on Python 3.8, 3.9, and 3.10.

