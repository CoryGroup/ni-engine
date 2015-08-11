from hardware_factory import HardwareFactory
from hardware_manager import HardwareManager
from labjack import U3LV,U3HV
from test import TestHardware
from abstract_hardware import AbstractHardware
from newport import Newport301
from srs import CTC100
from nidaq import NIPCI6602
from faulhaber import FaulhaberMCLM3002Hardware
#Register all predefined hardware here

HardwareManager.register_hardware(U3LV)
HardwareManager.register_hardware(U3HV)
HardwareManager.register_hardware(TestHardware)
HardwareManager.register_hardware(Newport301)
HardwareManager.register_hardware(CTC100)
HardwareManager.register_hardware(FaulhaberMCLM3002Hardware)

# Since NIPCI6602 depends on the platform-specific DAQmx library, it may
# fail to load. If so, it will be represented by a None.
if NIPCI6602 is not None:
    HardwareManager.register_hardware(NIPCI6602)
