from .labjack_analog_in import LJAnalogIn
from ..abstract_sensors import CurrentIn
import ni_engine.config as config
from ni_engine.storage import DataContainer,data
import quantities as pq
from ni_engine.hardware.labjack import U3LV,U3HV
import u3
from ni_engine.util_fns import assume_units

    
    
    
    

class LJCurrentIn(CurrentIn):
    """
    Current sensor for Labjack device. Converts an analog voltage, to a current. Requires external 
    current sensing hardware
    """
    code = "LJCURRENTIN"
    name = "Labjack Current Pin"
    description = "Measures a current by converting an input current to a voltage based off some scaling factor"
    def __init__(self,ID,device,pin,max_current,min_current=0*pq.A,voltage_to_current_factor=1*pq.A/pq.V,
        scaling_factor=1,current_offset=0*pq.A,name=name,description=description,max_stored_data=100):
        """
        Parameters
        ----------
        ID : str 
            The device id
        device : AbstractHardware
            A pieve of U3 hardware.

        pin : int
            Current In Pin. Must support analog voltage measurements
        voltage_to_current_factor : int or quantities.Quantity
            Dictates how input voltages are converted to a current 
        scaling_factor: int
            How much to scale the measured current by
        current_offset : quantities.Quantity or float
            How much to offset outputted current by 
        name : str
        description : str
        max_stored_data : int

        """
        self._device = device
        self._pin = pin
        self._voltage_to_current_factor = voltage_to_current_factor
        self.analog_in = LJAnalogIn("{}_vin".format(ID),device,pin,1,name="{} analog in".format(name),
            description="analog in for current sensor: {}".format(ID),max_stored_data=max_stored_data)
        
        super(LJCurrentIn,self).__init__(ID,LJCurrentIn.code,max_current,min_current,scaling_factor,current_offset,name=name,
            description=description,max_stored_data=max_stored_data)

    def connect(self):
        """
        Connects created device
        Normally called by `SensorManager`
        """
        # connect to analog in pin
        self.analog_in.connect()    
        
    @property
    def voltage_to_current_factor(self):
        return self._voltage_to_current_factor
    
        
    
    def _get_current(self):
        """
        Get the current on the pin by converting the voltage

        Returns
        -------
        quantities.Quantity
            of Amps
        """
        return self.analog_in.voltage*self.voltage_to_current_factor
    def measure(self):
        """
        Measures whether pin is high or not

        Returns
        -------
        DataContainer
            A container for the measurements obtained
        """
        con = DataContainer(self.id,self.max_stored_data)
        con['max_current'] = data(self.id,self.code,'max_current',self.max_current)
        con['min_current'] = data(self.id,self.code,'min_current',self.min_current)
        con['scaling_factor'] = data(self.id,self.code,'scaling_factor',self.scaling_factor)
        con['voltage_to_current_factor'] = data(self.id,self.code,'voltage_to_current_factor',self.voltage_to_current_factor)
        con['current'] = data(self.id,self.code,'current',self.current)

        return con

    def disconnect(self):
        """
        disconnects device
        """
        self.analog_in.disconnect()
        raise NotImplementedError('Abstract method has not been implemented')
            

    def delete(self):
        """
        Deletes device
        """
        del self.analog_in
        del self

    @classmethod
    def create(cls,configuration,data_handler,device):
        """
        Creates device, normally called by sensor manager
        """
        #extract config info        
        ID = configuration[config.ID]
        name = configuration.get(config.NAME,cls.name)
        description = configuration.get(config.DESCRIPTION,cls.description)
        pin = configuration['pin']
        scaling_factor = assume_units(float(configuration.get('scaling_factor',1)),
            pq.A/pq.V).rescale(pq.A/pq.V)
        max_stored_data = configuration.get(config.MAX_DATA,100)
        max_current = configuration.get('max_current')
        min_current = configuration.get('min_current',0*pq.A)
        voltage_to_current_factor = configuration.get('voltage_to_current_factor',1*pq.A/pq.V)
        current_offset = configuration.get('current_offset',0*pq.A)
        return LJCurrentIn(ID,device,pin,max_current,min_current=min_current,
            voltage_to_current_factor=voltage_to_current_factor,
            scaling_factor=scaling_factor,current_offset=current_offset,name=name,
            description=description,max_stored_data=max_stored_data)
