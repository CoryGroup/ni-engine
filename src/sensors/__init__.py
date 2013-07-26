from abstract_sensor import AbstractSensor
from labjack import Ei1050Sensor,LabJackInternalSensor
from sensor_factory import SensorFactory
from sensor_manager import SensorManager
from storage import Data,DataContainer
from test import GaussianSensor
# Register all predefined Sensors here
SensorManager.register_sensor(Ei1050Sensor)
SensorManager.register_sensor(LabJackInternalSensor)
SensorManager.register_sensor(GaussianSensor)