import ni_engine.config as config
from instruments.srs import SRSCTC100
from ..abstract_hardware import AbstractHardware

class CTC100(AbstractHardware,SRSCTC100):
    """
    Hardware object for Stanford Research Systems CTC 100 
    Cryogenic temperature controller. handles hardware initialization.

    **Required Parameters:**

    * 'uri' (str)
       * Is a uri string formatted for instrument kit. For example
         "tcpip://192.168.0.100:23 is a valid uri if the Newport 
         is on a local lan at ip address 192.168.0.100 and listening
         on port 23. Other uri, can be for gpib, serial or usb. See InstrumentKit
         documentation for details.

    **Optional Parameters:**
    **None**
    """
    code = "CTC100"
    name = "Stanford Research Systems CTC100"
    description = "Cryogenic Temperature Controller"
    
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


        hardware = CTC100.open_from_uri(uri)
        hardware.initialize(ID,name=n,description=d)
        #hardware._file.debug = True
        return hardware

                    






