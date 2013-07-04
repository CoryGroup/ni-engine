import config

class ControllerFactory(object):
	
	controllerBuilders = dict()

	def __init__(self,hardwareManager,sensorManager):
		self.hardwareManager = hardwareManager
		self.sensorManager = sensorManager

	def createController(self,config):
		
		
		controllerCode = self.getCode(config)		
		hardware = self.getHardware(config)
		sensors = self.getSensors(config)		
		if controllerCode in ControllerFactory.controllerBuilders:
			return ControllerFactory.controllerBuilders[controllerCode].create(config,hardware,sensors)		

		else:
			raise Exception("Controller Type: {0} not recognised".format(controllerCode)) 

	
	

	def getCode(self,configuration):
		return configuration[config.codeString]

	def getHardware(self,configuration):
		hardwareId = configuration[config.hardwareIdString]
		return self.hardwareManager.getHardware(hardwareId)

	def getSensors(self,configuration):
		if config.sensorsForPlatformString in configuration:
			sensorIDs = map(lambda x: x[config.sensorIdString],configuration[config.sensorsForPlatformString])
			return dict(zip(sensorIDs,map(lambda x : self.sensorManager.getSensor(x),sensorIDs)))
		
		return dict()



	@classmethod
	def registerController(cls,controller):
		code = controller.code
		cls.controllerBuilders[code]= controller