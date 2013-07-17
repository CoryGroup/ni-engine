import sys

try:
    sys.path.append("ni_engine/configuration")
    sys.path.append("ni_engine/")    
except Exception:
    print "Couldn't import paths"

import config
import sensors
import hardware
import controllers
class NiEngine(object):
    def __init__(self,sensor_config,available_config):
        self.configuration = config.Configuration(available_config)
        self.configuration.readConfig(sensor_config)
        self.hardware_manager = hardware.HardwareManager(self.configuration)
        self.hardware_manager.addAllHardware()
        self.sensor_manager = sensors.SensorManager(self.configuration,self.hardware_manager)
        self.sensor_manager.addAllSensors()
        self.controller_manager =  controllers.ControllerManager(self.configuration,self.hardware_manager,self.sensor_manager)
        self.controller_manager.addAllControllers()

    
        