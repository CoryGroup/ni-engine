from abstractSensor import AbstractSensor
from ei1050Sensor import Ei1050Sensor
from labJackInternalSensor import LabJackInternalSensor
from sensorFactory import SensorFactory
from sensorManager import SensorManager


# Register all predefined Sensors here
SensorManager.registerSensor(Ei1050Sensor)
SensorManager.registerSensor(LabJackInternalSensor)