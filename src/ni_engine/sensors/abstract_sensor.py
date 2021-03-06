from ni_engine.tools import Item
from abc import ABCMeta, abstractmethod , abstractproperty

class AbstractSensor(Item):

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
            raise 
        

    @abstractmethod
    def connect(self):
        """
        Connects sensor
        """
        raise NotImplementedError('Abstract method has not been implemented')

    @abstractmethod
    def disconnect(self):
        """
        Disconnects sensor
        """
        raise NotImplementedError('Abstract method has not been implemented')

    @abstractmethod
    def delete(self):
        """
        Deletes sensor
        """
        raise NotImplementedError('Abstract method has not been implemented')

    @abstractmethod
    def measure(self):
        """
        Called to measure sensor

        Returns
        -------
        DataContainer
        
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
    
    

    # abstract method to handle sensor creation based on configuration
    @classmethod
    @abstractmethod
    def create(cls,config,data_handler,hardware):
        """
        Abstract method that when implemented is the intializer method for the sensor.
        
        Parameters
        ----------
        config : configuration
        data_handler : data_handler
        hardware : HardwareManager

        Returns
        -------
        AbstractSensor
        """
        raise NotImplementedError('Abstract method has not been implemented')


    
