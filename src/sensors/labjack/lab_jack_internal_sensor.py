from ..abstract_sensor import AbstractSensor
import config
from storage import DataContainer,Data
import quantities as pq
class TemperatureContainer(DataContainer):
    """
    Container for holding temperature measurements. Implements `AbstractMeasurementContainer`
    """

    def __init__(self,ID,temperature,max_stored_data=-1):
        super(TemperatureContainer,self).__init__(ID,max_stored_data=-1)
        self['temperature'] = temperature

    @property
    def temperature(self):
        """
        Returns
        -------
        Data
            returns the temperature measurement
        """

        return self['temperature']   
    
    

class LabJackInternalSensor(AbstractSensor):
    """
    Labjack internal temperature temperature sensor. Is built into the labjack.
    Configuration has options(required if not otherwise noted):
    .. code-block :: yaml
        code: LABINT
        id: string for other systems to refer to device by
        name: human readable name #optional
        description: human readable description #optional


    """
    code = "LABINT"
    name = "Labjack internal temperature sensor"
    description = "Built-in labjack sensor measures temperature"

    def __init__(self,ID,device,name=name,description=description,max_stored_data=-1):
        """
        Parameters
        ----------
        ID : str 
        device : AbstraceHardware
        name : str
        description : str
        """
        self._device = device
        self._id = ID 
        self._name = name
        self._description = description
        self._max_stored_data = -1

    def connect(self):
        """
        Intialize device and connect it to hardware if required
        """
        pass

    def measure(self):
        """
        Get a measurement from the device

        Returns
        -------
        TemperatureContainer
        """
        temp = self._device.getTemperature()*pq.K
        measurement = Data(self._id,LabJackInternalSensor.code,"Temperature",temp)
        container = TemperatureContainer(self._id,measurement,self._max_stored_data)
        return container

    def disconnect(self):
        """
        Disconnects device from hardware 
        """
        pass

    def delete(self):
        """
        Deletes itself
        """
        del self

    @classmethod
    def create(cls,configuration,data_handler,device):
        """
        Creates object from configuration and hardware

        Parameters 
        ----------

        configuration : Configuration

        device : U3LV

        Returns 
        -------

        LabJackInternalSensor

        """
        ID = configuration[config.ID]
        n = LabJackInternalSensor.name
        d = LabJackInternalSensor.description
        if config.NAME in configuration:
            n= configuration[config.NAME]
        if config.DESCRIPTION in configuration:
            n= configuration[config.DESCRIPTION]
        return LabJackInternalSensor(ID,device,n,d)
