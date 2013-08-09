import config 
import u3
from hardware_factory import HardwareFactory
class HardwareManager(object):
    """
    Manages all hardware objects. This includes setup, management and deletion
    """
    def __init__(self,configuration,data_handler):                
        """
        Parameters
        ----------
        configuration : Configuration
        data_handler : DataHandler 
        """
        self.configuration = configuration
        self._hardware = dict()
        self._data_handler = data_handler
        self._hardwareFactory = HardwareFactory(self._data_handler)
    
    def add_hardware(self,hardware_config):
        """
        Based on configuration file. Creates a piece of hardware and 
        adds it to management

        Parameters 
        ----------
        hardware_config : dict 
            Contains all information for creation of hardware object
        """
        hardware = self._hardwareFactory.create_hardware(hardware_config)
        self._hardware[hardware.id] = hardware

    def add_all_hardware(self):
        """
        Adds all hardware in configuration
        """
        for x in self.configuration.hardware:
            self.add_hardware(x)

    def remove_hardware(self,hardware):
        """
        removes piece of hardware 

        Parameters
        ----------
        hardware : AbstractHardware or str
        """
        if isinstance(hardware,str):
            hardware =self.get_hardware(hardware) 
        
        if isinstance(hardware,AbstractHardware):
            del self._hardware[hardware.id]
            hardware.disconnect()
        else: raise ValueError("Must give valid hardware object or string")
    
    

    def remove_all(self):
        """
        Remove all hardware objects in manager
        """
        for k,v in self._hardware.iteritems():
            v.disconnect()
        self._hardware = dict()


    def get_all_hardware(self):
        """
        Creates and adds to management all hardware defined in configuration file
        """
        for x in self.configuration.hardware:
            self.add_hardware(x)

    def get_hardware(self,hardwareId):
        """
        Gets a piece of hardware in management by id name

        Parameters
        ----------
        hardwareId : str 

        Returns
        -------
        AbstractHardware
        """
        if hardwareId in self._hardware and isinstance(hardwareId,str):            
            return self._hardware[hardwareId]
        else: raise ValueError("{0} is not a valid hardware id".format(hardwareId))

    @classmethod
    def register_hardware(cls,hardware):
        """
        Used for registering hardware class with `HardwareFactory`   
        """
        HardwareFactory.register_hardware(hardware)