import ni_engine.config as config
from ..abstract_sensor import AbstractSensor
from abc import abstractmethod,abstractproperty
from ni_engine.util_fns import assume_units
import quantities as pq



class CurrentIn(AbstractSensor):


    def __init__(self,ID,code,max_current,min_current=0*pq.A,scaling_factor=1,current_offset=0*pq.A,units=pq.A,name="",description="",max_stored_data=100):
        """
        Initialize the abstrac pin

        Parameters
        ----------
        max_current: quantities.Quantity or float
        min_current: quantities.Quantity or float
        scaling_factor: quantities.Quantity or float
            Factor to scale all currents measured
        current_offset: quantities.Quantity
        units: quantities.Quantity

        """
        self.units = units
        self._max_current = assume_units(float(min_current),self.units).rescale(self.units)
        self._min_current = assume_units(float(max_current),self.units).rescale(self.units)
        self._scaling_factor = scaling_factor
        self._current_offset = assume_units(float(current_offset),self.units).rescale(self.units)

        super(CurrentIn,self).__init__(ID,code,name,description,max_stored_data)


    @abstractmethod
    def _get_current(self):
        """
        Is implemented by classes that inherit this class. Method 
        should talk to sensor and report back current as Quantity.

        Returns
        -------
        quantities.Quantity
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
    def current(self):
        """
        Retrieves the current current at the pin. 

        Returns
        -------        
        quantities.Quantity
            The current of pin
        """
      
        return self._get_current()*self.scaling_factor + self.current_offset
        

    
    
    @property
    def max_current(self):
        """
        The maximum voltage that the pin can read. 

        Parameters
        ----------
        max_voltage: quantities.Quantity or float

        Returns
        -------
        quantities.Quantity
            the max voltage of pin
        """
        return self._max_current
    
    @max_current.setter
    def max_current(self,max_current):
        self._max_current = assume_units(float(max_current),self.units).rescale(self.units)

    @property
    def min_current(self):
        """
        The minimum current that the pin can read. 

        Returns
        -------
        quantities.Quantity
            the min current of pin
        """
        return self._min_current
    
    @property
    def scaling_factor(self):
        """
        A factor to multiply all reported voltages by. Useful if for example, you are 
        downstepping voltages to be with max values of pin etc. 

        Returns
        -------
        quantities.Quantity
        """
        return self._scaling_factor
    
    @property
    def current_offset(self):
        """
        How much the current is offset from 0A 

        Returns
        -------
        quantities.Quantity
            the current offset
        """
        return self._current_offset