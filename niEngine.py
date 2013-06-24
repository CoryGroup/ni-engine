import sys

try:
	sys.path.append("ni_engine/configuration")
	sys.path.append("ni_engine/")	
except Exception:
	print "Couldn't import paths"

import config
import sensors
import hardware
import config
class NiEngine(object):
	def __init__(self,sensorConfig,availableConfig):
		self.configuration = config.Configuration(availableConfig)
		self.configuration.readConfig(sensorConfig)
		self.hardwareManager = hardware.HardwareManager(self.configuration)
		self.hardwareManager.addAllHardware()
		self.sensorManager = sensors.SensorManager(self.configuration,self.hardwareManager)
		self.sensorManager.addAllSensors()


	
		