from abstract_sensor import AbstractSensor
import ei1050
import Queue
import config
from measurement import Measurement
from measurement_container import AbstractMeasurementContainer

class Ei1050MeasurementContainer(AbstractMeasurementContainer):
    def __init__(self,temperature,humidity):

        super(ei1050MeasurementContainer,self).__init__(temperature=temperature ,humidity=humidity)

    @property
    def temperature(self):
        return self['temperature']
    
    @property
    def humidity(self):
        return self['humidity']
    
    
    
    def _join(self,container):        

        return Ei1050MeasurementContainer(self.temperature+container.temperature,
                self.humidity+container.humidity)

class Ei1050Sensor(AbstractSensor):
    code = "EI1050"
    name = "EI1050Sensor"
    description = " "
    KELVIN_CONVERSION = 293.15
    def __init__(self,ID,device,data_pin,clock_pin,enable_pin,threaded=False,polling_time=0.5,name=name,description=description,retry_limit=20):
        self.device = device
        self.data_pin = data_pin
        self.clock_pin = clock_pin
        self.enable_pin = enable_pin
        self.threaded = threaded 
        self.polling_time = polling_time
        self.id = ID
        self.name = name
        self.description = description
        self.retry_limit = retry_limit
        self.retries = 0

    def connect(self):
        if self.threaded:
            self.queue = Queue.LifoQueue()
            self.probe = ei1050.EI1050Reader(self.device,self.queue,enable_pinNum=self.enable_pin,data_pinNum=self.data_pin,clock_pinNum=self.clock_pin)
            
            self.probe.start()
            
        else:
            self.probe = ei1050.EI1050(self.device,enable_pinNum=self.enable_pin,data_pinNum=self.data_pin,clock_pinNum=self.clock_pin)

    def measure(self):
        try:
            if self.threaded: 
                            
                reading= self.queue.get(block=True,timeout=None)
                if self.queue.qsize() >=100:
                    self.queue.clear()
                self.queue.put(reading)

            else:
                reading = self.probe.getReading()
            temp = reading.getTemperature()  + Ei1050Sensor.KELVINCONVERSION # convert from celsius to kelvin
            temperature = Measurement(self.id,Ei1050Sensor.code,"Temperature",temp,time=reading.getTime())
            humidity = Measurement(self.id,Ei1050Sensor.code,"Humidity",reading.getHumidity(),time=reading.getTime())
            container = Ei1050MeasurementContainer(temperature,humidity)
            self.retries =0
            return container
        except Exception as e:
            self.retries += 1
            print "Measurement not successful retrying"
            print e
            if self.retries < self.retry_limit:
                return self.measure()
            else: raise Exception("Measurement could not be completed: Retry limit exceeded")

    def disconnect(self):
        if self.threaded:
            self.probe.stop()
            

    def delete(self):
        del self.probe

    @classmethod
    def create(cls,configuration,device):
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
        data_pin = configuration["pins"]["data"]

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