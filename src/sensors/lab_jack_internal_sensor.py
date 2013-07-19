from abstract_sensor import AbstractSensor
import config
from measurement import Measurement
from measurement_container import AbstractMeasurementContainer
import quantities as pq
class TemperatureContainer(AbstractMeasurementContainer):
    """
    Container for holding temperature measurements. Implements `AbstractMeasurementContainer`
    """

    def __init__(self,temperature):
        super(TemperatureContainer,self).__init__(temperature=temperature)

    @property
    def temperature(self):
        """
        Returns
        -------
        Measurement
            returns the temperature measurement
        """

        return self['temperature']   
    
    def _join(self,container):
        return TemperatureContainer(self.temperature+container.temperature)

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

    def __init__(self,ID,device,name=name,description=description):
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
        measurement = Measurement(self._id,LabJackInternalSensor.code,"Temperature",temp)
        container = TemperatureContainer(measurement)
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
    def create(cls,configuration,device):
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
