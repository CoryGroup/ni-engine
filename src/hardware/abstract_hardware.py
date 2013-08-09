
from tools import Item
from abc import ABCMeta, abstractmethod , abstractproperty

class AbstractHardware(Item):
    """
    Abstract Hardware class that all hardware classes must implement
    """
    __metaclass__ = ABCMeta
    

    

    @abstractmethod
    def disconnect(self):
        """
        disconnect from hardware
        """
        raise NotImplementedError

    # abstract method to handle sensor creation based on configuration
    @classmethod
    @abstractmethod
    def create(cls,config,data_handler):
        """
        Create the hardware. Is called from `HardwareManager`.

        Parameters
        ----------
        config : dict 
            Dictionary containing required configuration information
        data_handler : DataHandler 
            contains data taken and old loaded data if configured for it.  

        """
        raise NotImplementedError

    
        