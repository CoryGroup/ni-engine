from hardware_factory import HardwareFactory
from hardware_manager import HardwareManager
from labjack import U3LV
from test import TestHardware
from abstract_hardware import AbstractHardware
from newport import Newport301
from srs import CTC100
from ni import NIPCI6602
#Register all predefined hardware here

HardwareManager.register_hardware(U3LV)
HardwareManager.register_hardware(TestHardware)
HardwareManager.register_hardware(Newport301)
HardwareManager.register_hardware(CTC100)
HardwareManager.register_hardware(NIPCI6602)