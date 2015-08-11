# Let daq_counter's __all__ take care of things.
try:
    from daq_sensor import *
except ImportError:
    # Declare names from daq_sensor to be None.
    DAQCounterSensor = None

