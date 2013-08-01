import config
from instruments.other import NewportESP301
from ..abstract_hardware import AbstractHardware
class Newport301(AbstractHardware,NewportESP301):
    code = "NEW301"
    name = "Newport ESP301 motor controller"
    description = ""
    
    #__init__ inherited from NewportESP301 which inherits from Instrument

    ## As with instrument kit we can't use inits
    ## use this setter method to set all required 
    ## variables after intialization
    def initialize(self,ID,name="name",description="description"):
        self.id = ID
        self.name = name
        self.description = description

    def disconnect(self):
        pass

    @classmethod
    def create(cls,configuration,data_handler):
        ID = configuration[config.ID]        
        d = configuration.get(config.DESCRIPTION,cls.description)
        n = configuration.get(config.NAME,cls.name)
        uri = configuration['uri']


        hardware = Newport301.open_from_uri(uri)
        hardware.initialize(ID,name=n,description=d)
        #hardware._file.debug = True
        return hardware

                    







