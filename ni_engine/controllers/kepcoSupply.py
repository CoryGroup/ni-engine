import config 
from LJTDAC import LJTDAC
class KepcoSupply(LJTDAC):
	code = 'kepco'
	name = 'Kepco Power Supply'
	description = 'Voltage controlled Kepco Power Supply 0-10V'
	defaultVoltage = 0

	def __init__(self,ID,hardware,voltagePin,crowbarPin,sensors=dict(),defaultTemperature=293.15,defaultVoltage=0,name=name,description=description):
		self.id = ID 
		self.hardware = hardware
		self.voltagePin = voltagePin 
		self.crowbarPin = crowbarPin 
		self.sensors = sensors 
		self.defaultTemperature = defaultTemperature
		self.defaultVoltage = defaultVoltage
		self.name = name
		self.description = description

	def connect(self):
		self.initialiseDefault()





	@staticmethod 
	def create(cls,configuration,hardware,sensors):
		ID = configuration[config.idString]
		n = cls.name
		d = cls.description
		if config.nameString in configuration:
			n= configuration[config.nameString]
		if config.descriptionString in configuration:
			d= configuration[config.descriptionString]
		threaded = configuration["threaded"]
		voltagePin = configuration['pins']['voltage']
		crowbarPin = configuration['pins']['crowbar']
		maxVoltage = configuration['maxVoltage']
		defaultVoltage = cls.defaultVoltage
		if 'defaultVoltage' in configuration:
			defaultVoltage = configuration['defaultVoltage']

		if config.sensorString in configuration:
			sensors = configuration[config.sensorString]
			return KepcoSupply(ID,hardware,voltagePin,crowbarPin,sensors=sensors,defaultVoltage=defaultVoltage,name=n,description=d)

		else:
			temperature = configuration['temperature']
			return KepcoSupply(ID,hardware,voltagePin,crowbarPin,defaultTemperature=temperature,defaultVoltage=defaultVoltage,name=n,description=d)

