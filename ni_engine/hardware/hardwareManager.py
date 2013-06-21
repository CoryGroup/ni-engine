import config 
import u3
from hardwareFactory import HardwareFactory
class HardwareManager(object):

	def __init__(self,configuration):
				
		self.configuration = configuration
		self.hardware = dict()
		self.hardwareFactory = HardwareFactory()
	
	def addHardware(self,hardwareConfig):
		hardware = self.hardwareFactory.createHardware(hardwareConfig)
		self.hardware[hardware.id] = hardware

	def removeHardware(self,hardware):
		if hardware: 
			del self.hardware[hardware.id]
			hardware.disconnect()

		else: raise ValueError("Must give valid object")
	
	def removeHardwareByName(self,hardwareName):
		if hardwareName: 
			del self.hardware[hardwareName]
			hardware.disconnect()

		else: raise ValueError("Must give valid name")

	def removeAll(self):
		for k,v in self.hardware.iteritems():
			v.disconnect()
		self.hardware = dict()


	def parseFactoryYaml(self,configYaml):
		return configYaml

	def addAllHardware(self):
		for x in self.configuration.hardware:
			self.addHardware(x)

	def getHardware(self,hardwareId):
		if hardwareId in self.hardware:
			return self.hardware[hardwareId]
		else: raise ValueError("{0} is not a valid hardware id".format(hardwareId))


	@classmethod
	def registerHardware(cls,hardware):
		HardwareFactory.registerHardware(hardware)