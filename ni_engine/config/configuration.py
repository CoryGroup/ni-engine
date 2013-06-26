import yaml 
import os 
import sys
import configVariables as config
class Configuration(object):
	

	
	def __init__(self,availableInterfaces,**kwargs):
		
		self.availableInterfaces = availableInterfaces
		if 'configFile' in kwargs:
			self.configFile = kwargs['configFile']
		inter = open(self.availableInterfaces,'r')
		interfaces = yaml.load(inter)		
		self.availableSensors = interfaces[config.sensorString]
		self.availableHardware = interfaces[config.hardwareString] 
		self.availableControllers = interfaces[config.controllersString]

	def readConfig(self,configFile=None):
		if configFile:
			self.configFile = configFile
		if not self.configFile:
			raise ValueError("ConfigFile must be set")

		file = open(self.configFile,'r')

		self.yamlConfig = yaml.load(file)

		self.sensors = self.yamlConfig[config.sensorString]

		self.hardware = self.yamlConfig[config.hardwareString]

		self.controllers = self.yamlConfig[config.controllersString]

		self.configuration = self.yamlConfig[config.configurationString]

		if self.validateConfig():
			return True
		else:
			raise ValueError("Configuration files submitted are not valid. Cannot continue. Exiting...")
			sys.exit(1)

	@property
	def getSensors(self):
		return self.sensors

	@property 
	def getHardware(self):
		return self.hardware

	@property 
	def requiredSensors(self): 
		hard =[]
		for x in self.sensors:
			if config.codeString in x:
				hard.append(x[config.codeString])
			else:  
				raise ValueError("All sensors must have sensor code in configuration")
		return hard

	@property 
	def requiredHardware(self): 
		hard =[]
		for x in self.hardware:
			if config.codeString in x:
				hard.append(x[config.codeString])
			else:  
				raise ValueError("All hardware must have sensor code in configuration")
		return hard

	@property
	def requiredControllers(self): 
		hard =[]
		for x in self.controllers:
			if config.codeString in x:
				hard.append(x[config.codeString])
			else:  
				raise ValueError("All controllers must have sensor code in configuration")
		return hard
	


	def areValidSensorReferenced(self,requiredSensors):		

		for x in requiredSensors:
			if x not in self.availableSensors:
				raise ValueError("Not all sensor references are valid")
				return False
			elif not self.availableSensors[x][config.isOnString]:
				raise ValueError("Sensor not enabled")
				return False
		return True

	def areValidControllersReferenced(self,requiredControllers):		

		for x in requiredControllers:
			if x not in self.availableControllers:
				raise ValueError("Not all controller references are valid")
				return False
			elif not self.availableControllers[x][config.isOnString]:
				raise ValueError("Controller not enabled")
				return False
		return True

	def isValidHardwareReferenced(self,requiredHardware):		

		for x in requiredHardware:
			if  x not in self.availableHardware:
				raise ValueError("Not all hardware references are valid")
				return False
			elif not self.availableHardware[x][config.isOnString]:
				raise ValueError("Hardware not enabled")
				return False
		return True

	# Takes a configuration to reference hardware by token: hardwareID
	def areSensorReferencetoHardwareValid(self,referenceConfig):
		idDict = dict()
		for x in self.hardware:			
			idDict[x[config.idString]] = x
		for y in referenceConfig:			
			if y[config.hardwareIdString] not in idDict:
				raise ValueError("Sensor: {0} reference id does not have hardware match".format(y[config.hardwareIdString] ))
				return False
			elif y[config.codeString] not in self.availableHardware[idDict[y[config.hardwareIdString]][config.codeString]][config.sensorsForPlatformString]:
				raise ValueError("Sensor: {0} not available for platform".format(y[config.hardwareIdString] ))
				return False
			elif  not self.availableHardware[idDict[y[config.hardwareIdString]][config.codeString]][config.sensorsForPlatformString][y[config.codeString]][config.isOnString]:
				raise ValueError("Sensor: {0} not enabled for platform".format(y[config.hardwareIdString] ))
				return False

		return True

	def areControllerReferencetoHardwareValid(self,referenceConfig):
		idDict = dict()
		for x in self.hardware:			
			idDict[x[config.idString]] = x
		for y in referenceConfig:			
			if y[config.hardwareIdString] not in idDict:
				raise ValueError("Controller: {0} reference id does not have hardware match".format(y[config.hardwareIdString] ))
				return False
			elif y[config.codeString] not in self.availableHardware[idDict[y[config.hardwareIdString]][config.codeString]][config.controllersForPlatformString]:
				raise ValueError("Controller: {0} not available for platform".format(y[config.hardwareIdString] ))
				return False
			elif  not self.availableHardware[idDict[y[config.hardwareIdString]][config.codeString]][config.controllersForPlatformString][y[config.codeString]][config.isOnString]:
				raise ValueError("Controller: {0} not enabled for platform".format(y[config.hardwareIdString] ))
				return False

		return True

	def areReferencetoSensorValid(self,referenceConfig):
		idDict = dict()
		for x in self.sensors:			
			idDict[x[config.idString]] = x

		for x in referenceConfig:
			for y in x[config.sensorsForPlatformString]:		
				if y[config.sensorIdString] not in idDict:
					raise ValueError("Sensor reference id does not have hardware match")
					return False
			

		return True

	def validateConfig(self):
		sensorVal = self.areValidSensorReferenced(self.requiredSensors)
		hardwareVal = self.isValidHardwareReferenced(self.requiredHardware)
		controllerVal = self.areValidControllersReferenced(self.requiredControllers)
		crossRefSensorHardwareVal = self.areSensorReferencetoHardwareValid(self.sensors)
		crossRefControllerHardwareVal = self.areControllerReferencetoHardwareValid(self.controllers)
		refToSensors = self.areReferencetoSensorValid(self.controllers)
		
		if sensorVal and hardwareVal and controllerVal and crossRefSensorHardwareVal and \
		crossRefControllerHardwareVal and refToSensors:
			return True
		
		return False


	@property
	def storeMeasurements(self):
		if config.storeMeasurementString in self.configuration:
			return self.configuration[config.storeMeasurementString]
		else: 
			return False

	

