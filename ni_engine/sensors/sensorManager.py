from sensorFactory import SensorFactory


class SensorManager(object):
	
	def __init__(self,configuration,hardwareManager):				
		self.configuration = configuration
		self.sensors = dict()
		self.sensorFactory = SensorFactory(hardwareManager)
		self.measurements = dict()
		self.storeMeasurements = self.configuration.storeMeasurements
		
	def addSensor(self,sensorConfig):
		sensor = self.sensorFactory.createSensor(sensorConfig)
		self.sensors[sensor.id] = sensor
		sensor.connect()

	def removeSensor(self,sensor):
		if sensor: 
			del self.sensors[sensor.id]
			sensor.disconnect()

		else: raise ValueError("Must give valid object")
	
	def removeSensorByName(self,sensorName):
		if sensorName: 
			sensor = self.sensors[sensorName]
			del self.sensors[sensorName]
			sensor.disconnect()

		else: raise ValueError("Must give valid name")

	def removeAll(self):
		for k,v in self.sensors.iteritems():
			v.disconnect()
		self.sensors = dict()

	def parseFactoryYaml(self,configYaml):
		return configYaml

	def addAllSensors(self):
		for x in self.configuration.sensors:
			self.addSensor(x)

	def getSensorById(self,ID):
		if ID in self.sensors:
			return self.sensors[ID]
		else: raise ValueError("No Sensor exists for id: {0}".format(ID))

	def getData(self,sensor):
		if sensor.id in self.measurements:
			return self.measurements[sensor.id]
		else: raise Exception("Sensor has no measurements available")
	def getAllData(self):
		return self.measurements

	def getAllCurrentData(self):
		curr = dict()
		for k in self.measurements:
			sen = self.getSensorById(k)
			curr[k] = self.getMostRecentData(sen)

	def getMostRecentData(self,sensor):
		if sensor.id in self.measurements:
			data =  self.measurements[sensor.id]
			recentData = dict()
			for k,v in data.items():
				recentData[k]= v[-1]
			return recentData
		else: raise Exception("Sensor has no measurements available")

	def measure(self,sensor):
		if sensor.id not in self.measurements:
			sensorMeasurement = dict()
			self.measurements[sensor.id]= sensorMeasurement
		else:
			sensorMeasurement = self.measurements[sensor.id]

		if self.storeMeasurements:
			measurement = sensor.measure()
			for k,v in measurement.items():
				if k in sensorMeasurement:
					sensorMeasurement[k].append(v)
				else:
					if not isinstance(v,list):
						sensorMeasurement[k] = [v]
					else:
						sensorsMeasurement[k] = v
		else:
			measurement = sensor.measure()
			sensorMeasurement = dict()
			for k,v in measurement.items():
				if not isinstance(v,list):
					sensorMeasurement[k] = [v]
				else:
					sensorMeasurement[k] = v
					
		return self.getData(sensor)
	def measureAll(self):
		for k,v in self.sensors.items():
			self.measure(v)
		return self.getAllData()


	def getSensor(self,sensorId):
		if sensorId in self.sensors:			
			return self.sensors[sensorId]
		else: raise ValueError("{0} is not a valid sensor id".format(sensorId))


	@classmethod
	def registerSensor(cls,sensor):
		SensorFactory.registerSensor(sensor)