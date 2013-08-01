

from tools import Item
from abc import ABCMeta, abstractmethod , abstractproperty
from storage import DataContainer,Data

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

    @abstractmethod 
    def get_status(self):
        """
        Returns a data_container containing parameters of controller relevant to status 

        Returns
        -------
        DataContainer
            Made up of data objects containing elements relevent to status
        """

    # abstract method to handle sensor creation based on configuration

    @classmethod
    @abstractmethod
    def create(cls,config,data_handler,sensors,hardware):
        """
        Abstract method that when implemented is the intializer method for the controller.
        Take a configuration
        """
        pass

    