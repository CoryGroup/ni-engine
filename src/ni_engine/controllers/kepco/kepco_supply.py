import ni_engine.config as config 
from ..labjack import LJTDAC
from ..abstract_controller import AbstractController
from ni_engine.util_fns import assume_units
import quantities as pq
from ni_engine.storage import DataContainer,data

class KepcoSupply(AbstractController):
    code = 'KEPCO'
    name = 'Kepco Power Supply'
    description = 'Voltage controlled Kepco Power Supply 0-10V'
    MAX_VOLTAGE = pq.Quantity(120,pq.V)

    def __init__(self,ID,hardware,voltage_pin,crowbar_pin,max_voltage=pq.Quantity(0,pq.V),
        default_voltage=pq.Quantity(0,pq.V),default_crowbar=None, name=name,
        description=description,max_stored_data=100):

        self._default_crowbar = assume_units(float(default_crowbar),pq.V).rescale(
            pq.V)
        if default_crowbar is None:
            self._default_crowbar = assume_units(float(max_voltage),pq.V).rescale(
            pq.V)
        
        self._hardware = hardware
        self._voltage_pin = voltage_pin 
        self._crowbar_pin = crowbar_pin             
        self._default_voltage = assume_units(float(default_voltage),pq.V).rescale(pq.V)
        self._max_voltage = assume_units(float(max_voltage),pq.V).rescale(pq.V)       
        
        self._voltage = self._default_voltage
        self._crowbar = self._default_crowbar        
        
        super(KepcoSupply,self).__init__(ID,KepcoSupply.code,name,description,max_stored_data)
    def connect(self):
        self.initialize_defaults()

    def disconnect(self):
        pass

    def initialize_defaults(self):
        self._voltage_dac = LJTDAC('kepco voltage dac',self._hardware,self._voltage_pin,self.dac_voltage(self._voltage),
            max_voltage=self.dac_voltage(self._max_voltage),name="LJTDAC Kepco",
            description="Controller managed by Kepco Supply to control it")
        self._crowbar_dac = LJTDAC('kepco crowbar dac',self._hardware,self._crowbar_pin,
            self.dac_voltage(self._crowbar),
            max_voltage=self.dac_voltage(self._max_voltage),name="LJTDAC Kepco",
            description="Controller managed by Kepco Supply to control it")
        self._voltage_dac.connect()
        self._crowbar_dac.connect()        
        self.crowbar = self._crowbar
        self.voltage = self._voltage
    
    @property
    def voltage(self):
        return self.dac_to_kepco_voltage(self._voltage_dac.voltage)
    @voltage.setter
    def voltage(self, voltage):
        """
        Set, the voltage out of the Kepco Supply. From 0-120V.

        Parameters
        ----------
        voltage: pq.Quantity or float 

        Returns 
        -------
        pq.Quantity

        """
        self._voltage = assume_units(float(voltage),pq.V).rescale(
            pq.V)  
        self._voltage_dac.voltage = self.dac_voltage(self._voltage)

    property
    def crowbar(self):
        return self.dac_to_kepco_voltage(self._crowbar_dac.voltage)
    @voltage.setter
    def crowbar(self, crowbar):
        """
        Set, the crowbar voltage out of the Kepco Supply. From 0-120V.

        Parameters
        ----------
        voltage: pq.Quantity or float 

        Returns 
        -------
        pq.Quantity

        """
        self._crowbar = assume_units(float(crowbar),pq.V).rescale(
            pq.V)  
        self._crowbar_dac.voltage =  self.dac_voltage(self._crowbar)

    def dac_voltage(self,voltage):
        """
        Convert the desired output voltage of the Kepco Supply
        to output voltage for dac

        Parameters
        ----------
        voltage: pq.Quantity or float

        Returns
        ------- 
        pq.Quantity

        """
        voltage = assume_units(float(voltage),pq.V).rescale(
            pq.V)
        v = 10.0*voltage/120.
        if v>self.MAX_VOLTAGE:
            return self.dac_voltage(self.MAX_VOLTAGE)
        else: 
            return v

    def dac_to_kepco_voltage(self,voltage):
        voltage = assume_units(float(voltage),pq.V).rescale(
            pq.V)
        v = 120.*voltage/10.0
        return v

    def get_status(self):
        d = DataContainer(self.id,self.max_stored_data)
        d['voltage'] = data(self.id,self.code,'voltage',self.voltage)
        d['crowbar'] = data(self.id,self.code,'crowbar',self.crowbar)
        return d

    @classmethod 
    def create(cls,configuration,data_handler,hardware,sensors):
        """
        Used to create controller from Controller_manager
        """
        ID = configuration[config.ID]
        n = cls.name
        d = cls.description
        if config.NAME in configuration:
            n= configuration[config.NAME]
        if config.DESCRIPTION in configuration:
            d= configuration[config.DESCRIPTION]
        
        voltage_pin = configuration['pins']['voltage']
        crowbar_pin = configuration['pins']['crowbar']
        max_voltage = pq.Quantity(configuration['max_voltage'],pq.V)
        crowbar_voltage = max_voltage
        max_stored_data = configuration.get(config.MAX_DATA,100)      
        

        default_voltage = pq.Quantity(configuration.get('default_voltage',0),pq.V)
                
        return KepcoSupply(ID,hardware,voltage_pin,crowbar_pin,max_voltage,crowbar_voltage,default_voltage,name=n,description=d,max_stored_data=max_stored_data)

