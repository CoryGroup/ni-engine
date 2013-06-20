import AbstractSensor, ei1050, Queue.LifoQueue


class ei1050Sensor(AbstractSensor):

	def __init__(self,device,dataPin,clockPin,enablePin,threaded=False,pollingTime=0.5):

		self.device = device, 
		self.dataPin = dataPin
		self.clockPin = clockPin
		self.enablePin = enablePin
		self.threaded = threaded 
		self.pollingTime = pollingTime


	def connect(self):
		if self.threaded:
			self.queue = LifoQueue()
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
