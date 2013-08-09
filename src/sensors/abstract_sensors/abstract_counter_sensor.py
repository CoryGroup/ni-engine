##
# abstract_counter_sensor.py: Definition of ABC for counting devices.
##
# Part of the NI Engine project.
##

## IMPORTS #####################################################################

import config
from ..abstract_sensor import AbstractSensor
from abc import abstractmethod,abstractproperty
from util_fns import assume_units
import quantities as pq
import numpy as np

## CLASSES #####################################################################

class AbstractCounterSensor(AbstractSensor):
    """
    Abstract sensor used to represent single- or multi-channel counting devices.
    """
    
    def __init__(self):
        super(AbstractCounterSensor, self).__init__()

    @abstractproperty
    def n_channels(self):
        """
        Returns
        -------
        n_channels : int
            Number of channels admitted by this sensor.
        """
        pass

    @abstractproperty
    def counts(self):
        """
        Returns
        -------
        counts : quantities.Quantity
            The number of counts seen since the last reset.
        """
        pass
        
    @property
    def units(self):
        """
        Returns
        -------
        units : quantities.Quantity
            The units of the counting device.
        """
        return pq.counts
        
    def reset(self):
        """
        Sets the counts for each channel to zero.
        """
        raise NotImplementedError()
        

