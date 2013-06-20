
class AbstractSensor(object):

	metaInfo = ""

	def connect(self):
		raise NotImplementedError


	def disconnect(self):
		raise NotImplementedError

	def measure(self):
		raise NotImplementedError


	# abstract method to handle sensor creation based on configuration
	@staticmethod
	def create(config):
		raise NotImplementedError
		