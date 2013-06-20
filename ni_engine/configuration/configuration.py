import yaml 
import os 
import sys
class Configuration(object):
	availableSensors= None
	availableHardware = None
	hardware = None
	sensors = None
	codeString = 'code'
	hardwareIdString = 'hardwareID'
	sensorsForPlatformString = 'sensors'
	isOnString = 'enabled'
	
	def __init__(self,availableInterfaces,**kwargs):
		
		self.availableInterfaces = availableInterfaces
		if 'configFile' in kwargs:
			self.configFile = kwargs['configFile']
		inter = open(self.availableInterfaces,'r')
		interfaces = yaml.load(inter)

		self.availableSensors = interfaces['sensors']
		self.availableHardware = interfaces['hardware'] 

	def readConfig(self,configFile=None):
		if configFile:
			self.configFile = configFile
		if not self.configFile:
			raise ValueError("ConfigFile must be set")

		file = open(self.configFile,'r')

		self.yamlConfig = yaml.load(file)

		self.sensors = self.yamlConfig['sensors']

		self.hardware = self.yamlConfig['hardware']

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
			if self.codeString in x:
				hard.append(x[self.codeString])
			else:  
				raise ValueError("All sensors and hardware must have sensor code in configuration")
		return hard

	@property 
	def requiredHardware(self): 
		hard =[]
		for x in self.hardware:
			if self.codeString in x:
				hard.append(x[self.codeString])
			else:  
				raise ValueError("All sensors and hardware must have sensor code in configuration")
		return hard
	


	def areValidSensorReferenced(self):		

		for x in self.requiredSensors:
			if x not in self.availableSensors:
				raise ValueError("Not all sensors references are valid")
				return False
			elif not self.availableSensors[x][self.isOnString]:
				raise ValueError("Sensor not enabled")
				return False
		return True

	def isValidHardwareReferenced(self):		

		for x in self.requiredHardware:
			if  x not in self.availableHardware:
				raise ValueError("Not all hardware references are valid")
				return False
			elif not self.availableHardware[x][self.isOnString]:
				raise ValueError("Sensor not enabled")
				return False
		return True


	def areSensortoHardwareValid(self):
		idDict = dict()
		for x in self.hardware:			
			idDict[x['id']] = x
		for y in self.sensors:			
			if y[self.hardwareIdString] not in idDict:
				raise ValueError("Sensor reference id does not have hardware match")
				return False
			elif y[self.codeString] not in self.availableHardware[idDict[y[self.hardwareIdString]][self.codeString]][self.sensorsForPlatformString]:
				raise ValueError("Sensor not available for platform")
				return False
			elif  not self.availableHardware[idDict[y[self.hardwareIdString]][self.codeString]][self.sensorsForPlatformString][y[self.codeString]][self.isOnString]:
				raise ValueError("Sensor not enabled for platform")
				return False

		return True

	def validateConfig(self):
		sensorVal = self.areValidSensorReferenced()
		hardwareVal = self.isValidHardwareReferenced()
		crossRefVal = self.areSensortoHardwareValid()

		if sensorVal and hardwareVal and crossRefVal:
			return True
		
		return False

