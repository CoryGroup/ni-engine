import ni_engine.config as config 
from ..labjack import LJTDAC
from ..abstract_controller import AbstractController


class KepcoSupply(AbstractController):
    code = 'KEPCO'
    name = 'Kepco Power Supply'
    description = 'Voltage controlled Kepco Power Supply 0-10V'
    default_voltage = 0

    def __init__(self,ID,hardware,voltage_pin,crowbar_pin,max_voltage,default_voltage=0,default_crowbar=None, name=name,description=description):
        self.default_crowbar = default_crowbar
        if default_crowbar is None:
            self.default_crowbar = max_voltage

        self._id = ID 
        self._hardware = hardware
        self._voltage_pin = voltage_pin 
        self._crowbar_pin = crowbar_pin             
        self._default_voltage = default_voltage
        self._max_voltage = max_voltage        
        self._name = name
        self._description = description
        self._voltageOut = self._default_voltage
        
        if abs(voltage_pin-crowbar_pin) != 1 : raise ValueError("Pins must be on same LJTDAC")

        self.dac_pin = min(self._crowbar_pin,self._voltage_pin)

        if min(self._voltage_pin,self._crowbar_pin) == self._voltage_pin :
            self.voltage_a = self.dac_voltage(self._default_voltage)
            self.voltage_b = self.dac_voltage(self.default_crowbar)
        else:
            self.voltage_a = self.dac_voltage(self.default_crowbar)
            self.voltage_b = self.dac_voltage(self._default_voltage)        

    def connect(self):
        self.initialize_defaults()

    def disconnect(self):
        pass

    def initialize_defaults(self):
        self.ljtdac = LJTDAC('kepco supply dac',self._hardware,min(self._voltage_pin,self._crowbar_pin),default_voltage=0,max_voltage=10,name="LJTDAC Kepco",description="Controller managed by Kepco Supply to control it")
        self.set_voltage()
    
    def set_voltage(self,voltage=None,crowbar=None):
        if voltage is not None:
            if min(self._voltage_pin,self._crowbar_pin) == self._voltage_pin :
                self.voltage_a = self.dac_voltage(voltage)
            else:
                self.voltage_b = self.dac_voltage(voltage)

        if crowbar is not None:
            if min(self._voltage_pin,self._crowbar_pin) == self._voltage_pin :
                self.voltage_b = self.dac_voltage(crowbar)
            else:
                self.voltage_a = self.dac_voltage(crowbar)
        
        self.ljtdac.set_voltage(voltage_a=self.voltage_a,voltage_b=self.voltage_b)

    def dac_voltage(self,voltage):
        return 10.0*voltage/self._max_voltage

    @classmethod 
    def create(cls,configuration,data_handler,hardware,sensors):
        ID = configuration[config.ID]
        n = cls.name
        d = cls.description
        if config.NAME in configuration:
            n= configuration[config.NAME]
        if config.DESCRIPTION in configuration:
            d= configuration[config.DESCRIPTION]
        
        voltage_pin = configuration['pins']['voltage']
        crowbar_pin = configuration['pins']['crowbar']
        max_voltage = configuration['max_voltage']
        crowbarVoltage = max_voltage
        if 'crowbarVoltage' in configuration:
            crowbarVoltage = configuration['crowbarVoltage']

        default_voltage = cls.default_voltage
        if 'default_voltage' in configuration:
            default_voltage = configuration['default_voltage']
                
        return KepcoSupply(ID,hardware,voltage_pin,crowbar_pin,max_voltage,crowbarVoltage,default_voltage,name=n,description=d)

