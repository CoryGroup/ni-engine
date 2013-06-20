import yaml
import sensorFactory


class SensorManager(object):
	
	def __init__(self,niEngine,configuration):
		self.niEngine = niEngine		
		self.configuration = configuration
		self.sensors = dict()
		self.sensorFactory = sensorFactory(parseFactoryYaml(self.configYaml))
	
	def addSensor(self,sensorConfig):
		sensor = self.sensorFactory.createSensor(sensorConfig)
		self.sensors[sensor.name] = sensor

	def removeSensor(self,sensor):
		if sensor: 
			del self.sensors[sensor.name]
			sensor.disconnect()

		else: raise ValueError("Must give valid object")
	
	def removeSensorByName(self,sensorName):
		if sensorName: 
			del self.sensors[sensorName]
			sensor.disconnect()

		else: raise ValueError("Must give valid name")

	def removeAll():
		for k,v in self.sensors.iteritems():
			v.disconnect()
		self.sensors = dict()


	def parseFactoryYaml(self,configYaml=self.configYaml):
		return self.configYaml