import ei1050Sensor
import config
class SensorFactory(object):
	
	sensorBuilders = dict()

	def __init__(self,hardwareManager,sensorManager):
		self.hardwareManager = hardwareManager
		self.sensorManager = sensorManager

	def createController(self,config):
		
		for k in ControllerFactory.controllerBuilders:
			print k
		controllerCode = self.getCode(config)
		print controllerCode
		hardware = self.getHardware(config)
		sensors = self.getSensors(config)		
		if controllerCode in ControllerFactory.controllerBuilders:
			return ControllerFactory.controllerBuilders[controllerCode].create(config,hardware,sensors)		

		else:
			raise Exception("Sensor Type not recognised") 

	
	

	def getCode(self,configuration):
		return configuration[config.codeString]

	def getHardware(self,configuration):
		hardwareId = configuration[config.hardwareIdString]
		return self.hardwareManager.getHardware(hardwareId)

	def getSensors(self,configuration):
		sensorIDs = map(lambda x: x[config.sensorIdString],configuration)
		return dict(zip(sensorIDs,map(lambda x : self.sensorManager.getSensor(x),sensorIDs)))


	@classmethod
	def registerSensor(cls,sensor):
		code = sensor.code
		cls.sensorBuilders[code]= sensor