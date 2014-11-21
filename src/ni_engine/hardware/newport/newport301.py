import ni_engine.config as config
from instruments.other import NewportESP301
from ..abstract_hardware import AbstractHardware
class Newport301(AbstractHardware,NewportESP301):
    """
    NewportESP301 class. Sets up communication with 
    NewportESP301 device via Instrument kit. 

    **Required Parameters:**

    * 'uri' (str)
       * Is a uri string formatted for instrument kit. For example
         "serial://COM10?baud=19200" is a valid uri if the Newport 
         is on serial port 'COM10'. The baud parameter specifies 
         the serial baud rate which is 19200 for the Newport. 
         Other uri, can be for gpib or usb, see InstrumentKit
         documentation for details.


    **Optional Parameters::**

    **None**
    """

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
        raise NotImplementedError('Abstract method has not been implemented')

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

                    







