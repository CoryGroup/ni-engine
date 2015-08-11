

from ni_engine.tools import Item
from abc import ABCMeta, abstractmethod , abstractproperty
from ni_engine.storage import DataContainer,data

class AbstractController(Item):
    
    """
    An abstractController class
    """
    
    __metaclass__ = ABCMeta 

    def __init__(self,ID,code,name,description,max_stored_data = 100):
        self._id = ID
        self._name = name
        self._description = description
        self._max_stored_data = max_stored_data
        self._code = code
    
    @property
    def max_stored_data(self):
        try:
            return self._max_stored_data
        except AttributeError,e:
            print e
            return ""

    @abstractmethod
    def connect(self):
        """
        Abstract connect method
        """
        raise NotImplementedError('Abstract method has not been implemented')

    @abstractmethod
    def disconnect(self):
        """
        Abstract disconnect method
        """
        raise NotImplementedError('Abstract method has not been implemented')  

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
        raise NotImplementedError('Abstract method has not been implemented')

    @property
    def threadsafe(self):
        """
        Must be overwritten to be made true. 
        If is threadsafe return True and can 
        be used with futures.
        Returns
        -------
        bool
        """
        return False
    
