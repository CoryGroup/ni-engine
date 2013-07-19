from hardware_factory import HardwareFactory
from hardware_manager import HardwareManager
from u3lv import U3LV
from abstract_hardware import AbstractHardware
#Register all predefined hardware here

HardwareManager.register_hardware(U3LV)