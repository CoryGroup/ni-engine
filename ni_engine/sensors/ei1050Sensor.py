import abstractSensor, ei1050, Queue


class ei1050Sensor(abstractSensor.AbstractSensor):

	def __init__(self,device,dataPin,clockPin,enablePin,threaded=False,pollingTime=0.5):

		self.device = device, 
		self.dataPin = dataPin
		self.clockPin = clockPin
		self.enablePin = enablePin
		self.threaded = threaded 
		self.pollingTime = pollingTime


	def connect(self):
		if self.threaded:
			self.queue = Queue.LifoQueue()
			self.probe = ei1050.EI1050Reader(device,self.queue,self.enablePin,self.dataPin,self.clockPin)
			self.probe.run()
		else:
			self.probe = ei1050.EI1050(device,self.enablePin,self.dataPin,self.clockPin)

	def measure(self):

		if self.threaded: 
			measurement = self.queue.get(block=True,timeout=None)
		else:
			measurement = self.probe.getReading()

		return measurement


	def disconnect(self):
		if self.threaded:
			self.probe.stop()
			del self.probe
		else: 
			del self.probe


	@staticmethod
	def create(self,config):
		#extract config info


		if threaded:
			if pollingTime:
				return ei1050Sensor(device,dataPin,clockPin,enablePin,threaded=True,pollingTime=pollingTime)
			else: 
				return ei1050Sensor(device,dataPin,clockPin,enablePin,threaded=True)
		else:
			return ei1050Sensor(device,dataPin,clockPin,enablePin)