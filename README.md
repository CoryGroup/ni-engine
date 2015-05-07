# NI-Engine

Ni-Engine is a library designed to make experiments with 
the NIST Neutron interferometer easy. It provides a simple
interface to the equipment at NIST and allows recording of 
data in an easy to use fashion to HDF files. Simple scripts 
can be written that greatly reduce the entry level complexity
of inteferometry experiments and still allow advanced 
experiments to be written. A sample experiment can be as simple
as: 

    from ni_engine import NiEngine

Import the main class from the library

    import quantities as pq

Import a library to make use of units in python

    import numpy as np

Import numpy for its linear algebra functionality 

    n = NiEngine('path/to/configuration.yml')

Create an instance of NiEngine from an experiment 
configuration file. 

    sensor_manager = n.sensor_manager 
    controller_manager = n.controller_manager 

Get instances of the sensor and controller managers
which contain references to all sensors and controllers

    motor = controller_manager.get_controller('motor')

On the assumption that we have defined a motor of 
the `Newport301Axis` in our configuration file we get a 
reference to the motor object:: 
````
    # an array of all the positions we want to test
    positions = np.linspace(0,10,21) * pq.deg 

    #cycle through all positions
    for x in positions: 
        #move motor to position
        motor.move_absolute(x)
        #measure all sensors and store to file
        sensor_manager.measure_all()
        #record the status of all controllers (which will include position)
        controller_manager.get_all_status()
````

In this simple example we have created an experiment to cycle
the motor stage through 21 positions between 0 and 10 degrees. 
At each step the position and data from all sensors is recorded 
to a file for later analysis as specified in the documentation. 


## Installing on Ubuntu 

It is recommended that one uses Python virtualenvs (but not necessary) in order to seperate dependencies from other
python enviroments. 

Update the Ubuntu package repository 
    sudo apt-get update

Install required libraries 
    sudo apt-get install git python-pip python-dev hdf5-tools libhdf5-dev

Install required python packages via pip 
    sudo pip install sphinx numpydoc numpy numexpr cython tables futures pyyaml flufl.enum quantities

Install Labjack driver 
    cd ~
    git clone https://github.com/labjack/LabJackPython.git
    cd LabJackPython
    sudo python setup.py install

Install driver for Labjack usb on Unix 
    cd ~
    git clone git://github.com/labjack/exodriver.git
    cd exodriver
    sudo ./install.sh

Install Instrument kit 
    cd ~
    git clone https://github.com/Galvant/InstrumentKit.git
    cd InstrumentKit/instruments
    sudo python setup.py install

Install Ni-Engine 
    git clone https://github.com/CoryGroup/ni-engine.git
    cd ni-engine/
    sudo python setup.py install


Test Ni-Engine if you have a labjack installed. 
    cd ~/ni-engine/src/
    python ni_engine/examples/current_test.py  
    
##Building Documentation


###Building 


The Ni-Engine documentation uses the python documentation tool [Sphinx](http://sphinx-doc.org/).
You must install it on your system along with the following sphinx modules:

* [Numpy-Docs] (https://pypi.python.org/pypi/numpydoc)

After installation the documentation can than be built by navigating to the **doc**
directory and entering the command

    make html

For other options enter 

    make
On windows 
    .\make.bat html

###Generating API


To get rid of a lot of manual labour the API is generated using
[sphinx-apidoc](http://sphinx-doc.org/man/sphinx-apidoc.html) . If in the 
source directory it can be run like so::

    sphinx-apidoc -n -o api ../../src/ni_engine

This will run a dry run. Make sure everything looks correct and than run::

    sphinx-apidoc -f -o api ../../src/ni_engine

This will build the documentation and place it in the source/api folder.
Now when you go to build the documentation there may be errors due to modules
being documented that should not be. Delete their corresponding .rst files 
in the api directory. 
