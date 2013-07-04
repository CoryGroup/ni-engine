from controllerFactory import ControllerFactory

class ControllerManager(object):
	
	def __init__(self,configuration,hardwareManager,sensorManager):
				
		self.configuration = configuration
		self.controllers= dict()
		self.controllerFactory = ControllerFactory(hardwareManager,sensorManager)
		
	def addController(self,controllerConfig):
		controller = self.controllerFactory.createController(controllerConfig)
		self.controllers[controller.id] = controller
		controller.connect()

	def removeSensor(self,controller):
		if controller: 
			del self.controllers[controller.id]
			controller.disconnect()

		else: raise ValueError("Must give valid object")
	
	def removeSensorByName(self,controllerName):
		if controllerName: 
			controller = self.controllers[controllerName]
			del self.controllers[controllerName]
			controller.disconnect()

		else: raise ValueError("Must give valid name")

	def removeAll(self):
		for k,v in self.controllers.iteritems():
			v.disconnect()
		self.controllers = dict()


	def parseFactoryYaml(self,configYaml):
		return configYaml

	def addAllControllers(self):
		for x in self.configuration.controllers:
			self.addController(x)

	def getControllerById(self,ID):
		if ID in self.controllers:
			return self.controllers[ID]
		else: raise ValueError("No Controllerexists for id: {0}".format(ID))	

	@classmethod
	def registerController(cls,controller):
		ControllerFactory.registerController(controller)