
Configuration 
============= 

Ni-Engine has been designed to run off configuration files
passed to it upon initilization. These configuration files 
must be in the `yaml <http://www.yaml.org/>`_ format. Configuration
files are used so that all creation and initialization can be done 
automatically by Ni-Engine based upon specified hardware,sensors and
controllers in the configuration file. This allows for many different
experiments to be run with identical hardware setups and removes much 
of necessary boilerplate code. 

The Configuration class
^^^^^^^^^^^^^^^^^^^^^^^
Handling of configuration files is done by :class:`ni_engine.config.Configuration`.
This class is passed the path of two files. One of which, the experimental setup 
configuration is necessary for the user to specify and the other which contains 
information on what sensors,hardware and controllers are enabled/disabled for 
what devices is optional. The average user shouldn't have to use 
:class:`ni_engine.config.Configuration` as it should be handled automatically. 
However, it is useful to understand how the internals work. 

Building your own configuration file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
All configuration files are formatted in `yaml <http://www.yaml.org/>`_. This 
makes configuration easy to understand and human readable. Every configuration
file has four key sections; **hardware, sensors, controllers** and **configuration**. 
The hardware, sensors and controllers sections correspond to objects to be created from 
:mod:`ni_engine.hardware`, :mod:`ni_engine.sensors` and :mod:`ni_engine.controllers` 
respectively, while the configuration section corresponds to general configuration, 
including data storage configuration. 

Every piece of hardware,sensor or controller is defined in the configuration file. 
They each share several default paramaters:

.. code-block:: yaml

   # a name of the item
   name: Newport motor
   # a description of the item
   description: A cool description
   # A code to reference the actual 
   # python code object by. 
   # Each hardware,sensor or controller
   # has a unique code that Ni-Engine will
   # recognise and figure out which object
   # to build. For example here we tell it 
   # to build a NewportAxis to control an 
   # axis on a Newport device. 
   code: NEWPORTAXIS
   #The id is also very important. We refer
   # to the objects we build via their id's 
   #from their respective managers. Also
   # When sensors and controllers need to be
   #tied to hardware objects, we tie them in 
   # based off ids. 
   id: motor

Additionally **sensors**, and **controllers**
have another required parameter which is:

.. code-block:: yml

   #the hardware_id parameter specifies which
   #piece of hardware in the configuration the 
   #sensor or controller requires
   hardware_id: newport


Thus we can now show how to build a configuration file to do a simple experiment using
two pieces of hardware; a labjack (:class:`ni_engine.hardware.labjack.U3LV`) and newport 
(:class:`ni_engine.hardware.newport.Newport301`). We will also use a temperature sensor (
:class:`ni_engine.sensors.labjack.LabJackInternalSensor`), 
connected to the labjack and a controller (:class:`ni_engine.controllers.newport.Newport301Axis`),
connected to the newport:
    
.. code-block:: yaml

   #the hardware section
   hardware:
   # define the labjack
    - name: Labjack U3-LV
      description: Test labjack
      code: U3LV
      id: labjack
   # define the newport   
    - name: Newport ESP-301
      description: Newport motor controller
      code: NEW301
       id: newport
       # additional configuration information required to connect
       uri: "serial://COM10?baud=19200"

   #the sensors section
   sensors: 
    #define the temperature sensor
    - name: Labjack Internal Sensor
      description: Temperature inside labjack
      code: LABINT
      id: internal 
    # tell the sensor that it is tied to the labjack
      hardware_id: labjack
   #the controllers section 
   controllers:
    - name: Newport Stepper axis
      description: Commutated stepper in degrees
        code: NEWPORTAXIS
        #Tell the controller that it is connected
        # to the newport
        hardware_id: newport  
        id: motor
        default_position: 0
        axis_id: 0
        configuration_parameters:
         motor_type: 2
         current: 0.9
         voltage: 10
         units: 7
         feedback_configuration: 0
         position_display_resolution: 4
         full_step_resolution: 0.9
         microstep_factor: 5
         home: 0
         max_velocity: 2
         acceleration_feed_forward: 1
          max_acceleration: 2
         hardware_limit_configuration: 24
         reduce_motor_torque_time: 1000
         reduce_motor_torque_percentage: 20
          max_base_velocity: 2.0
         acceleration: 1.0
         deceleration: 1.0
         estop_deceleration: 1.0
         jog_high_velocity: 1.0
         jog_low_velocity: 1.0
         jerk: 1.0
         homing_velocity: 1.0
         velocity: 1.0

This is some example configuration of physical hardware. Ni_Engine
will take this file and figure out what needs to be created and assigned
to what automatically. The actual objects can later be accessed through the
managers. You may notice that there is a bunch of information that is specified
that had not been mentioned before. This is extra information that is required 
for individual objects to function. You can find out what information is required 
for object creation on their individual documentation pages. 

While the configuration above is adequate to define the physical hardware, there are still 
some additional configuration parameters required for the system as a whole to function. 
These are defined in the **configuration** section and look like this:

