import config 
from ..abstract_sensor import AbstractSensor
from storage import DataContainer,data
import PyDAQmx as daq
import ctypes as C
import time
class NICounter(AbstractTemperatureSensor):
    code = 'NICOUNTER'
    name = 'National Instruments event counter'
    description = 'Counts number of events that have occurred'    
    
    

    def __init__(self,ID,hardware,output_configuration,input_configuration,max_stored_data=100,name=name,description=description):
        """
        Initialize the thermistor 
        """
                  
        self._id = ID         
        self._ni6602 = self._hardware = hardware                              
        self._name = name
        self._description = description
        self._max_stored_data = max_stored_data
        self._hardware_path = hardware.path
        self._channel_name = channel_name 
        
        super(NICounter,self).__init__() 

    def connect(self):
        """
        Connect to axis
        """
        self._channel = self._ctc100.channel[self._channel_name]

    def disconnect(self):
        pass

    
    
    def measure(self):
        con = DataContainer(self.id,self._max_stored_data)
        con['temperature'] = self.temperature
        con['average_temperature'] = self.average_temperature
        con['std_dev_temperature'] = self.std_dev_temperature        
        return con

    
    def delete(self):
        del self
    def parse_input(self,input_configuration):
        self._input_counter = output_configuration['counter']
        self._input_name = output_configuration['name']

        # either 'rising' or 'falling' 
        active = output_configuration['active_edge']
        if active == 'rising':
            self._active_edge = daq.DAQmx_Val_Rising
        elif active == 'falling':
            self._active_edge = daq.DAQmx_Val_Falling
        else:
            raise ValueError('active_edge ({0})is not valid DAQmx type'.format(active))
    def parse_output(self,output_configuration):
        self._output_counter = output_configuration['counter']
        self._output_name = output_configuration['name']
        self._output_delay = output_configuration['delay']
        self._output_high_time = output_configuration['high_time']
        self._output_low_time = output_configuration['low_time']
        
        

        # check to see if we want continous sampling
        if 'continuous' in output_configuration:

    @classmethod 
    def create(cls,configuration,data_handler,hardware):

        ID = configuration[config.ID]
        n = configuration.get(config.NAME,cls.name)
        d = configuration.get(config.DESCRIPTION,cls.description)
        channel_name = configuration.get("channel_name")
                
        return CTCThermistor(ID,hardware,channel_name,name=n,description=d)

