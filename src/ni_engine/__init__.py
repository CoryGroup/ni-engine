#!/usr/bin/python
# -*- coding: utf-8 -*-
##
# __init__.py: Main package module for the entire NI Engine project.
##
# Part of the NI Engine project.
##
"""

"""

## LOGGING CONFIGURATION ######################################################

# We occasionally use logging here, so let's make sure there's a NullHandler
# to catch messages even if the application doesn't.
# We also need to make sure logging is in place *before* importing everything
# else, so that import errors are logged properly.
import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())

## IMPORTS ####################################################################

# Make the following subpackages available w/o explicitly importing.
from . import config
from . import sensors
from . import hardware
from . import controllers
from . import tools

# Pull in the things we need right here.
from .config import Configuration
from .sensors import SensorManager
from .hardware import HardwareManager
from .controllers import ControllerManager
from .storage import DataHandler

## CLASSES ####################################################################

class NiEngine(object):
    """
    Class representing a neutron interferometry experiment, including
    sensors, controllers and storage devices.
    
    Parameters
    ----------
    sensor_config : str
        Path to a YAML-formatted configuration file listing the sensors that
        are to be read from in this experiment.
        
    available_config : str
        Path to a YAML-formatted configuration file listing which equipment is
        available for use in this experiment.
    """
    def __init__(self, sensor_config, available_config):
        self.configuration = Configuration(available_config)
        self.configuration.read_config(sensor_config)
        
        self.data_handler = DataHandler(self.configuration)
        
        self.hardware_manager = HardwareManager(
            self.configuration, self.data_handler
        )
        self.hardware_manager.add_all_hardware()
        
        self.sensor_manager = SensorManager(
            self.configuration, self.data_handler, self.hardware_manager
        )
        self.sensor_manager.add_all_sensors()
        
        self.controller_manager =  ControllerManager(
            self.configuration, self.data_handler, self.hardware_manager,
            self.sensor_manager
        )
        self.controller_manager.add_all_controllers()

    
        
