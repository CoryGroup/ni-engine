
Ni-Engine Architecture
======================

Ni-Engine is a highly object oriented library, designed 
to be simple to use and easily extendable. There are three 
main classes of objects. Which, are **hardware**, **sensors**
and **controllers**.


Hardware
^^^^^^^^

Hardware objects are normally where the software interface between 
the physical device and computer are established. Every 
:class:`.AbstractSensor` and 
:class:`.AbstractController` requires 
a valid :class:`.AbstractHardware` that supports 
the specified sensor or controller to function. Hardware objects are managed 
by an instance of :class:`.HardwareManager`. Normally, during 
program operation it is not necessary to access the hardware objects as the sensors
and controllers should handle all necessary interactions with these objects. 
If it proves necessary hardware objects can be accessed through 
:meth:`.HardwareManager.get_hardware`.

Sensors
^^^^^^^

Sensors all inherit from :class:`.AbstractSensor`. Sensors
are to be implemented by devices who's only purpose is to measure the enviroment
and not to take any action. The primary action implemented by sensors is 
:meth:`.AbstractSensor.measure` this should return the 
measurement inside a :class:`.DataContainer`. All sensors 
are created by a :class:`.SensorManager` and should whenever
possible have the measure method called by the manager as this allows for easy 
storage of data. To obtain a sensor from the sensor manager use 
:meth:`.SensorManager.get_sensor`.

Controllers
^^^^^^^^^^^

Controllers all inherit from :class:`.AbstractController`. Controllers
are to be implemented by devices who's purpose to take action. Controllers may implement
many different different actions and it is normally useful to obtain the actual 
controller object to call its methods. This can be obtained from the 
:class:`.ControllerManager` by calling 
:meth:`.ControllerManager.get_controller`. All controllers
implement the method :meth:`.AbstractController.get_status` , 
which should respond with a :class:`.DataContainer` containing 
vital information, such as position, velocity and other parameters of the specific
controller.



Ni-Engine Program Flow
^^^^^^^^^^^^^^^^^^^^^^
On initialization of an instance of :class:`.NiEngine` an instance of 
:class:`.Configuration` is created to read in and handle verification
of configuration files. An instance of :class:`.DataHandler` is created
in order to manage storage of data, both in memory and on disk. The 
:class:`.DataHandler` is passed its relevant configuration and if necessary
sets up the specified instance of :class:`.AbstractPhysicalStorage`.
This is used to store data on disk. The :class:`.NiEngine` instance than creates instances
of :class:`.HardwareManager`, :class:`.ControllerManager`
and :class:`.ControllerManager` which are passed their relevant configuration
information. Based on these configuration the managers create specified instances of their respective
:class:`.AbstractHardware`, :class:`.AbstractSensor` and 
:class:`.AbstractController` objects. Initialization is now complete, and user
specified instructions may now be executed. 

Data in Ni-Engine
^^^^^^^^^^^^^^^^^
Whenever possible commands with numerical parameters in Ni-Engine should be passed as a :class:`quantities.Quantity`.
This allows the use of units and allows a much more explicit way of specifying arguments that will reduce 
user errors, when different units come into play. This also allows the passing of equivalent units that can 
than be converted by the actual instances of the classes to the required units. 

Ni-Engine attempts to pass data around in the form of :class:`.Data` instances. These may be
created using the factory method :func:`.data_value.data`. Data objects may be used just like 
their `value` attribute. Just like so:: 

    >>> data('newport','NEWPORTAXIS','position',1.0*pq.m) == pq.Quantity(1.0,pq.m)
    True

The reason, that :class:`.Data` instances are preferred, is that by only using these instances
it makes programming of storage engines much easier. As such :class:`.DataHandler` will only 
accept instances of :class:`.DataContainer` which can contain multiple instances of 
:class:`.Data` each. 