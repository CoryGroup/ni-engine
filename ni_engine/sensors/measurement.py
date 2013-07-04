from datetime import datetime

class Measurement(object):

	def __init__(self,sensorId,sensorCode,measurementName,value,time=datetime.now()):
		self.sensorId = sensorId
		self.sensorCode = sensorCode
		self.measurementName = measurementName
		self.value = value 
		self.time = time

	def __lt__(self,other):
		return self.time < other.time