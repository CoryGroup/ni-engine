import abstractSensor, ei1050, Queue
import config
from measurement import Measurement
class Ei1050Sensor(abstractSensor.AbstractSensor):
	code = "EI1050"
	name = "EI1050Sensor"
	description = " "

	def __init__(self,ID,device,dataPin,clockPin,enablePin,threaded=False,pollingTime=0.5,name=name,description=description,retryLim=20):

		self.device = device
		self.dataPin = dataPin
		self.clockPin = clockPin
		self.enablePin = enablePin
		self.threaded = threaded 
		self.pollingTime = pollingTime
		self.id = ID
		self.name = name
		self.description = description
		self.retryLim = retryLim


	def connect(self):
		if self.threaded:
			self.queue = Queue.LifoQueue()
			self.probe = ei1050.EI1050Reader(self.device,self.queue,enablePinNum=self.enablePin,dataPinNum=self.dataPin,clockPinNum=self.clockPin)
			
			self.probe.start()
			
		else:
			self.probe = ei1050.EI1050(self.device,enablePinNum=self.enablePin,dataPinNum=self.dataPin,clockPinNum=self.clockPin)

	def measure(self):
		try:
			if self.threaded: 
							
				reading= self.queue.get(block=True,timeout=None)
				if self.queue.qsize() >=100:
					self.queue.clear()
				self.queue.put(reading)

			else:
				reading = self.probe.getReading()

			temperature = Measurement(self.id,Ei1050Sensor.code,"Temperature",reading.getTemperature(),time=reading.getTime(),)
			humidity = Measurement(self.id,Ei1050Sensor.code,"Humidity",reading.getHumidity(),time=reading.getTime(),)
			measurementDict = dict()
			measurementDict['temperature'] = temperature
			measurementDict['humidity'] = humidity
			self.retries =0
			return measurementDict
		except Exception as e:
			self.retries += 1
			print "Measurement not successful retrying"
			print e
			if self.retries < self.retryLim:
				return self.measure()
			else: raise Exception("Measurement could not be completed: Retry limit exceeded")

	def disconnect(self):
		if self.threaded:
			self.probe.stop()
			del self.probe
		else: 
			del self.probe


	@classmethod
	def create(cls,configuration,device):
		#extract config info
		
		ID = configuration[config.idString]
		n = Ei1050Sensor.name
		d = Ei1050Sensor.description
		if config.nameString in configuration:
			n= configuration[config.nameString]
		if config.descriptionString in configuration:
			n= configuration[config.descriptionString]
		threaded = configuration["threaded"]
		dataPin = configuration["pins"]["data"]
		clockPin = configuration["pins"]["clock"]
		enablePin = configuration["pins"]["enable"]
		dataPin = configuration["pins"]["data"]

		if "pollingTime" in configuration:
			pollingTime = configuration["pollingTime"]
		else: 
			pollingTime = None
		if threaded:
			if pollingTime:				
				return Ei1050Sensor(ID,device,dataPin,clockPin,enablePin,threaded=True,pollingTime=pollingTime,name = n,description = d)
			else: 
				return Ei1050Sensor(ID,device,dataPin,clockPin,enablePin,threaded=True,name = n,description = d)
		else:
			return Ei1050Sensor(ID,device,dataPin,clockPin,enablePin)