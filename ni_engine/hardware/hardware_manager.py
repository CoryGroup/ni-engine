import config 
import u3
from hardware_factory import HardwareFactory
class HardwareManager(object):

    def __init__(self,configuration):                
        self.configuration = configuration
        self.hardware = dict()
        self.hardwareFactory = HardwareFactory()
    
    def add_hardware(self,hardware_config):
        hardware = self.hardwareFactory.create_hardware(hardware_config)
        self.hardware[hardware.id] = hardware

    def remove_hardware(self,hardware):
        if hardware: 
            del self.hardware[hardware.id]
            hardware.disconnect()

        else: raise ValueError("Must give valid object")
    
    def remove_hardware_by_name(self,hardware_name):
        if hardware_name: 
            del self.hardware[hardware_name]
            hardware.disconnect()

        else: raise ValueError("Must give valid name")

    def remove_all(self):
        for k,v in self.hardware.iteritems():
            v.disconnect()
        self.hardware = dict()


    def parse_factory_yaml(self,config_yaml):
        return config_yaml

    def get_all_hardware(self):
        for x in self.configuration.hardware:
            self.add_hardware(x)

    def get_hardware(self,hardwareId):
        if hardwareId in self.hardware:            
            return self.hardware[hardwareId]
        else: raise ValueError("{0} is not a valid hardware id".format(hardwareId))

    @classmethod
    def register_hardware(cls,hardware):
        HardwareFactory.register_hardware(hardware)