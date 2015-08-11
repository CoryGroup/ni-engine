from ni_engine.sensors.abstract_sensor import AbstractSensor
from ni_engine.sensors.labjack import Ei1050Sensor,LabJackInternalSensor,LJAnalogIn,LJDigitalIn,\
										LJCurrentIn
from ni_engine.sensors.sensor_factory import SensorFactory
from ni_engine.sensors.sensor_manager import SensorManager
from ni_engine.storage import data,DataContainer
from test import GaussianSensor
from srs import CTCThermistor
from nidaq import DAQCounterSensor
# Register all predefined Sensors here
SensorManager.register_sensor(Ei1050Sensor)
SensorManager.register_sensor(LabJackInternalSensor)
SensorManager.register_sensor(LJAnalogIn)
SensorManager.register_sensor(LJDigitalIn)
SensorManager.register_sensor(LJCurrentIn)
SensorManager.register_sensor(GaussianSensor)
SensorManager.register_sensor(CTCThermistor)

# Like the PCI6602 hardware, this can fail, so we should check for that.
if DAQCounterSensor is not None:
    SensorManager.register_sensor(DAQCounterSensor)
