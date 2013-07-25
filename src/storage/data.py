from datetime import datetime
import quantities as pq
import time 

class Data(object):
    """
    Measurement class for storing measurements taken from sensors. 
    Passed around by the ni-engine system
    """
    def __init__(self,ID,code,name,value,time=None):
        """
        :param str sensor_id: The ID of sensor from which measurement was taken
        :param str sensor_code: The code for sensor type which measurement comes from
        :param str measurement_name: Description of the measurement
        :param quantity.Quantity value: The value measured 
        :param datetime.datetime time: The time at which the measurement was taken
        """

        #make sure value is acceptable
        assert (isinstance(value,pq.Quantity) or isinstance(value,str) or
            isinstance(value,int) or isinstance(value,float) or
            isinstance(value,bool))
        
        time = datetime.now()
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
        """
        Gets value must be of valid type
        Returns
        -------
        pq.Quantity or str or int or float or bool
        """
        return self._value

    @property
    def id(self):
        """
        Returns
        -------
        str
            id of where the data was taken from
        """
        return self._id


    @property
    def code(self):
        """
        Returns
        -------
        str
            code of device data was taken from
        """
        return self._code 

    @property
    def time(self):
        """
        Returns
        -------
        datetime.datetime
        """
        return self._time

    @property 
    def name(self):
        """
        Returns
        -------
        str
            Measurement name (ie. temperature,distance etc.)
        """
        return self._name
    
    
   
    