from hardware_factory import HardwareFactory
from hardware_manager import HardwareManager
from u3lv import U3LV
from test_hardware import TestHardware
from abstract_hardware import AbstractHardware
from newport301 import Newport301
#Register all predefined hardware here

HardwareManager.register_hardware(U3LV)
HardwareManager.register_hardware(TestHardware)
HardwareManager.register_hardware(Newport301)