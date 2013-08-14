from datetime import datetime
import quantities as pq
import time 
import copy

class Data(object):


    """
    Data class for storing measurements taken from sensors. 
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
        assert isinstance(value,(pq.Quantity,str,int,float,long,bool))   
        
        time = datetime.now()
        self._id = ID
        self._code = code
        self._name = name
        self._value = value 
        self._time = time
        self._value_type = type(self._value)
        super(type(self.value),self).__init__(self.value)       

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
            Data name (ie. temperature,distance etc.)
        """
        return self._name

    def __repr__(self):
        return "( {0}, {1}, {2} )".format(self.name,self.time,self.value)

    def __str__(self):
        return "( {0}, {1}, {2} )".format(self.name,self.time,self.value)

    def __copy__(self,memo):
        t = type(self)
        return t(self.id,self.code,self.name,self.value,self.time)

    def __deepcopy__(self,memo):
        t = type(self)
        return t(self.id,self.code,self.name,copy.deepcopy(self.value),copy.deepcopy(self.time))

class FloatData(Data,float):
    def __init__(self,ID,code,name,value,time=None):
        assert(isinstance(value,float))                
        super(FloatData,self).__init__(ID,code,name,value,time)  

class StringData(Data,str):
    def __init__(self,ID,code,name,value,time=None):
        assert(isinstance(value,str))                
        super(StringData,self).__init__(ID,code,name,value,time)  

class IntData(Data,int):
    def __init__(self,ID,code,name,value,time=None):
        assert(isinstance(value,int))                
        super(IntData,self).__init__(ID,code,name,value,time) 

class LongData(Data,long):
    def __init__(self,ID,code,name,value,time=None):
        assert(isinstance(value,long))                
        Data.__init__(ID,code,name,value,time) 

class BoolData(Data):
    def __init__(self,ID,code,name,value,time=None):
        assert(isinstance(value,bool))            
        super(BoolData,self).__init__(ID,code,name,value,time)  

    def __nonzero__(self):
            return self.value

class QuantityData(Data,pq.Quantity):
    def __new__(cls, ID,code,name,value,time=None):
        return super(QuantityData, cls).__new__(cls, value, units=value.units)

    def __init__(self,ID,code,name,value,time=None):
        assert(isinstance(value,pq.Quantity))
        Data.__init__(self,ID,code,name,value,time)  
    
    def __deepcopy__(self,memo):
        t = type(self)
        return t(self.id,self.code,self.name,pq.Quantity(self.value.magnitude,self.value.units),
            copy.deepcopy(self.time))

def data(ID,code,name,value,time=None):
    "Factory method to create correct data object"
    if isinstance(value,int):
        return IntData(ID,code,name,value,time)
    elif isinstance(value,long):
        return LongData(ID,code,name,value,time)
    elif isinstance(value,bool):
        return Data(ID,code,name,value,time)
    elif isinstance(value,float):
        return FloatData(ID,code,name,value,time)
    elif isinstance(value,str):
        return StringData(ID,code,name,value,time)
    if isinstance(value,pq.Quantity):
        return QuantityData(ID,code,name,value,time)
    else:
        raise TypeError("Value is of type {0} and is not a supported data object".format(type(value)))
        

    



   






    