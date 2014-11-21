import ni_engine.config as config
from ..abstract_sensor import AbstractSensor
from abc import abstractmethod,abstractproperty
from ni_engine.util_fns import assume_units
import quantities as pq



class DigitalIn(AbstractSensor):


    def __init__(self,ID,code,high_voltage,low_voltage=0*pq.V,units=pq.V,name="",description="",max_stored_data=100):
        """
        Initialize the abstrac pin

        Parameters
        ----------
        high_voltage: quantities.Quantity or float
        low_voltage: quantities.Quantity or float
        units: quantities.Quantity

        """
        self.units = units
        self.high_voltage = high_voltage
        self.low_voltage = low_voltage
        
        

        super(DigitalIn,self).__init__(ID,code,name,description,max_stored_data)

    @property
    def is_high(self):
        """
        check if pin is high or not

        Returns
        -------
        bool
        """
        
        is_high = bool(self.val)        
        return is_high

    @abstractproperty
    def val(self):
        """
        Return whether the pin is 0(low) or 1(high)

        Returns
        -------
        int
        """
        raise NotImplementedError('Abstract method has not been implemented')

    @property
    def units(self):
        return self._units
    @units.setter
    def units(self, unit):
        assert isinstance(unit,pq.Quantity)
        self._units = unit
    


    @property 
    def voltage(self):
        """
        Retrieves the current voltage at the pin. 

        Returns
        -------        
        quantities.Quantity
            The current voltage of pin
        """

        if self.is_high:
            return self.high_voltage
        else: 
            return self.low_voltage
        

    
    
    @property
    def low_voltage(self):
        """
        The voltage of low state of pin. 

        Parameters
        ----------
        low_voltage: quantities.Quantity or float

        Returns
        -------
        quantities.Quantity
            the low voltage of pin
        """
        return self._low_voltage
    
    @low_voltage.setter
    def low_voltage(self,low_voltage):
        self._low_voltage = assume_units(float(low_voltage),self.units).rescale(self.units)

    @property
    def high_voltage(self):
        """
        The voltage of high state of pin

        Parameters
        ----------
        high_voltage: quantities.Quantity or float

        Returns
        -------
        quantities.Quantity
            the high voltage of pin
        """
        return self._high_voltage
    
    @high_voltage.setter
    def high_voltage(self,high_voltage):
        self._high_voltage = assume_units(float(high_voltage),self.units).rescale(self.units)

  