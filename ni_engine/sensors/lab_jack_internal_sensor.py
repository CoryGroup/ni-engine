from abstractSensor import AbstractSensor
import config
from measurement import Measurement

class LabJackInternalSensor(AbstractSensor):
    code = "LABINT"
    name = "Labjack internal temperature sensor"
    description = "Built-in labjack sensor measures temperature"

    def __init__(self,ID,device,name=name,description=description):
        self.device = device
        self.id = ID 
        self.name = name
        self.description = description

    def connect(self):
        pass

    def measure(self):
        temp = self.device.getTemperature()
        measurementDict = dict()
        measurementDict['temperature'] = Measurement(self.id,LabJackInternalSensor.code,"Temperature",temp)
        return measurementDict

    def disconnect(self):
        del self

    @classmethod
    def create(cls,configuration,device):
        ID = configuration[config.ID]
        n = LabJackInternalSensor.name
        d = LabJackInternalSensor.description
        if config.NAME in configuration:
            n= configuration[config.NAME]
        if config.DESCRIPTION in configuration:
            n= configuration[config.DESCRIPTION]
        return LabJackInternalSensor(ID,device,n,d)