from datetime import datetime
import quantities as pq
class Measurement(object):
    """
    Measurement class for storing measurements taken from sensors. 
    Passed around by the ni-engine system
    """
    def __init__(self,ID,code,name,value,time=datetime.now()):
        """
        :param str sensor_id: The ID of sensor from which measurement was taken
        :param str sensor_code: The code for sensor type which measurement comes from
        :param str measurement_name: Description of the measurement
        :param quantity.Quantity value: The value measured 
        :param datetime.datetime time: The time at which the measurement was taken
        """
        # Value must be of type pq.quantity
        assert type(value) is pq.Quantity

        self._id = ID
        self._code = code
        self._name = name
        self._value = value 
        self._time = time

    def __lt__(self,other):
        """
        Allow ordering based on time of measurements
        """
        return self._time < other._time

    @property
    def value(self):
        return self._value

    @property
    def id(self):
        return self._id


    @property
    def code(self):
        return self._code 

    @property
    def time(self):
        return self._time

    @property 
    def name(self):
        return self._name
    
    
   
    