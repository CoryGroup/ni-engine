import config 
import u3
import hardwareFactory
class HardwareManager(object):

	def __init__(self,configuration):		
		self.niEngine = niEngine		
		self.configuration = configuration
		self.hardware = dict()
		self.factory = hardwareFactory.HardwareFactory(self.parseFactoryYaml(self.configuration))
	
	def addHardware(self,hardwareConfig):
		hardware = self.hardwareFactory.createHardware(hardwareConfig)
		self.hardware[hardware.id] = wardware

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
