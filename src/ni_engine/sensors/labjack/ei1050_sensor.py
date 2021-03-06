from ..abstract_sensor import AbstractSensor
import ei1050
import Queue
import ni_engine.config as config
from ni_engine.storage import DataContainer,data
import quantities as pq

class Ei1050MeasurementContainer(DataContainer):
    """
    data container for Ei1050Sensor
    """
    def __init__(self,ID,temperature,humidity,max_stored_data=-1):

        super(Ei1050MeasurementContainer,self).__init__(ID,max_stored_data)
        
        self['temperature'] = temperature
        self['humidity'] = humidity
        
    @property
    def temperature(self):
        """
        Returns
        -------
        list
            Containing `data` objects of temperature measurements
        """
        return self['temperature']
    
    @property
    def humidity(self):
        """
        Returns
        -------
        list
            Containing `data` objects of humidity measurements
        """
        return self['humidity']
    
    
    
    

class Ei1050Sensor(AbstractSensor):
    """
    Sensor implementation of Ei1050 temperature and humidity sensor. Operates on Labjack U3-LV hardware currently
    but could be extend to function on other Labjack devices. 

    ** Required Parameters:**

    * 'thread'(bool) Whether to thread measurements or not (may or may not be working)
    * 'pins' (pins on Labjack)
        * 'clock_pin'(int)
        * 'enable_pin'(int)
        * 'data_pin'(int)

    ** Optional Parameters:**

    * 'polling_time' (float) If threaded time between measurements
    """
    code = "EI1050"
    name = "EI1050Sensor"
    description = " "
    KELVIN_CONVERSION = 273.15
    def __init__(self,ID,device,data_pin,clock_pin,enable_pin,threaded=False,polling_time=0.5,name=name,description=description,retry_limit=1,max_stored_data=-1):
        """
        Parameters
        ----------
        ID : str 
            The device id
        device : U3LV
            A pieve of U3LV hardware. Currently only works on U3LV

        data_pin : int
            FIO or CIO pin number
        clock_pin : int
            FIO or CIO pin number
        enable_pin : int
            FIO or CIO pin number
        threaded : bool
            Whether measurements should be threaded or not
        name : str
        description : str
        retry_limit : int
            If measurement fails how many times to retry before quitting

        """
        self._device = device
        self._data_pin = data_pin
        self._clock_pin = clock_pin
        self._enable_pin = enable_pin
        self._threaded = threaded 
        self._polling_time = polling_time
        self._id = ID
        self._name = name
        self._description = description
        self._retry_limit = retry_limit
        self._retries = 0
        self._max_stored_data = max_stored_data
    def connect(self):
        """
        Connects created device
        Normally called by `SensorManager`
        """
        self._device.configDigital(self._data_pin)
        self._device.configDigital(self._clock_pin)
        if self._threaded:
            self._queue = Queue.LifoQueue()
            self._probe = ei1050.EI1050Reader(self._device,self._queue,enable_pinNum=self._enable_pin,data_pinNum=self._data_pin,clock_pinNum=self._clock_pin)
            
            self._probe.start()
            
        else:
            self._probe = ei1050.EI1050(self._device,enable_pinNum=self._enable_pin,data_pinNum=self._data_pin,clock_pinNum=self._clock_pin)

    def measure(self):
        """
        Measures temperature and humitdity

        Returns
        -------
        Ei1050MeasurementContainer
            A container for the measurements obtained
        """
        try:
            if self._threaded: 
                            
                reading= self._queue.get(block=True,timeout=None)
                if self._queue.qsize() >=100:
                    self._queue.clear()
                self._queue.put(reading)

            else:
                reading = self._probe.getReading()
            temp = (reading.getTemperature()  + Ei1050Sensor.KELVIN_CONVERSION)*pq.K # convert from celsius to kelvin
            temperature = data(self.id,Ei1050Sensor.code,"Temperature",temp,time=reading.getTime())
            humidity = data(self.id,Ei1050Sensor.code,"Humidity",reading.getHumidity()*pq.percent,time=reading.getTime())
            container = Ei1050MeasurementContainer(self.id,temperature,humidity,self._max_stored_data)
            self._retries =0
            return container
        except Exception as e:
            self._retries += 1
            print "data not successful retrying"
            print e
            if self._retries < self._retry_limit:
                return self.measure()
            else: 
                raise Exception("data could not be completed: Retry limit exceeded")

    def disconnect(self):
        """
        disconnects device
        """
        if self._threaded:
            self._probe.stop()
            

    def delete(self):
        """
        Deletes device
        """
        del self._probe

    @classmethod
    def create(cls,configuration,data_handler,device):
        """
        Creates device, normally called by sensor manager
        """
        #extract config info        
        ID = configuration[config.ID]
        n = Ei1050Sensor.name
        d = Ei1050Sensor.description
        if config.NAME in configuration:
            n= configuration[config.NAME]
        if config.DESCRIPTION in configuration:
            n= configuration[config.DESCRIPTION]
        threaded = configuration["threaded"]
        data_pin = configuration["pins"]["data"]
        clock_pin = configuration["pins"]["clock"]
        enable_pin = configuration["pins"]["enable"]      

        if "polling_time" in configuration:
            polling_time = configuration["polling_time"]
        else: 
            polling_time = None
        if threaded:
            if polling_time:                
                return Ei1050Sensor(ID,device,data_pin,clock_pin,enable_pin,threaded=True,polling_time=polling_time,name = n,description = d)
            else: 
                return Ei1050Sensor(ID,device,data_pin,clock_pin,enable_pin,threaded=True,name = n,description = d)
        else:
            return Ei1050Sensor(ID,device,data_pin,clock_pin,enable_pin)
