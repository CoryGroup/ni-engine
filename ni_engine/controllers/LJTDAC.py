import config


class LJTDAC(abstractController):
	code = 'LJTDAC'
	name = 'LJTDAC Extension'
	description = 'A dac extension that can output from -10V-10V'
	defaultVoltage = 0.0
	maxVoltage = 10.0
	def __init__(self,ID,hardware,dacPin,defaultVoltage=0,maxVoltage=10,name=name,description=description):
		self.id = ID 
		self.hardware = hardware
		self.dacPin = dacPin		
		self.defaultVoltage = defaultVoltage
		self.maxVoltage = maxVoltage
		self.name = name
		self.description = description

	def connect(self):
		self.initialiseDefault()




	def initialiseDefault(self):
		
		
	@staticmethod 
	def create(cls,configuration,hardware,sensors):
		ID = configuration[config.idString]
		n = cls.name
		d = cls.description
		if config.nameString in configuration:
			n= configuration[config.nameString]
		if config.descriptionString in configuration:
			d= configuration[config.descriptionString]
		
		dacPin = configuration['pins']['dac']

		maxVoltage = cls.maxVoltage
		if 'maxVoltage' in configuration:
			maxVoltage = configuration['maxVoltage']
		maxVoltage = cls.maxVoltage

		if 'defaultVoltage' in configuration:
			defaultVoltage = configuration['defaultVoltage']

		
		
		return LJTDAC(ID,hardware,dacPin,defaultVoltage=defaultVoltage,maxVoltage = maxVoltage, name=n,description=d) 