import config
class HardwareFactory(object):
	hardwareBuilders = dict()
	

	def createHardware(self,config):
		hardwareCode = self.getCode(config)				
		if hardwareCode in HardwareFactory.hardwareBuilders:
			return HardwareFactory.hardwareBuilders[hardwareCode].create(config)		

		else:
			raise Exception("hardware Type: {0} not recognised".format(hardwareCode)) 			

	def getCode(self,configuration):
		return configuration[config.codeString]
	
	@classmethod
	def registerHardware(cls,hardware):
		code = hardware.code
		HardwareFactory.hardwareBuilders[code]= hardware