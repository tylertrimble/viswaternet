.. highlight:: shell

============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every little bit helps, and credit will always be given. 

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/tylertrimble/viswaternet/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.
* Note that we provide a list of common warning messages at the bottom of this page. If your bug is related to unexpected warning messages, please check there first!

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug" and "help
wanted" is open to whoever wants to implement it. 

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

VisWaterNet could always use more documentation, whether as part of the
official VisWaterNet docs, in docstrings, or even on the web in blog posts,
articles, and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://github.com/tylertrimble/viswaternet/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Get Started!
------------

Ready to contribute? Here's how to set up VisWaterNet for local development.

1. Fork the `viswaternet` repo on GitHub.
2. Clone your fork locally::

    $ git clone git@github.com:your_name_here/viswaternet.git

3. Install your local copy into a virtualenv. Assuming you have virtualenvwrapper installed, this is how you set up your fork for local development::

    $ mkvirtualenv viswaternet
    $ cd viswaternet/
    $ python setup.py develop

4. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

5. When you're done making changes, check that your changes pass flake8 and the
   tests, including testing other Python versions with tox::

    $ flake8 viswaternet tests
    $ python setup.py test or pytest
    $ tox

   To get flake8 and tox, just pip install them into your virtualenv.

6. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

7. Submit a pull request through the GitHub website.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst.

Testing
----

How to run the automated tests:

1. Navigate into the directory containing your local copy of VisWaterNet.
2. Run the following line:

    $ python -m unittest tests/test_viswaternet.py

Deploying
---------

A reminder for the maintainers on how to deploy.
Make sure all your changes are committed (including an entry in HISTORY.rst).
Then run::

$ bump2version patch # possible: major / minor / patch
$ git push
$ git push --tags

Warning Messages
---------

Since VisWaterNet relies on several other packages, and these packages display warnings regarding changes in future package versions, missing data in the input file, etc., we decided not to suppress warning messages. Here, we have compiled a number of common warning messages we run into when using VisWaterNet. 

.. code:: python

    UserWarning: Not all curves were used in "/viswaternet/CTown.inp"; added with type None, units conversion left to user warnings.warn('Not all curves were used in "{}"; added with type None, units conversion left to user'.format(self.wn.name))
    
WNTR displays this warning when the .INP input file contains curves (e.g., to model pump behavior) or patterns (e.g., describing the time-varying demand at junctions) that are not assigned to pumps or junctions.

