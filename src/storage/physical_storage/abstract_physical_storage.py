import config 
from abc import ABCMeta, abstractmethod , abstractproperty
from queue import Queue
class AbstractPhysicalStorage :
    """
    Abstract physical storage class that must be implemented by all 
    physical storage mediums. 
    """
    __metaclass__ = ABCMeta


    

    
    def store_measurement(self,type_measurement,measurement):
        """
        Takes a AbstractDataContainer and stores to file

        Parameters 
        ----------
        type_measurement : str 
            What type of information to store. Ie. controller, hardware or sensor
        measurement : AbstractMeasurement or list[AbstractMeasurement]

        """
        self.write_queue.put((type_measurement,measurement.deepcopy()))
        if(self.write_queue.qsize()>=self.bulk_write):
            self.write_measurement()
        

    @abstractmethod
    def write_measurement(self):
        """
        Is called when the number of measurements in measurement queue
        is greater than the bulk_write parameter
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





    @abstractmethod
    def create(self,configuration):
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
        if self._bulk_write is not None:
            return self._bulk_write
        else: return 0
        
    def set_bulk_write(self,value):
        self._bulk_write = value
    

    @property
    def write_queue(self):
        """
        Queue that holds all of the AbstractDataContainers to be written. The data 
        inside the queue is a tuple of (measurement_type(str),AbstractDataContainer )
        """
        if self._write_queue is None:
            self._write_queue = MeasurementQueue()
            return self._write_queue
        else:
            return self._write_queue
    @write_queue.setter:
    def write_queue(self,write_queue):
        assert isinstance(write_queue,MeasurementQueue)
        self._write_queue = write_queue


        

class MeasurementQueue(Queue):
    """
    Normal, queue with size method overridden 
    and implemented to get number of measurements stored inside
    """
    def __init__(self,maxsize=0):
        super(MeasurementQueue, self).__init__(maxsize=maxsize)


    def _qsize(self, len=len):
        """
        Overide _qsize method of python standard library so that it works 
        with AbstractDataContainers
        """
        l = list(self.queue)
        return reduce(lambda x, y: len(x)+len(y), l)
