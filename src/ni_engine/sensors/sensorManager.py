import yaml
import sensorFactory
class SensorManager:

	
	def __init__(self,niEngine,configYaml=None):
		self.niEngine = niEngine
		self.configYaml = configYaml
		self.sensors = dict()
		self.sensorFactory = sensorFactory(parseFactoryYaml(self.configYaml))

	
	def addSensor(self,sensorConfig):
		sensor = self.sensorFactory.createSensor(sensorConfig)
		self.sensors[sensor.name] = sensor

	def removeSensor(self,sensor=None,sensorName=None):
		if sensor: 
			del self.sensors[sensor.name]
			sensor.disconnect()

		elif sensorName: 
			del self.sensors[sensorName]
			sensor.disconnect()

		else: raise ValueError("Must specify either name or object")
	
	def removeAll():
		for k,v in self.sensors.iteritems():
			v.disconnect()
		self.sensors = dict()


	def parseFactoryYaml(self,configYaml=self.configYaml):
		return self.configYaml