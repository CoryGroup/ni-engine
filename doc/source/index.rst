

Welcome to NI-Engine's documentation!
=====================================
Ni-Engine is a library designed to make experiments with 
the NIST Neutron interferometer easy. It provides a simple
interface to the equipment at NIST and allows recording of 
data in an easy to use fashion to HDF files. Simple scripts 
can be written that greatly reduce the entry level complexity
of inteferometry experiments and still allow advanced 
experiments to be written. A sample experiment can be as simple
as: 

>>> from ni_engine import NiEngine

Import the main class from the library

>>> import quantities as pq

Import a library to make use of units in python

>>> import numpy as np

Import numpy for its linear algebra functionality 

>>> n = NiEngine('path/to/configuration.yml')

Create an instance of NiEngine from an experiment 
configuration file. 

>>> sensor_manager = n.sensor_manager 
>>> controller_manager = n.controller_manager 

Get instances of the sensor and controller managers
which contain references to all sensors and controllers

>>> motor = controller_manager.get_controller('motor')

On the assumption that we have defined a motor of 
the `Newport301Axis` in our configuration file we get a 
reference to the motor object:: 

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


In this simple example we have created an experiment to cycle
the motor stage through 21 positions between 0 and 10 degrees. 
At each step the position and data from all sensors is recorded 
to a file for later analysis as specified in the :doc:`configuration file </tutorial/configuration>`. 





Contents
--------

.. toctree::
   :maxdepth: 3

   introduction/installation
   introduction/ni_engine_architecture
   introduction/configuration
   introduction/available_devices
   introduction/building_documentation
   api/modules


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`



