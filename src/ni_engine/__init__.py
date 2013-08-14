
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
    def __init__(self, sensor_config, available_config):
        self.configuration = Configuration(available_config)
        self.configuration.read_config(sensor_config)
        self.data_handler = DataHandler(self.configuration)
        self.hardware_manager = HardwareManager(self.configuration,self.data_handler)
        self.hardware_manager.add_all_hardware()
        self.sensor_manager = SensorManager(self.configuration,self.data_handler,self.hardware_manager)
        self.sensor_manager.add_all_sensors()
        self.controller_manager =  ControllerManager(self.configuration,self.data_handler,self.hardware_manager,self.sensor_manager)
        self.controller_manager.add_all_controllers()

    
        
