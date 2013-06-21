import yaml
from sensorFactory import SensorFactory


class SensorManager(object):
	
	def __init__(self,niEngine,configuration,hardwareManager):
		self.niEngine = niEngine		
		self.configuration = configuration
		self.sensors = dict()
		self.factory = SensorFactory(self.parseFactoryYaml(self.configuration),hardwareManager)
	
	def addSensor(self,sensorConfig):
		sensor = self.sensorFactory.createSensor(sensorConfig)
		self.sensors[sensor.id] = sensor

	def removeSensor(self,sensor):
		if sensor: 
			del self.sensors[sensor.id]
			sensor.disconnect()

		else: raise ValueError("Must give valid object")
	
	def removeSensorByName(self,sensorName):
		if sensorName: 
			del self.sensors[sensorName]
			sensor.disconnect()

		else: raise ValueError("Must give valid name")

	def removeAll(self):
		for k,v in self.sensors.iteritems():
			v.disconnect()
		self.sensors = dict()


	def parseFactoryYaml(self,configYaml):
		return configYaml

	def addAllSensors(self):
		for x in configuration.sensors:
			self.addSensor(x)

	@classmethod
	def registerSensor(cls,sensor):
		SensorFactory.registerSensor(sensor)