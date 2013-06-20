import ei1050Sensor
import config
class SensorFactory(object):
	
	def __init__(self,sensorBuilders,hardwareManager):
		self.sensorBuilders = dict()
		self.sensorBuilders = sensorBuilders

	def createSensor(self,config):
		sensorCode = getCode(config)
		hardware = getHardware(config)		
		if sensorCode in sensorBuilders:
			return sensorBuilders[sensorCode].create(config,hardware)		

		else:
			raise Exception("Sensor Type not recognised") 

		

	def getInterface(self,configuration):
		pass

	def getCode(self,configuration):
		return configuration[config.idString]

	def getHardware(self,configuration):
		return configuration[config.hardwareIdString]

	