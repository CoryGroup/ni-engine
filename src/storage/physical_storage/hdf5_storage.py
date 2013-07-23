
from abstract_physical_storage import AbstractPhysicalStorage
import tables import *
import numpy as np
import config


class TableMeasurement(tables.IsDescription):
    measurement_name = StringCol(50)
    code = StringCol(20)
    

class HDF5Storage(AbstractPhysicalStorage):

    """
    HDF5 data storage engine. 
    """
    code = "HDF5"
    
    def __init__(self,file_name,buffer_size=100):
        self._measurements= []
        self.buffer_size = buffer_size
        
    

    def create_measurement_row(self,group):
        if "time" not in group:
            group.create_dataset("time",(100,),maxshape=(None,),dtype=str)

        if "measurement" not in group:
            group.create_dataset("measurement",(100,),maxshape=(None,),dtype='f')
        
    def write_measurement(self,queue):
        """
        Is called when the number of measurements in measurement queue
        is greater than the bulk_write parameter

        Parameters
        ----------
        queue : ItemStore
        """

        data_to_write = queue.get_all()  
        print "writing"
        print data_to_write      
        self._measurements.append(data_to_write)
        
   





    @classmethod
    def create(cls,configuration):
        """
        Takes configuration, generates object of storage engine and returns it.

        Parameters
        ----------
        configuration : dictionary
            Configuration dictionary

        Returns 
        -------
        TestPhysicalStorage
            Object of class with correct configuration information
        """
        buffer_size = configuration.get('buffer_size',10)
        return TestPhysicalStorage(buffer_size)

  
      

    @property 
    def storage_code(self):
        """
        Should return the storage engine code
        
        Returns
        -------
        str
        """
        return TestPhysicalStorage.code
        


