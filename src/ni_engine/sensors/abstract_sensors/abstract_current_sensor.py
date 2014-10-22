import ni_engine.config as config
from .abstract_sensor import AbstractSensor
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
            Factor to scale all voltages reported by
        current_offset: quantities.Quantity
        units: quantities.Quantity

        """
        self.units = units
        self.max_current = max_current
        self.min_current = min_current
        self.scaling_factor = scaling_factor
        self.current_offset = current_offset

        super(CurrentIn,self).__init__(ID,code,name,description,max_stored_data)


    @abstractmethod
    def get_current(self):
        """
        Is implemented by classes that inherit this class. Method 
        should talk to sensor and report back current as Quantity.

        Returns
        -------
        quantities.Quantity
        """
        pass

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
            The current current of pin
        """

        return self.get_current()*self.scaling_factor
        

    
    
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

        Parameters
        ----------
        min_current: quantities.Quantity or float

        Returns
        -------
        quantities.Quantity
            the min current of pin
        """
        return self._min_current
    
    @min_voltage.setter
    def min_voltage(self,min_voltage):
        self._min_current = assume_units(float(min_voltage),self.units).rescale(self.units)

    @property
    def scaling_factor(self):
        """
        A factor to multiply all reported voltages by. Useful if for example, you are 
        downstepping voltages to be with max values of pin etc. 

        Parameters
        ----------
        scaling_factor: quantities.Quantity (dimensionless) or float

        Returns
        -------
        quantities.Quantity
        """
        return self._scaling_factor
    @scaling_factor.setter
    def scaling_factor(self, scaling_factor):
        self._scaling_factor = assume_units(float(scaling_factor),pq.dimensionless).rescale(pq.dimensionless)
    