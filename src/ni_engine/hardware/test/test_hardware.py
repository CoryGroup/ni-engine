from ..abstract_hardware import AbstractHardware
import ni_engine.config as config
class TestHardware(AbstractHardware):
    code = "TEST"
    
    def __init__(self,ID,name,description):
        self._name = name
        self._id = ID
        self._description = description
        self._code = TestHardware.code

    
    def disconnect(self):
        pass

    # abstract method to handle sensor creation based on configuration
    @classmethod    
    def create(cls,configuration,data_handler):
        ID = configuration.get(config.ID)
        name = configuration.get(config.NAME,"test hardware")
        description = configuration.get(config.DESCRIPTION,"has no functionality")
        return TestHardware(ID,name,description)
