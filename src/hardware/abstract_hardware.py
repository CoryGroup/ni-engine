
from tools import Item
from abc import ABCMeta, abstractmethod , abstractproperty

class AbstractHardware(Item):
    
    __metaclass__ = ABCMeta
    

    

    @abstractmethod
    def disconnect(self):
        raise NotImplementedError

    # abstract method to handle sensor creation based on configuration
    @classmethod
    @abstractmethod
    def create(cls,config,data_handler):
        raise NotImplementedError

    
        