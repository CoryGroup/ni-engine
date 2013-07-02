class AbstractSensor(object):

	metaInfo = ""

	def connect(self):
		raise NotImplementedError


	def disconnect(self):
		raise NotImplementedError	


	# abstract method to handle sensor creation based on configuration
	@classmethod
	def create(cls,config):
		raise NotImplementedError