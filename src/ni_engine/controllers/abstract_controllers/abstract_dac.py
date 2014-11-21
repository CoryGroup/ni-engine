import ni_engine.config as config
from ..abstract_controller import AbstractController
from abc import abstractmethod,abstractproperty
from ni_engine.util_fns import assume_units
import quantities as pq

class AbstractDAC(AbstractController):
    """
    Class that should be implemented by all DAC's to maintain a 
    common interface. 
    """
    @property
    def absolute(self):
        """
        Whether the DAC can set negative voltages

        Parameters
        ----------
        absolute : bool
        """
        if not hasattr(self,"_absolute"):
            self._absolute = True
        return self._absolute

    
        self._max_voltage = v
    @absolute.setter
    def absolute(self,absolute):
        self._absolute = absolute
        
    @property
    def max_voltage(self):
        """
        Max voltage the DAC can be set to

        Parameters
        ----------
        max_voltage : float or `quantities.Quantity`

        Returns
        `quantities.Quantity`

        """
        if not hasattr(self,"_max_voltage"):
            
            self._max_voltage = assume_units(0.0,pq.V)
            
        
        return self._max_voltage
    
    @max_voltage.setter
    def max_voltage(self, max_voltage):
        
        v = assume_units(float(max_voltage),pq.V).rescale(
            pq.V)
        self._max_voltage = v
        

      
    @property
    def voltage(self):
        """
        Set the voltage to a certain value.

        Parameters
        ----------
        voltage : `quantities.Quantity` or float

        Returns 
        -------
        `quantities.Quantity
        """
        if not hasattr(self,"_voltage"):
            self._voltage = 0.0* pq.V
        return self._voltage

    @voltage.setter
    def voltage(self,voltage):        
        if self.absolute:
            voltage = abs(voltage)

        v = assume_units(float(voltage),pq.V).rescale(pq.V)        
        self.max_voltage
        if v.magnitude > self.max_voltage.magnitude:
            raise ValueError("The voltage of {0}, cannot be set greater than {1}".format(self,v))
        elif v.magnitude < -self.max_voltage.magnitude:
            raise ValueError("The voltage of {0}, cannot be set less than {1}".format(self,v))        
        self._voltage = v
        self._set_voltage(v)
        
    
    @abstractmethod
    def _set_voltage(self,voltage):
        """
        Is called by `set_voltage`, must be implemented for `set_voltage` to work. 

        Parameters
        ----------
        voltage : `quantities.Quantity`
        """
        raise NotImplementedError('Abstract method has not been implemented')


    
