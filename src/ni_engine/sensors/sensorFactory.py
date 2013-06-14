import ei1050Sensor

class SensorFactory:

	def createSensor(self,config):
		sensorType = getType(config)		

		if sensorType == "EI1050":
			sensor = createEI1050(self,config)


		if  not sensor:
			raise Exception("Sensor Type not recognised") 

		return sensor

	def getInterface(self,config):
		pass

	def getType(self,config):
		pass

	def createEI1050(self,config):
		#extract config info


		if threaded:
			if pollingTime:
				return ei1050Sensor(device,dataPin,clockPin,enablePin,threaded=True,pollingTime=pollingTime)
			else: 
				return ei1050Sensor(device,dataPin,clockPin,enablePin,threaded=True)
		else:
			return ei1050Sensor(device,dataPin,clockPin,enablePin)