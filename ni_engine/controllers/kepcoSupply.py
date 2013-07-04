import config 
from ljtdac import LJTDAC
from abstractController import AbstractController
class KepcoSupply(AbstractController):
	code = 'KEPCO'
	name = 'Kepco Power Supply'
	description = 'Voltage controlled Kepco Power Supply 0-10V'
	defaultVoltage = 0

	def __init__(self,ID,hardware,voltagePin,crowbarPin,maxVoltage,defaultVoltage=0,defaultCrowbar=None, name=name,description=description):
		self.defaultCrowbar = defaultCrowbar
		if defaultCrowbar is None:
			self.defaultCrowbar = maxVoltage

		self.id = ID 
		self.hardware = hardware
		self.voltagePin = voltagePin 
		self.crowbarPin = crowbarPin 			
		self.defaultVoltage = defaultVoltage
		self.maxVoltage = maxVoltage		
		self.name = name
		self.description = description
		self.voltageOut = self.defaultVoltage
		
		if abs(voltagePin-crowbarPin) != 1 : raise ValueError("Pins must be on same LJTDAC")

		self.dacPin = min(self.crowbarPin,self.voltagePin)

		if min(self.voltagePin,self.crowbarPin) == self.voltagePin :
			self.voltageA = self.dacVoltage(self.defaultVoltage)
			self.voltageB = self.dacVoltage(self.defaultCrowbar)
		else:
			self.voltageA = self.dacVoltage(self.defaultCrowbar)
			self.voltageB = self.dacVoltage(self.defaultVoltage)		

	def connect(self):
		self.initializeDefaults()

	def initializeDefaults(self):
		self.ljtdac = LJTDAC('kepco supply dac',self.hardware,min(self.voltagePin,self.crowbarPin),defaultVoltage=0,maxVoltage=10,name="LJTDAC Kepco",description="Controller managed by Kepco Supply to control it")
		self.setVoltage()
	
	def setVoltage(self,voltage=None,crowbar=None):
		if voltage is not None:
			if min(self.voltagePin,self.crowbarPin) == self.voltagePin :
				self.voltageA = self.dacVoltage(voltage)
			else:
				self.voltageB = self.dacVoltage(voltage)

		if crowbar is not None:
			if min(self.voltagePin,self.crowbarPin) == self.voltagePin :
				self.voltageB = self.dacVoltage(crowbar)
			else:
				self.voltageA = self.dacVoltage(crowbar)
		
		self.ljtdac.setVoltage(voltageA=self.voltageA,voltageB=self.voltageB)

	def dacVoltage(self,voltage):
		return 10.0*voltage/self.maxVoltage

	@classmethod 
	def create(cls,configuration,hardware,sensors):
		ID = configuration[config.idString]
		n = cls.name
		d = cls.description
		if config.nameString in configuration:
			n= configuration[config.nameString]
		if config.descriptionString in configuration:
			d= configuration[config.descriptionString]
		
		voltagePin = configuration['pins']['voltage']
		crowbarPin = configuration['pins']['crowbar']
		maxVoltage = configuration['maxVoltage']
		crowbarVoltage = maxVoltage
		if 'crowbarVoltage' in configuration:
			crowbarVoltage = configuration['crowbarVoltage']

		defaultVoltage = cls.defaultVoltage
		if 'defaultVoltage' in configuration:
			defaultVoltage = configuration['defaultVoltage']
				
		return KepcoSupply(ID,hardware,voltagePin,crowbarPin,maxVoltage,crowbarVoltage,defaultVoltage,name=n,description=d)

