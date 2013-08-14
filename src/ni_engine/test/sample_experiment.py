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

# We also need to import the NI engine itself.
from ni_engine import NiEngine

## EXPERIMENT #################################################################

# We start by loading the engine.
print "Loading NI Engine..."
n = NiEngine(
    # We need to pass two configuration files: one for this experiment in
    # particular, and one for the hardware setup common to all experiments.
    "ni_engine/test/sample_experiment.yml",
    "../conf/available_interfaces.yml"
)

# Next, we give names to the sensors, the controllers, and the data.
# These are configured by "sample_experiment.yml", as pointed to above.
sensors = n.sensor_manager
controllers = n.controller_manager 
data = n.data_handler

# Next, we extract the motor controller for the phase flag and give it a name.
print "Getting motor..."
motor = controllers.get_controller('phase_flag')

# Finally, we begin the experiment.
for idx_average in xrange(100):

    print "Starting average #{0}...".format(idx_average)

    # Each average within the experiment consists of a loop over theta,
    # letting theta be between 0 and 10 degrees.
    for theta in np.linspace(0, 10, 21) * pq.degree:
        # Move the motor to theta, as given by the loop above.
        print "Moving phase flag to {}...".format(theta)
        motor.move_absolute(theta)
        
        # Sleep for an interval to allow the experiment to rethermalize,
        # and for the motor to move.
        time.sleep(1)
        
        # Now perform all of the measurements specified in the configuration
        # file included above, recording to an HDF5-formatted data file.
        print "Measuring..."
        sensors.measure_all(compound=True)
        
