Building Documentation
======================

Building 
^^^^^^^^

The Ni-Engine documentation uses the python documentation tool `Sphinx <http://sphinx-doc.org/>`_.
You must install it on your system along with the following sphinx modules:

* `Numpy-Docs <https://pypi.python.org/pypi/numpydoc>`_

After installation the documentation can than be built by navigating to the **doc**
directory and entering the command::

>>> make html

For other options enter ::

>>> make


Generating API
^^^^^^^^^^^^^^

To get rid of a lot of manual labour the API is generated using
`sphinx-apidoc <http://sphinx-doc.org/man/sphinx-apidoc.html>`_ . If in the 
**source** directory it can be run like so::

>>> sphinx-apidoc -n -o api ../../src/ni_engine

This will run a dry run. Make sure everything looks correct and than run::

>>> sphinx-apidoc -f -o api ../../src/ni_engine

This will build the documentation and place it in the **source/api** folder.
Now when you go to build the documentation there may be errors due to modules
being documented that should not be. Delete their corresponding **.rst** files 
in the **api** directory. 