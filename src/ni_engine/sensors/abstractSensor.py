
class AbstractSensor:

	self.metaInfo = ""

	def connect(self):
		raise NotImplementedError


	def disconnect(self):
		raise NotImplementedError

	def measure(self):
		raise NotImplementedError

		