"""
Name: EI1050
Desc: A few simple classes to handle communication with the EI1050 probe
"""
import threading
import time
import sys
import u3
import u6
import ue9
from datetime import datetime
class EI1050(object):
    """
    EI1050 class to simplify communication with an EI1050 probe
    """

    U3 = 3
    U6 = 6
    UE9 = 9
    U3_STRING = "U3"
    U6_STRING = "U6"
    UE9_STRING = "UE9"
    U3_DEFAULT_DATA_PIN_NUM = 4
    U3_DEFAULT_CLOCK_PIN_NUM = 5
    U3_DEFAULT_ENABLE_PIN_NUM = 7
    U6_DEFAULT_DATA_PIN_NUM = 0
    U6_DEFAULT_CLOCK_PIN_NUM = 1
    U6_DEFAULT_ENABLE_PIN_NUM = 3
    UE9_DEFAULT_DATA_PIN_NUM = 0
    UE9_DEFAULT_CLOCK_PIN_NUM = 1
    UE9_DEFAULT_ENABLE_PIN_NUM = 3
    FIO_PIN_STATE = 0
    
    def __init__(self, device, autoUpdate=True, enable_pinNum=-1, data_pinNum = -1, clock_pinNum = -1, shtOptions = 0xc0,deviceType=3):
        self.device = device
        self.autoUpdate = autoUpdate
        self.data_pinNum = data_pinNum
        self.clock_pinNum = clock_pinNum
        self.shtOptions = shtOptions
        self.enable_pinNum = enable_pinNum
        self.curState = { 'StatusReg' : None, 'StatusCRC' : None, 'Temperature' : None, 'TemperatureCRC' : None, 'Humidity' : None, 'HumidityCRC' : None,'Time':None }
        self.deviceType = deviceType
        # Determine device type
        if not (self.deviceType == EI1050.U3 or self.deviceType == EI1050.U6 or EI1050.deviceType == self.UE9): 
            raise TypeError('Invalid device passed. Can not get default values.')

        # If not specified otherwise, use class default for the data pin number
        if self.enable_pinNum == -1:
            if self.deviceType == EI1050.U3: self.enable_pinNum = EI1050.U3_DEFAULT_ENABLE_PIN_NUM
            elif self.deviceType == EI1050.U6: self.enable_pinNum = EI1050.U6_DEFAULT_ENABLE_PIN_NUM
            elif self.deviceType == EI1050.UE9: self.enable_pinNum = EI1050.UE9_DEFAULT_ENABLE_PIN_NUM
            else:
                raise TypeError('Invalid device passed. Can not get default values.')

        # If not specified otherwise, use class default for the data pin number
        if self.data_pinNum == -1:
            if self.deviceType == EI1050.U3: self.data_pinNum = EI1050.U3_DEFAULT_DATA_PIN_NUM
            elif self.deviceType == EI1050.U6: self.data_pinNum = EI1050.U6_DEFAULT_DATA_PIN_NUM
            elif self.deviceType == EI1050.UE9: self.data_pinNum = EI1050.UE9_DEFAULT_DATA_PIN_NUM
            else:
                raise TypeError('Invalid device passed. Can not get default values.')

        # If not specified otherwise, use class default for the clock pin number
        if self.clock_pinNum == -1:
            if self.deviceType == EI1050.U3: self.clock_pinNum = EI1050.U3_DEFAULT_CLOCK_PIN_NUM
            elif self.deviceType == EI1050.U6: self.clock_pinNum = EI1050.U6_DEFAULT_CLOCK_PIN_NUM
            elif self.deviceType == EI1050.UE9: self.clock_pinNum = EI1050.UE9_DEFAULT_CLOCK_PIN_NUM
            else:
                raise TypeError('Invalid device passed. Can not get default values.')

        
        
        # Set to write out
        if self.deviceType == EI1050.U3: self.device.getFeedback(u3.BitDirWrite(self.enable_pinNum,1))
        elif self.deviceType == EI1050.U6: self.device.getFeedback(u6.BitDirWrite(self.enable_pinNum,1))

    def enableAutoUpdate(self):
        """
        Name: EI1050.enableAutoUpdate()
        Desc: Turns on automatic updating of readings
        """
        self.autoUpdate = True

    def disableAutoUpdate(self):
        """
        Name: EI1050.disableAutoUpdate()
        Desc: Truns off automatic updating of readings
        """
        self.autoUpdate = False
        
    def getStatus(self):
        """
        Name: EI1050.getStatus()
        Desc: A read of the SHT1x status register
        """
        if self.autoUpdate: self.update()
        return self.curState['StatusReg']

    def getStatusCRC(self):
        """
        Name: EI1050.getStatusCRC()
        Desc: Get cyclic reduancy check for status
        """
        if self.autoUpdate: self.update()
        return self.curState['StatusCRC']

    def getTemperature(self):
        """
        Name: EI1050.getTemperature()
        Desc: Get a temperature reading from the EI1050 probe
        """
        if self.autoUpdate: self.update()
        return self.curState['Temperature']

    def getTemperatureCRC(self):
        """
        Name: EI1050.getStatusCRC()
        Desc: Get cyclic redundancy check for temperature reading
        """
        if self.autoUpdate: self.update()
        return self.curState['TemperatureCRC']

    def getHumidity(self):
        """
        Name: EI1050.getHumidity()
        Desc: Get a humidity reading from the EI1050 probe
        """
        if self.autoUpdate: self.update()
        return self.curState['Humidity']

    def getHumidityCRC(self):
        """
        Name: EI1050.getHumidityCRC()
        Desc: Get cyclic redundancy check for humidity reading
        """
        if self.autoUpdate: self.update()
        return self.curState['HumidityCRC']

    def getReading(self):
        """
        Name: EI1050.getReading()
        Desc: Get a reading and create a Reading object with the information
        """
        if self.autoUpdate: self.update()
        if self.curState.has_key('StatusCRC'): return Reading(self.curState['StatusReg'], self.curState['StatusCRC'], self.curState['Temperature'], self.curState['TemperatureCRC'], self.curState['Humidity'], self.curState['HumidityCRC'])
        else: return Reading(self.curState['StatusReg'], 0, self.curState['Temperature'], self.curState['TemperatureCRC'], self.curState['Humidity'], self.curState['HumidityCRC'])
    def update(self):
        """
        Name: EI1050.update()
        Desc: Gets a fresh set of readings from this probe
        """
        self.writeBitState(self.enable_pinNum,1) # Enable the probe
        self.curState = self.device.sht1x(self.data_pinNum, self.clock_pinNum, self.shtOptions)
        self.writeBitState(self.enable_pinNum,0) # Disable the probe
         
    def writeBitState(self, pinNum, state):
        """
        Name: EI1050.writeBitState(pinNum, state)
        Desc: Device independent way to write bit state
        """
        
        if self.deviceType == EI1050.U3: self.device.getFeedback(u3.BitStateWrite(pinNum,state))
        elif self.deviceType == EI1050.U6: self.device.getFeedback(u6.BitStateWrite(pinNum,state))
        elif self.deviceType == EI1050.UE9: self.device.singleIO(1, pinNum, Dir=1, State=state)
