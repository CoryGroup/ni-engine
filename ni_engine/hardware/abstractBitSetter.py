class AbstractBitSetter (object):

	def setPins(self,list):
		raise NotImplementedError

	def setBitDir(self,list):
		raise NotImplementedError
		
	def readAnalogPins(self,list):
		raise NotImplementedError

	def readDigitalPins(self,list):
		raise NotImplementedError
