

from tools import Item
from abc import ABCMeta, abstractmethod , abstractproperty

class AbstractController(Item):
    
    """
    An abstractController class
    """
    
    __metaclass__ = ABCMeta 

    

    @abstractmethod
    def connect(self):
        """
        Abstract connect method
        """
        pass

    @abstractmethod
    def disconnect(self):
        """
        Abstract disconnect method
        """
        pass  

    # abstract method to handle sensor creation based on configuration

    @classmethod
    @abstractmethod
    def create(cls,config,data_handler,sensors,hardware):
        """
        Abstract method that when implemented is the intializer method for the controller.
        Take a configuration
        """
        pass

    