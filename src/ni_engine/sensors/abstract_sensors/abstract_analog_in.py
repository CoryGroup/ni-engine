import ni_engine.config as config
from ..abstract_sensor import AbstractSensor
from abc import abstractmethod,abstractproperty
from ni_engine.util_fns import assume_units
import quantities as pq



class AnalogIn(AbstractSensor):


    def __init__(self,ID,code,max_voltage,min_voltage=0*pq.V,scaling_factor=1,units=pq.V,name="",description="",max_stored_data=100):
        """
        Initialize the abstrac pin

        Parameters
        ----------
        max_voltage: quantities.Quantity or float
        min_voltage: quantities.Quantity or float
        scaling_factor: quantities.Quantity or float
            Factor to scale all voltages reported by
        units: quantities.Quantity

        """
        self.units = units
        self.max_voltage = max_voltage
        self.min_voltage = min_voltage
        self.scaling_factor = scaling_factor
        

        super(AnalogIn,self).__init__(ID,code,name,description,max_stored_data)


    @abstractmethod
    def _get_voltage(self):
        """
        Is implemented by classes that inherit this class. Method 
        should talk to sensor and report back voltage as Quantity.

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
    def voltage(self):
        """
        Retrieves the current voltage at the pin. 

        Returns
        -------        
        quantities.Quantity
            The current voltage of pin
        """

        return self._get_voltage()*self.scaling_factor
        

    
    
    @property
    def max_voltage(self):
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
        return self._max_voltage
    
    @max_voltage.setter
    def max_voltage(self,max_voltage):
        self._max_voltage = assume_units(float(max_voltage),self.units).rescale(self.units)

    @property
    def min_voltage(self):
        """
        The minimum voltage that the pin can read. 

        Parameters
        ----------
        min_voltage: quantities.Quantity or float

        Returns
        -------
        quantities.Quantity
            the min voltage of pin
        """
        return self._min_voltage
    
    @min_voltage.setter
    def min_voltage(self,min_voltage):
        self._min_voltage = assume_units(float(min_voltage),self.units).rescale(self.units)

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
    