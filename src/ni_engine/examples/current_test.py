"""
Test the current testing 
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
    "ni_engine/examples/example_configurations/test_labjack_current.yml"
)
  

# Next, we give names to the sensors, the controllers, and the data.
# These are configured by "sample_experiment.yml", as pointed to above.
sensors = n.sensor_manager
controllers = n.controller_manager 


# Next, we extract the motor controller for the phase flag and give it a name.
print "Getting Current Sensors"
analog_ins = map(lambda x: sensors.get_sensor('currentin{}'.format(x)),range(0,2))

# Finally, we begin the experiment.
for idx in xrange(1000000):

    print "Starting cycle #{0}...".format(idx)

    for x in analog_ins:
        print x.current

    sensors.measure_all()
