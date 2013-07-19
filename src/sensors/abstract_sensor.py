from tools import Item
from abc import ABCMeta, abstractmethod , abstractproperty

class AbstractSensor(Item):

    __metaclass__ = ABCMeta
    
    
    

    @abstractmethod
    def connect(self):
        raise NotImplementedError

    @abstractmethod
    def disconnect(self):
        raise NotImplementedError

    @abstractmethod
    def delete(self):
        raise NotImplementedError

    @abstractmethod
    def measure(self):
        raise NotImplementedError

    # abstract method to handle sensor creation based on configuration
    @classmethod
    @abstractmethod
    def create(cls,config):
        raise NotImplementedError


    