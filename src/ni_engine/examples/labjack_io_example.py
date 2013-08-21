"""
For 100 averages: 
    Sweep phase flag over settings of theta
    measure counts
"""

## IMPORTS ####################################################################

# We need to import a few things from Python's standard library, NumPy and a
# other third-party libraries.
import time
import sys
import numpy as np
import quantities as pq
import math
# We also need to import the NI engine itself.
from ni_engine import NiEngine

## EXPERIMENT #################################################################

# We start by loading the engine.
print "Loading NI Engine..."
n = NiEngine(
    # We need to pass two configuration files: one for this experiment in
    # particular, and one for the hardware setup common to all experiments.
    "ni_engine/examples/conf/labjack_io.yml",
    "../conf/available_interfaces.yml"
)

# Next, we give names to the sensors, the controllers, and the data.
# These are configured by "sample_experiment.yml", as pointed to above.
sensors = n.sensor_manager
controllers = n.controller_manager 


# Next, we extract the motor controller for the phase flag and give it a name.
print "Getting Analog In"
analog_ins = map(lambda x: sensors.get_sensor('analogin{}'.format(x)),range(1,5))
print "Getting Digital In"
digital_ints = map(lambda x: sensors.get_sensor('digitalin{}'.format(x)),range(1,5))
print "Getting Dacs"
dacs = map(lambda x: controllers.get_controller('testDAC{}'.format(x)),range(1,9))


# Finally, we begin the experiment.
for idx in xrange(1000000):

    print "Starting cycle #{0}...".format(idx)

    #each cycle shifts the dac voltage according to a sin
    for idx_controller,controller in enumerate(dacs):
        controller.voltage = abs(3.5*math.sin(float(idx)*float(idx_controller)/500.))*pq.V
    sensors.measure_all()
