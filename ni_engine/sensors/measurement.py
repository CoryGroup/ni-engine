from datetime import datetime

class Measurement(object):

    def __init__(self,sensor_id,sensorCode,measurementName,value,time=datetime.now()):
        self.sensor_id = sensor_id
        self.sensorCode = sensorCode
        self.measurementName = measurementName
        self.value = value 
        self.time = time

    def __lt__(self,other):
        return self.time < other.time