class Reading:
    """
    A class that represents a reading taken from an EI1050 probe
    """

    def __init__(self, status, statusCRC, temperature, temperatureCRC, humidity, humidityCRC):
        self.__status = status
        self.__statusCRC = statusCRC
        self.__temperature = temperature
        self.__temperatureCRC = temperatureCRC
        self.__humidity = humidity
        self.__humidityCRC = humidityCRC
        self.__time = datetime.now()
    def getStatus(self):
        """
        Name: Reading.getStatus()
        Desc: Returns that status of the EI1050 probe at the time of this reading
        """
        return self.__status

    def getStatusCRC(self):
        """
        Name: Reading.getStatusCRC()
        Desc: Get the cyclic reduancy check for status at the time of this reading
        """
        return self.__statusCRC

    def getTemperature(self):
        """
        Name: Reading.getTemperature()
        Desc: Get the temperature reported by the EI1050 probe at the time of this reading
        """
        return self.__temperature

    def getTemperatureCRC(self):
        """
        Name: Reading.getStatusCRC()
        Desc: Get cyclic redundancy check for the temperature reading
        """
        return self.__temperatureCRC

    def getHumidity(self):
        """
        Name: Reading.getHumidity()
        Desc: Get the humidity reported by the EI1050 probe at the time of this reading
        """
        return self.__humidity

    def getHumidityCRC(self):
        """
        Name: Reading.getHumidityCRC()
        Desc: Get cyclic redundancy check for humidity reading
        """
        return self.__humidityCRC

    def getTime(self):
        """
        Name: Reading.getTime()
        Desc: Get time of measurement
        """
        return self.__time

class EI1050Reader(threading.Thread):
    """
    A simple threading class to read EI1050 values
    """
    def __init__(self, device, targetQueue, polling_time=1, autoUpdate=True, enable_pinNum=-1, data_pinNum = -1, clock_pinNum = -1, shtOptions = 0xc0):

        try:
            self.polling_time = polling_time # How long to wait between reads (in sec)
            self.targetQueue = targetQueue # The queue in which readings will be placed
            self.probe = EI1050(device, autoUpdate, enable_pinNum, data_pinNum, clock_pinNum, shtOptions)
            self.running = False
            self.exception = None
            
            threading.Thread.__init__(self, group=None)
        except:
           self.exception = sys.exc_info()

    def stop(self):
        """
        Stops this thread's activity. Note: this may not be immediate
        """
        self.running = False
    
    def run(self):
        self.running = True
        while self.running:
            try:
                self.targetQueue.put(self.probe.getReading())
                time.sleep(self.polling_time)
            except:
                self.exception = sys.exc_info()
                self.stop()
                break
