import config
from abstractController import AbstractController
import struct
class LJTDAC(AbstractController):
    code = 'LJTDAC'
    name = 'LJTDAC Extension'
    description = 'A dac extension that can output from -10V to +10V'
    default_voltage = 0.0
    max_voltage = 10.0
    DAC_PIN_DEFAULT = 0
    U3_DAC_PIN_OFFSET = 0
    EEPROM_ADDRESS = 0x50
    DAC_ADDRESS = 0x12
    CALIBRATION_OFFSET = 0.03
    
    def __init__(self,ID,device,dac_pin,default_voltage=0,max_voltage=10,name=name,description=description):
        self.id = ID 
        self.device = device
        self.dac_pin = dac_pin    
        self.default_voltage = default_voltage
        self.max_voltage = max_voltage
        self.name = name
        self.description = description
        
        if self.device.code == "U3LV":
            self.sclPin = self.dac_pin + LJTDAC.U3_DAC_PIN_OFFSET
            self.sdaPin = self.sclPin + 1
        else:
            self.sclPin = self.dac_pin
            self.sdaPin = self.sclPin + 1

        self.currVoltageA = self.default_voltage
        self.currVoltageB = self.default_voltage

    def connect(self):
        self.initialize_default()

    def initialize_default(self):
        self.get_cal_constants()
        self.set_voltage(voltage_a=self.default_voltage,voltage_b=self.default_voltage)

    def disconnect(self):
        pass

    def set_voltage(self,voltage_a=None,voltage_b=None,retries=5):
        self.get_cal_constants()        
        if voltage_a is not None:
            self.voltage_a = voltage_a
        if voltage_b is not None:  
            self.voltage_b = voltage_b
        
        #apply calibration function
        self.voltage_a = self.calibration_function(self.voltage_a)
        self.voltage_b = self.calibration_function(self.voltage_b)
        
        if self.voltage_a > self.max_voltage:
            self.voltage_a = self.max_voltage
        elif self.voltage_a < -self.max_voltage:
            self.voltage_a = -self.max_voltage

        if self.voltage_b > self.max_voltage:
            self.voltage_b = self.max_voltage
        elif self.voltage_b < -self.max_voltage:
            self.voltage_b = -self.max_voltage

        try:
            self.device.i2c(LJTDAC.DAC_ADDRESS, [48, int(self.calibration_function(((self.voltage_a*self.aSlope)+self.aOffset))/256), int(self.calibration_function(((self.voltage_a*self.aSlope)+self.aOffset))%256)], SDAPinNum = self.sdaPin, SCLPinNum = self.sclPin)
            self.device.i2c(LJTDAC.DAC_ADDRESS, [49, int(((self.voltage_b*self.bSlope)+self.bOffset)/256), int(((self.voltage_b*self.bSlope)+self.bOffset)%256)], SDAPinNum = self.sdaPin, SCLPinNum = self.sclPin)
        except Exception as a:
            print e
            print("retrying")
            self.set_voltage(retries=retries-1)            
        
    def get_cal_constants(self):             
        # Make request
        data = self.device.i2c(LJTDAC.EEPROM_ADDRESS, [64], NumI2CBytesToReceive=36, SDAPinNum = self.sdaPin, SCLPinNum = self.sclPin)
        response = data['I2CBytes']
        self.aSlope = self.to_double(response[0:8])
        self.aOffset = self.to_double(response[8:16])
        self.bSlope = self.to_double(response[16:24])
        self.bOffset = self.to_double(response[24:32])

        if 255 in response: raise IOError("The calibration constants for controller: {0} seem a little off. Please go into settings and make sure the pin numbers are correct and that the LJTickDAC is properly attached.".format(self.id))
    
    #calibrates function to be more accurate
    #testing has shown than an adjusted voltage follows equation
    #As far as I can tell builtin calibration function for dac is optimal
    #just return the required voltage than until a better calibration function is found
    def calibration_function(self,voltage):
        return voltage
        
    def to_double(self,buffer):
        """
        Name: to_double(buffer)
        Args: buffer, an array with 8 bytes
        Desc: Converts the 8 byte array into a floating point number.
        """
        if type(buffer) == type(''):
            bufferStr = buffer[:8]
        else:
            bufferStr = ''.join(chr(x) for x in buffer[:8])
        dec, wh = struct.unpack('<Ii', bufferStr)
        return float(wh) + float(dec)/2**32

    @classmethod 
    def create(cls,configuration,hardware,sensors):
        ID = configuration[config.ID]
        n = cls.name
        d = cls.description
        if config.NAME in configuration:
            n= configuration[config.NAME]
        if config.DESCRIPTION in configuration:
            d= configuration[config.DESCRIPTION]
        
        dac_pin = configuration['pins']['dac']    

        max_voltage = cls.max_voltage
        if 'max_voltage' in configuration:
            max_voltage = configuration['max_voltage']
        
        default_voltage = cls.default_voltage
        if 'default_voltage' in configuration:
            default_voltage = configuration['default_voltage']        
        
        return LJTDAC(ID,hardware,dac_pin,default_voltage=default_voltage,max_voltage = max_voltage, name=n,description=d) 