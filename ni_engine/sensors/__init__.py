from abstractSensor import AbstractSensor
from ei1050Sensor import Ei1050Sensor
from labJackInternalSensor import LabJackInternalSensor
from sensor_factory import SensorFactory
from sensor_manager import SensorManager


# Register all predefined Sensors here
SensorManager.register_sensor(Ei1050Sensor)
SensorManager.register_sensor(LabJackInternalSensor)