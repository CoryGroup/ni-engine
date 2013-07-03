import config
from abstractController import AbstractController
import struct
class LJTDAC(AbstractController):
	code = 'LJTDAC'
	name = 'LJTDAC Extension'
	description = 'A dac extension that can output from -10V to +10V'
	defaultVoltage = 0.0
	maxVoltage = 10.0
	DAC_PIN_DEFAULT = 0
	U3_DAC_PIN_OFFSET = 0
	EEPROM_ADDRESS = 0x50
	DAC_ADDRESS = 0x12
 	def __init__(self,ID,device,dacPin,defaultVoltage=0,maxVoltage=10,name=name,description=description):
		self.id = ID 
		self.device = device
		self.dacPin = dacPin	
		self.defaultVoltage = defaultVoltage
		self.maxVoltage = maxVoltage
		self.name = name
		self.description = description
		
		if self.device.code == "U3LV":
			self.sclPin = self.dacPin + LJTDAC.U3_DAC_PIN_OFFSET
			self.sdaPin = self.sclPin + 1
		else:
			self.sclPin = self.dacPin
			self.sdaPin = self.sclPin + 1

		self.currVoltageA = self.defaultVoltage
		self.currVoltageB = self.defaultVoltage

	def connect(self):
		self.initializeDefault()

	def initializeDefault(self):
		self.getCalConstants()
		self.setVoltage(voltageA=self.defaultVoltage,voltageB=self.defaultVoltage)

	def disconnect(self):
		pass

	def setVoltage(self,voltageA=None,voltageB=None,retries=5):
		if voltageA is not None:
			self.voltageA = voltageA
		if voltageB is not None:  
			self.voltageB = voltageB
		if self.voltageA > self.maxVoltage:
			self.voltageA %= self.maxVoltage
		if self.voltageB > self.maxVoltage:
			self.voltageA %= self.maxVoltage

		try:
			self.device.i2c(LJTDAC.DAC_ADDRESS, [48, int(((self.voltageA*self.aSlope)+self.aOffset)/256), int(((self.voltageA*self.aSlope)+self.aOffset)%256)], SDAPinNum = self.sdaPin, SCLPinNum = self.sclPin)
			self.device.i2c(LJTDAC.DAC_ADDRESS, [49, int(((self.voltageB*self.bSlope)+self.bOffset)/256), int(((self.voltageB*self.bSlope)+self.bOffset)%256)], SDAPinNum = self.sdaPin, SCLPinNum = self.sclPin)
		except Exception as a:
			print e
			print("retrying")
			self.setVoltage(retries=retries-1)
            
		
	def getCalConstants(self):		 
              
        # Make request
		data = self.device.i2c(LJTDAC.EEPROM_ADDRESS, [64], NumI2CBytesToReceive=36, SDAPinNum = self.sdaPin, SCLPinNum = self.sclPin)
		response = data['I2CBytes']
		self.aSlope = self.toDouble(response[0:8])
		self.aOffset = self.toDouble(response[8:16])
		self.bSlope = self.toDouble(response[16:24])
		self.bOffset = self.toDouble(response[24:32])

		if 255 in response: raise IOError("The calibration constants for controller: {0} seem a little off. Please go into settings and make sure the pin numbers are correct and that the LJTickDAC is properly attached.".format(self.id))
	
	def toDouble(self,buffer):
		"""
		Name: toDouble(buffer)
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
		ID = configuration[config.idString]
		n = cls.name
		d = cls.description
		if config.nameString in configuration:
			n= configuration[config.nameString]
		if config.descriptionString in configuration:
			d= configuration[config.descriptionString]
		
		dacPin = configuration['pins']['dac']	

		maxVoltage = cls.maxVoltage
		if 'maxVoltage' in configuration:
			maxVoltage = configuration['maxVoltage']
		
		defaultVoltage = cls.defaultVoltage
		if 'defaultVoltage' in configuration:
			defaultVoltage = configuration['defaultVoltage']		
		
		return LJTDAC(ID,hardware,dacPin,defaultVoltage=defaultVoltage,maxVoltage = maxVoltage, name=n,description=d) 