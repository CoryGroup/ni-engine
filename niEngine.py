import sys

try:
	sys.path.append("ni_engine/configuration")
	sys.path.append("ni_engine/hardware")
	sys.path.append("ni_engine/sensors")
except Exception:
	print "Couldn't import paths"

import config
import sensorManager
import configuration
class NiEngine(object):
	def __init__(self,sensorConfig,availableConfig):
		self.configuration = configuration.Configuration(availableConfig)
		self.configuration.readConfig(sensorConfig)
		self.hardwareManager = hardwareManager.HardwareManager(self,self.configuration)
		self.sensorManager = sensorManager.SensorManager(self,self.configuration,hardwareManager)

