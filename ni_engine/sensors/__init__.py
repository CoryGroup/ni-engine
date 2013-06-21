from abstractSensor import *
from ei1050Sensor import *
from sensorFactory import *
from sensorManager import *


# Register all predefined Sensors here
SensorManager.registerSensor(Ei1050Sensor)