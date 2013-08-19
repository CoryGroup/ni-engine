
Installation
============

Ni-Engine is very easy to install, however it has some required dependencies. 


* `python quantities <http://pythonhosted.org/quantities/user/installation.html>`_  
* `numpy <http://www.scipy.org/install.html>`_
* `python futures <https://pypi.python.org/pypi/futures>`_
* `pytables <http://www.pytables.org/moin>`_
* `instrument kit <https://github.com/Galvant/InstrumentKit>`_
* `pyyaml <http://pyyaml.org/wiki/PyYAMLDocumentation>`_
* `LabjackPython <http://labjack.com/support/labjackpython>`_
* `flufl.enum <http://pythonhosted.org/flufl.enum/>`_

And an optional dependency as there is no support for linux systems.

* `PyDAQmx <http://pythonhosted.org/PyDAQmx/>`_

After installation of all required dependencies, The latest version of 
Ni-Engine can be cloned or downloaded from the
`repository <https://github.com/CoryGroup/ni-engine>`_. After retrieving
the source code navigate into the directory

>>> cd ni_engine/src

And then install the library

>>> python setup.py install 

To test that the installation was successful open up a python 
interpreter session and enter 

>>> import ni_engine 

If no errors occur than installation was successful!