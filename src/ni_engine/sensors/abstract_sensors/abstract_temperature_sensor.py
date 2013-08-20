import ni_engine.config as config
from ..abstract_sensor import AbstractSensor
from abc import abstractmethod,abstractproperty
from ni_engine.util_fns import assume_units
import quantities as pq
import numpy as np


class AbstractTemperatureSensor(AbstractSensor):


    def __init__(self,running_average_length=100):
        """
        Parameters
        ----------
        running_average_length: int 
            number of data_points to take average over
        """
        self.running_average_length = 100
        self._running_temperature = []
        



    @property 
    def temperature(self):
        """
        Returns
        -------
        quantities.Quantity
            The temperature of sensor
        """
        temp = assume_units(float(self._get_temperature()),self.units).rescale(self.units)
        self._running_temperature = self._running_temperature[-self.running_average_length:]

    
    @abstractmethod
    def _get_temperature(self):
        """
        Returns 
        -------
        quantities.Quantity
            The temperature of sensor
        """
        pass
    @abstractproperty
    def units(self):
        """
        Returns
        -------
        quantities.Quantity
            The units of temperature
        """
        pass

    @property 
    def average_temperature(self):
        """
        Returns
        -------
        quantities.Quantity
            The average temperature 
        """
        return assume_units(float(np.mean(self._running_temperature)),self.units).rescale(self.units)

    @abstractproperty
    def std_dev_temperature(self):
        """
        Returns
        -------
        quantities.Quantity
            The standard deviation of temperature
        """
        return assume_units(float(np.std(self._running_temperature)),self.units).rescale(self.units)
