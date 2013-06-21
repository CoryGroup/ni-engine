import config
class HardwareFactory(object):
	hardwareBuilders = dict()
	def __init__(self,hardwareBuilders):
		
		self.hardwareBuilders = hardwareBuilders

	def createhardware(self,config):
		hardwareCode = getCode(config)				
		if hardwareCode in hardwareBuilders:
			return hardwareBuilders[hardwareCode].create(config)		

		else:
			raise Exception("hardware Type not recognised") 

			

	def getCode(self,configuration):
		return configuration[config.idString]

	
	@classmethod
	def registerHardware(hardware):
		code = hardware.code
		HardwareFactory.sensorBuilders[code]= sensor