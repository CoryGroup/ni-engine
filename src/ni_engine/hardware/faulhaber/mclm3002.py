import ni_engine.config as config
from instruments.faulhaber import FaulhaberMCLM3002
from ..abstract_hardware import AbstractHardware

class FaulhaberMCLM3002Hardware(AbstractHardware,NewportESP301):
    """
    FaulhaberMCLM3002Hardware class. Sets up communication with 
    FaulhaberMCLM3002 device via Instrument kit. 

    **Required Parameters:**

    * 'uri' (str)
       * Is a uri string formatted for instrument kit. For example
         "serial://COM10?baud=9600" is a valid uri if the Newport 
         is on serial port 'COM10'. The baud parameter specifies 
         the serial baud rate which is 9600 for the Newport. 
         Other uri, can be for gpib or usb, see InstrumentKit
         documentation for details.


    **Optional Parameters::**
    * 'velocity_source' (str)
        * Where the device should take its velocity commands from. Should be
        the string name of enum :type: `FaulhaberMCLM3002.VelocitySource`
    * 'answer_mode' (str)
        * How the device should communicate via serial commands. Should be
        the string name of enum :type: `FaulhaberMCLM3002.AnswerMode` 
        Enume to specify answer mode

            0: No asynchronous responses
            1: Allow asynchronous responses
            2: All commands with confirmation and asynchronous
            responses
            3: Debug mode, sent commands are returned
            4-7: analogous to 0-3, but responses resulting from a
            command in the sequence program are not sent
            (cannot be set via Motion Manager)

        Call via string correspondance below:                
            NoAsync = 0 
            AsyncResp = 1 
            AsyncAndConfirmation = 2 
            DebugMode = 3
            NoAsyncNoSeqResp = 4 
            AsyncRespNoSeqResp = 5 
            AsyncAndConfirmationNoSeqResp = 6 
            DebugModeNoSeqResp = 7

    **None**
    """

    code = "MCLM3002"
    name = "Faulhaber MCLM3002 Motor Controller"
    description = "Linear Motor Controller"
    
    #__init__ inherited from FaulhaberMCLM3002 which inherits from Instrument

    ## As with instrument kit we can't use inits
    ## use this setter method to set all required 
    ## variables after intialization
    def initialize(self,ID,name="name",description="description",answer_mode=FaulhaberMCLM3002.AnswerMode.NoAsync,
                    velocity_source=FaulhaberMCLM3002.VelocitySource.CONTMOD):
        self.id = ID
        self.name = name
        self.description = description
        self.answer_mode = answer_mode
        self.velocity_source = velocity_source

    def disconnect(self):
        raise NotImplementedError('Abstract method has not been implemented')

    @classmethod
    def create(cls,configuration,data_handler):
        ID = configuration[config.ID]        
        d = configuration.get(config.DESCRIPTION,cls.description)
        n = configuration.get(config.NAME,cls.name)
        uri = configuration['uri']
        # Must be the string name of one of FaulhaberMCLM3002.VelocitySource
        velocity_source = FaulhaberMCLM3002.VelocitySource[configuration.get('velocity_source','SerialInterface')]
        # Must be the string name of one of FaulhaberMCLM3002.AnswerMode 
        answer_mode = FaulhaberMCLM3002.AnswerMode[configuration.get('answer_mode','NoAsync')]


        hardware = FaulhaberMCLM3002Hardware.open_from_uri(uri)
        hardware.initialize(ID,name=n,description=d,answer_mode=answer_mode,velocity_source=velocity_source)
        #hardware._file.debug = True
        return hardware

                    
