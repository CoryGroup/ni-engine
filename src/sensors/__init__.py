from abstract_sensor import AbstractSensor
from labjack import Ei1050Sensor,LabJackInternalSensor
from sensor_factory import SensorFactory
from sensor_manager import SensorManager
from storage import data,DataContainer
from test import GaussianSensor
from srs import CTCThermistor
from nidaq import DAQCounterSensor
# Register all predefined Sensors here
SensorManager.register_sensor(Ei1050Sensor)
SensorManager.register_sensor(LabJackInternalSensor)
SensorManager.register_sensor(GaussianSensor)
SensorManager.register_sensor(CTCThermistor)
SensorManager.register_sensor(DAQCounterSensor)