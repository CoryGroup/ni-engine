import config 
from abc import ABCMeta, abstractmethod , abstractproperty
import threading
import copy
class AbstractPhysicalStorage :
    """
    Abstract physical storage class that must be implemented by all 
    physical storage mediums. 
    """
    __metaclass__ = ABCMeta


    CODE = "ABSTRACTSTORAGE"

    
    def store_measurement(self,type_measurement,measurement):
        """
        Takes a AbstractDataContainer and stores to file

        Parameters 
        ----------
        type_measurement : str 
            What type of information to store. Ie. controller, hardware or sensor
        measurement : AbstractMeasurement or list[AbstractMeasurement]

        """
        self.write_queue.add((type_measurement,copy.deepcopy(measurement)))
        print len(self.write_queue)
        if len(self.write_queue)>=self.bulk_write:
            self.write_measurement(self.write_queue)
        

    @abstractmethod
    def write_measurement(self,queue):
        """
        Is called when the number of measurements in measurement queue
        is greater than the bulk_write parameter

        Parameters
        ----------
        queue : ItemStore
        """
        pass
    
    def store_controller(self,controller_measurements):
        """
        Stores controller information

        Parameters
        ----------
        controller_measurements : AbstractDataContainer
        """
        self.write_measurement("controller",controller_measurements)

    
    def store_sensor(self,sensor_measurements):
        """
        Stores sensor information

        Parameters
        ----------
        sensor_measurements : AbstractDataContainer
        """
        self.write_measurement("sensor",sensor_measurements)

    
    def store_hardware(self,hardware_measurements):
        """
        Stores hardware information

        Parameters
        ----------
        hardware_measurements : AbstractDataContainer
        """
        self.write_measurement("hardware",hardware_measurements)




    @classmethod 
    @abstractmethod    
    def create(cls,configuration):
        """
        Takes configuration, generates object of storage engine and returns it.

        Parameters
        ----------
        configuration : dictionary
            Configuration dictionary

        Returns 
        -------
        AbstractPhysicalStorage
            Object of class with correct configuration information
        """
        pass

    @property
    def bulk_write(self):
        """
        property for how many measurements should be waited for until written to file
        """
        if not hasattr(self, '_bulk_write'):
            self._bulk_write = 0
            return int(self._bulk_write)
        else: return int(self._bulk_write)
    @bulk_write.setter    
    def sbulk_write(self,value):
        self._bulk_write = value
    

    @property
    def write_queue(self):
        """
        Queue that holds all of the AbstractDataContainers to be written. The data 
        inside the queue is a tuple of (measurement_type(str),AbstractDataContainer )
        """
        if not hasattr(self, '_write_queue'):
            self._write_queue = ItemStore()
            return self._write_queue
        else:
            return self._write_queue
    @write_queue.setter
    def write_queue(self,write_queue):
        assert isinstance(write_queue,ItemStore)
        self._write_queue = write_queue

    @abstractproperty
    def code(self):
        """
        Should return the storage engine code
        
        Returns
        -------
        str
        """
        pass
        


class ItemStore(object):
    """
    Threadsafe itemstore
    """

    def __init__(self):
        self.lock = threading.Lock()
        self.items = []

    def add(self, item):
        with self.lock:
            if isinstance(item, list):
                self.items.join(item)
            else:
                self.items.append(item)


    def get_all(self):
        with self.lock:
            items, self.items = self.items, []
        return items

    def __len__(self):
        with self.lock:
            length = reduce(lambda x,y : len(x)+len(y),self.items)
            print length
        return length
