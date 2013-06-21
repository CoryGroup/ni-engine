
class AbstractSensor(object):

	metaInfo = ""

	def __init__(self):
		raise NotImplementedError


	def disconnect(self):
		raise NotImplementedError

	


	# abstract method to handle sensor creation based on configuration
	@staticmethod
	def create(config):
		raise NotImplementedError
		