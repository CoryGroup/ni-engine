import config 
from instruments.srs import SRSCTC100

from ..abstract_sensors import AbstractTemperatureSensor

from storage import DataContainer,data

class CTCThermistor(AbstractTemperatureSensor):
    code = 'CTCTHERMISTOR'
    name = 'SRSCTC100 Thermistor'
    description = 'Stanford Research Systems CTC 100 Thermistor Channel'    
    
    

    def __init__(self,ID,hardware,channel_name,max_stored_data=100,name=name,description=description):
        """
        Initialize the thermistor 
        """
                  
        self._id = ID         
        self._ctc100 = self._hardware = hardware                              
        self._name = name
        self._description = description
        self._max_stored_data = max_stored_data
        self._channel_name = channel_name        
        super(CTCThermistor,self).__init__() 

    def connect(self):
        """
        Connect to axis
        """
        self._channel = self._ctc100.channel[self._channel_name]

    def disconnect(self):
        pass

    @property
    def channel(self):
        return self._channel 
    

    @property
    def temperature(self):
        temp = self.channel.value    
        return data(self.id,self.code,"current temperature",temp)
    @property
    def average_temperature(self):
        temp = self.channel.average
        return data(self.id,self.code,"average temperature",temp)

    @property 
    def std_dev_temperature(self):
        std = self.channel.std_dev
        return data(self.id,self.code,"standard deviation of temperature",std)

    @property
    def units(self):
        return self.channel.units
    
    def measure(self):
        con = DataContainer(self.id,self._max_stored_data)
        con['temperature'] = self.temperature
        con['average_temperature'] = self.average_temperature
        con['std_dev_temperature'] = self.std_dev_temperature        
        return con

    def _get_temperature(self):
        pass
    def delete(self):
        del self

    @classmethod 
    def create(cls,configuration,data_handler,hardware):

        ID = configuration[config.ID]
        n = configuration.get(config.NAME,cls.name)
        d = configuration.get(config.DESCRIPTION,cls.description)
        channel_name = configuration.get("channel_name")
                
        return CTCThermistor(ID,hardware,channel_name,name=n,description=d)