.. code-block:: yaml

   configuration: 
    #whether to write the data gathered in the 
    #experiment to hard storage 
    store_data: True
    #configure the physical storage if necessary
    storage:
     # code for the storage engine
     code: "HDF5"
     #name of the storage engine
     name: "Test Data Storage"
     #generic file path for name of files
     # to store data to. 
     file_path: "sample_experiment.h5"
     # how many piece of data to buffer 
     #before writing to physical storage
     # Affects performance
     buffer_size : 100
     #Whether we should create a new file
     with a higher index to write data to 
     (True) or overwrite the old file and
     store data there. 
     new_file : True 
     # If you want to load old values for intialization etc.
     load_previous_entries: 
      # number of old entries to store 
      # -1 or non-existent for max      
      number_entries: 50
      #keep old entries around after initialization
      #false by default
      store: Flase

Now our final configuration file for this experiment will look like:
    
.. code-block:: yaml

    #the hardware section
   hardware:
   # define the labjack
    - name: Labjack U3-LV
      description: Test labjack
      code: U3LV
      id: labjack
   # define the newport 
    - name: Newport ESP-301
      description: Newport motor controller
      code: NEW301
      id: newport
      # additional configuration information required to connect
      uri: "serial://COM10?baud=19200"
   #the sensors section
   sensors: 
    #define the temperature sensor
    - name: Labjack Internal Sensor
      description: Temperature inside labjack
      code: LABINT
      id: internal 
    # tell the sensor that it is tied to the labjack
      hardware_id: labjack
   #the controllers section 
   controllers:
    - name: Newport Stepper axis
      description: Commutated stepper in degrees
      code: NEWPORTAXIS
      #Tell the controller that it is connected
      # to the newport
      hardware_id: newport  
      id: motor
      default_position: 0
      axis_id: 0
      configuration_parameters:
       motor_type: 2
       current: 0.9
       voltage: 10
       units: 7
       feedback_configuration: 0
       position_display_resolution: 4
       full_step_resolution: 0.9
       microstep_factor: 5
       home: 0
       max_velocity: 2
       acceleration_feed_forward: 1
        max_acceleration: 2
       hardware_limit_configuration: 24
       reduce_motor_torque_time: 1000
       reduce_motor_torque_percentage: 20
        max_base_velocity: 2.0
       acceleration: 1.0
       deceleration: 1.0
       estop_deceleration: 1.0
       jog_high_velocity: 1.0
       jog_low_velocity: 1.0
       jerk: 1.0
       homing_velocity: 1.0
       velocity: 1.0
   configuration: 
    #whether to write the data gathered in the 
    #experiment to hard storage 
    store_data: True
    #configure the physical storage if necessary
    storage:
     # code for the storage engine
     code: "HDF5"
     #name of the storage engine
     name: "Test Data Storage"
     #generic file path for name of files
     # to store data to. 
     file_path: "sample_experiment.h5"
     # how many piece of data to buffer 
     #before writing to physical storage
     # Affects performance
     buffer_size : 100
     #Whether we should create a new file
     with a higher index to write data to 
     (True) or overwrite the old file and
     store data there. 
     new_file : True 
     # If you want to load old values for intialization etc.
     load_previous_entries: 
      # number of old entries to store 
      # -1 or non-existent for max      
      number_entries: 50
      #keep old entries around after initialization
      #false by default
      store: False

Using the configuration file 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If the path to the file looks like /path/to/file we can 
use this configuration with Ni-Engine like so:
    
    >>> from ni_engine import NiEngine
    
    >>> n = NiEngine('/path/to/file')
    
    Grab the internal sensor
    
    >>> internal = n.sensor_manager.get_sensor('internal')
    
    Grab the motor controller
    
    >>> motor = n.controller_manager.get_controller('motor')
    
    We could than get the temperature via 
    
    >>> n.sensor_manager.measure(internal)
    
    Which will return the temperature data inside a 
    :class:`ni_engine.storage.DataContainer` and also
    store the data to the specified file. We could also 
    for example move the motor to an absolute position
    of 10 degrees and then store its position. 

    >>> import quantities as pq 

    >>> motor.move_absolute(pq.Quantity(10.,pq.deg))

    >>> n.controller_manager.get_status(motor)

Specifying available hardware,sensors and controllers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Another optional configuration file that may be given
specifies what hardware,sensor and controller objects 
are enabled for a system and to what hardware sensors 
and controllers can be used with. This configuration 
file by default is in the config directory of ni_engine
and will be used unless a custom version is supplied. 
By default all hardware,sensors and controllers are 
enabled, with the hardware having support for all 
sensors and controllers possible enabled. The default
file looks like: 

.. code-block:: yaml

   hardware:
    U3LV:
     enabled: True
     sensors:
      EI1050:
       enabled: True
      LABINT:
       enabled: True
     controllers:
      KEPCO:
       enabled: True
      LJTDAC:
       enabled: True
    NEW301:
     enabled: True
     controllers:
      NEWPORTAXIS:
       enabled: True   

    TEST: 
     enabled: True
     sensors:
      GAUSSSENSOR:
       enabled: True   

   sensors: 
    EI1050:
     enabled: True
    LABINT:
     enabled: True
    GAUSSSENSOR:
     enabled: True   

   controllers: 
    KEPCO:
     enabled: True
    LJTDAC: 
     enabled: True
    NEWPORTAXIS:
     enabled: True

If you do not want a certain device to 
be enabled, simply set it to ``False``,
whether this be to disable the device for
everything or simply a certain piece of 
hardware. 

The only difference in setup is now when 
creating the Ni-Engine instance we supply 
an extra parameter::

>>> n = NiEngine('/path/to/file','/path/to/available_devices')