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
    def __init__(self,ID,device,pin,scaling_factor=1,current_offset=0*pq.A,name=name,description=description,max_stored_data=100):
        """
        Parameters
        ----------
        ID : str 
            The device id
        device : AbstractHardware
            A pieve of U3 hardware.

        pin : int
            Current In Pin. Must support analog voltage measurements
        scaling_factor : int
            Dictates how input voltages are converted to a current 
        current_offset : quantities.Quantity or float
            How much to offset outputted current by 
        name : str
        description : str
        max_stored_data : int

        """
        self._device = device
        self._pin = pin
        if isinstance(self._device,U3LV):
            super(LJCurrentIn,self).__init__(ID,LJCurrentIn.code,LJCurrentIn.U3LV_MAX_VOLTAGE,LJCurrentIn.U3LV_MIN_VOLTAGE,scaling_factor,
                units=LJCurrentIn.U3_UNITS,name=name,description=description,max_stored_data=max_stored_data)
        elif isinstance(self._device,U3HV):
            # Check if it is high-voltage input
            if 0<= self._pin <=3:
               super(LJCurrentIn,self).__init__(ID,LJCurrentIn.code,LJCurrentIn.U3HV_MAX_VOLTAGE,LJCurrentIn.U3HV_MIN_VOLTAGE,scaling_factor,
                units=LJCurrentIn.U3_UNITS,name=name,description=description,max_stored_data=max_stored_data)  
            #otherwise it is same as U3-LV
            else:
                super(LJCurrentIn,self).__init__(ID,LJCurrentIn.code,LJCurrentIn.U3LV_MAX_VOLTAGE,LJCurrentIn.U3LV_MIN_VOLTAGE,scaling_factor,
                units=LJCurrentIn.U3_UNITS,name=name,description=description,max_stored_data=max_stored_data)  

        else:   
            raise TypeError("{0} is not supported for this sensor".format(type(self._device)))
    def connect(self):
        """
        Connects created device
        Normally called by `SensorManager`
        """
        # set pin to analog
        self._device.configAnalog(self._pin)        
        
        
    
    def _get_voltage(self):
        """
        Get the voltage on the pin

        Returns
        -------
        quantities.Quantity
            of voltage
        """
        voltage = assume_units(float(self._device.getAIN(self._pin)),self.units).rescale(self.units)
        return voltage
    
    def measure(self):
        """
        Measures whether pin is high or not

        Returns
        -------
        DataContainer
            A container for the measurements obtained
        """
        con = DataContainer(self.id,self.max_stored_data)
        con['max_voltage'] = data(self.id,self.code,'max_voltage',self.max_voltage)
        con['min_voltage'] = data(self.id,self.code,'min_voltage',self.min_voltage)
        con['scaling_factor'] = data(self.id,self.code,'scaling_factor',self.scaling_factor)
        con['voltage'] = data(self.id,self.code,'voltage',self.voltage)

        return con

    def disconnect(self):
        """
        disconnects device
        """
        pass
            

    def delete(self):
        """
        Deletes device
        """
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
            pq.dimensionless).rescale(pq.dimensionless)
        max_stored_data = configuration.get(config.MAX_DATA,100)

        
        return LJCurrentIn(ID,device,pin,scaling_factor=scaling_factor,name=name,
            description=description,max_stored_data=max_stored_data)
