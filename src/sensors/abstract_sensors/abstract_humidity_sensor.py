import config
from ..abstract_sensor import AbstractSensor
from abc import abstractmethod,abstractproperty
from util_fns import assume_units
import quantities as pq
import numpy as np


class AbstractHumiditySensor(AbstractSensor):


    def __init__(self,running_average_length=100):
        self.running_average_length = 100
        self._running_humidity = []
        



    @property 
    def humidity(self):
        """
        Returns
        -------
        quantities.Quantity
            The humidity of sensor
        """
        temp = assume_units(float(self._get_humidity()),self.units).rescale(self.units)
        self._running_humidity = self._running_humidity[-self.running_average_length:]

    
    @abstractmethod
    def _get_humidity(self):
        """
        Returns 
        -------
        quantities.Quantity
            The humidity of sensor
        """
        pass
    @abstractproperty
    def units(self):
        """
        Returns
        -------
        quantities.Quantity
            The units of humidity
        """
        pass

    @property 
    def average_humidity(self):
        """
        Returns
        -------
        quantities.Quantity
            The average humidity 
        """
        return assume_units(float(np.mean(self._running_humidity)),self.units).rescale(self.units)

    @abstractproperty
    def std_dev_humidity(self):
        """
        Returns
        -------
        quantities.Quantity
            The standard deviation of humidity
        """
        return assume_units(float(np.std(self._running_humidity)),self.units).rescale(self.units)