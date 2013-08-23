from ..abstract_sensors import DigitalIn
import ni_engine.config as config
from ni_engine.storage import DataContainer,data
import quantities as pq
from ni_engine.hardware.labjack import U3LV,U3HV
import u3

    
    
    
    

class LJDigitalIn(DigitalIn):
    """
    Implementation of DigitalPin for Labjack. 

    **Required Parameters:**

    * 'pin'(int) Pin on Labjack

    *Optional Parameters:**

    **None**

    """
    code = "LJDIGITALIN"
    name = "Labjack Digital Pin"
    description = " "
    U3_HIGH_VOLTAGE = pq.Quantity(3.3,pq.V)
    U3_UNITS = pq.V
    def __init__(self,ID,device,pin,name=name,description=description,max_stored_data=100):
        """
        Parameters
        ----------
        ID : str 
            The device id
        device : AbstractHardware
            A pieve of U3LV hardware. Currently only works on U3LV

        pin : int
            Digital In Pin
        name : str
        description : str
        max_stored_data : int

        """
        self._device = device
        self._pin = pin
        if isinstance(self._device,(U3LV,U3HV)):
            super(LJDigitalIn,self).__init__(ID,LJDigitalIn.code,LJDigitalIn.U3_HIGH_VOLTAGE,units=LJDigitalIn.U3_UNITS,name=name,
                description=description,max_stored_data=max_stored_data)
        else:
            raise TypeError("{0} is not supported for this sensor".format(type(self._device)))
    def connect(self):
        """
        Connects created device
        Normally called by `SensorManager`
        """
        # set pin to digital
        self._device.configDigital(self._pin)
        #set pin to input
        self._device.getFeedback(u3.BitDirWrite(self._pin, 0))
        
    @property
    def is_high(self):
        """
        check if pin is high or not

        Returns
        -------
        bool
        """
        is_high = bool(self._device.getFeedback(u3.BitStateRead(self._pin)))        
        return is_high
    
    def measure(self):
        """
        Measures whether pin is high or not

        Returns
        -------
        DataContainer
            A container for the measurements obtained
        """
        con = DataContainer(self.id,self.max_stored_data)
        con['is_high'] = data(self.id,self.code,'is_high',self.is_high)
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
        max_stored_data = configuration.get(config.MAX_DATA,100)
        
        return LJDigitalIn(ID,device,pin,name=name,description=description,max_stored_data=max_stored_data)
