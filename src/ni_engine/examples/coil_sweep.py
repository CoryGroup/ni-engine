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
    r"C:\Users\corylab\Documents\GitHub\ni-engine\src\ni_engine\examples\example_configurations\coil_sweep.yml",
    r"C:\Users\corylab\Documents\GitHub\ni-engine\src\ni_engine\config\available_config.yml",
)
  

# Next, we give names to the sensors, the controllers, and the data.
# These are configured by "sample_experiment.yml", as pointed to above.
sensors = n.sensor_manager
controllers = n.controller_manager 


# Next, we extract the controllers for the two DAC channels.
dac0 = n.controller_manager.get_controller('testDAC0')
dac1 = n.controller_manager.get_controller('testDAC1')

for V in np.linspace(pq.Quantity(0, 'V'), pq.Quantity(3, 'V'), 10):
    dac0.voltage = V
    dac1.voltage = V
    sensors.measure_all()
