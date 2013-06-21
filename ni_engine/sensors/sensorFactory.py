import ei1050Sensor
import config
class SensorFactory(object):
	
	sensorBuilders = dict()

	def __init__(self,hardwareManager):
		self.hardwareManager = hardwareManager
		

	def createSensor(self,config):
		sensorCode = getCode(config)
		hardware = getHardware(config)		
		if sensorCode in SensorFactory.sensorBuilders:
			return SensorFactory.sensorBuilders[sensorCode].create(config,hardware)		

		else:
			raise Exception("Sensor Type not recognised") 

	
	

	def getCode(self,configuration):
		return configuration[config.idString]

	def getHardware(self,configuration):
		return configuration[config.hardwareIdString]

	@classmethod
	def registerSensor(cls,sensor):
		code = sensor.code
		cls.sensorBuilders[code]= sensor