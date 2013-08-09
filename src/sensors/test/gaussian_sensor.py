from tools import Item
from ..abstract_sensor import AbstractSensor
import random
from storage import DataContainer,data
import config
class GaussianSensor(AbstractSensor): 
    """
    Abstract sensor that who's measurement simply 
    pulls a value from a gaussian distribution. 
    """
    code = "GAUSSSENSOR"
    def __init__(self,ID,mu=1,sigma=1,max_measurements=-1,name="",description=""):
        self._mu =mu 
        self._sigma = sigma
        self._code = GaussianSensor.code
        self._name = name
        self._description = description
        self._id = ID
        self._max_measurements = max_measurements
    def connect(self):
        """
        Connects sensor
        """
        pass

    
    def disconnect(self):
        """
        Disconnects sensor
        """
        pass


    def delete(self):
        """
        Deletes sensor
        """
        del self

    
    def measure(self):
        """
        Called to measure sensor
        Returns
        -------
        DataContainer
        """
        val = random.gauss(self._mu,self._sigma)
        measurement = data(self.id,self.code,self.name,val)
        container = DataContainer(self._id,self._max_measurements)
        container["gaussian"]=measurement
        return container

    # abstract method to handle sensor creation based on configuration
    @classmethod    
    def create(cls,configuration,data_handler,hardware):
        """
        Abstract method that when implemented is the intializer method for the sensor.
        
        Parameters
        ----------
        config : configuration
        data_handler : data_handler
        hardware : HardwareManager

        Returns
        -------
        GaussianSensor
        """
        mu = configuration.get("mu",1)
        sigma = configuration.get("sigma",1)
        ID = configuration.get(config.ID)
        name = configuration.get(config.NAME,"gaussian sensor")
        description = configuration.get(config.DESCRIPTION,"pulls from gaussian distribution")
        max_measurements = configuration.get(config.MAX_DATA,-1)
        return GaussianSensor(ID,mu,sigma,max_measurements,name,description)


    