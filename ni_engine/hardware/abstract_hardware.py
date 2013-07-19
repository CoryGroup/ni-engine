
from tools import Item
from abc import ABCMeta, abstractmethod , abstractproperty

class AbstractHardware(Item):
    
    __metaclass__ = ABCMeta
    

    def __init__(self):
        self._name = ""
        self._description = ""

    @abstractmethod
    def disconnect(self):
        raise NotImplementedError

    # abstract method to handle sensor creation based on configuration
    @classmethod
    @abstractmethod
    def create(cls,config):
        raise NotImplementedError

    
        